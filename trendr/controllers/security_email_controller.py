from flask import (
    current_app as app,
    after_this_request,
    redirect,
    abort,
    url_for,
    render_template,
    flash,
    request,
)
from flask_security import current_user
from flask_security.decorators import auth_required
from flask_security.twofactor import tf_login
from flask_security.utils import (
    base_render_json,
    config_value,
    do_flash,
    get_message,
    get_token_status,
    get_url,
    hash_data,
    login_user,
    logout_user,
    verify_hash,
)
from flask_security.forms import email_required, email_validator
from flask_wtf import FlaskForm
from werkzeug.datastructures import ImmutableMultiDict
from wtforms import StringField, SubmitField
from wtforms.validators import EqualTo
from werkzeug.local import LocalProxy
from trendr.controllers.user_controller import find_user
from trendr.routes.helpers.json_response import json_response

_security = LocalProxy(lambda: app.extensions["security"])  # type: ignore
_datastore = LocalProxy(lambda: _security.datastore)


def _commit(response=None):
    _datastore.commit()
    return response


class ChangeEmailForm(FlaskForm):
    email = StringField("Email", validators=[email_required])
    new_email = StringField("New email", validators=[email_required, email_validator])
    new_email_confirm = StringField(
        "Retype email",
        validators=[EqualTo("new_email", message="Email does not match")],
    )
    submit = SubmitField("Change email")

    def validate(self):
        if not super(ChangeEmailForm, self).validate():
            return False

        if self.email.data != current_user.email:
            self.email.errors.append("Invalid email")
            return False
        if self.email.data.strip() == self.new_email.data.strip():
            self.email.errors.append(
                "Your new email must be different than your previous email"
            )
            return False
        if find_user(self.new_email.data):
            self.new_email.errors.append("Another user with this email already exists")
            return False
        return True


def confirm_change_email_token_status(token):
    """
    Returns the expired status, invalid status, user, and new email
    of a confirmation token. For example::
        expired, invalid, user, new_email = (
            confirm_change_email_token_status('...'))
    Based on confirm_email_token_status in Flask-Security.
    :param token: The confirmation token
    """
    expired, invalid, user, token_data = get_token_status(
        token, "confirm", "CONFIRM_EMAIL", return_data=True
    )
    new_email = None

    if not invalid and user:
        fs_uniquifier, token_email_hash, new_email = token_data
        invalid = not verify_hash(token_email_hash, user.email)

    return expired, invalid, user, new_email


def generate_change_email_confirmation_link(user, new_email):
    """Based on generate_confirmation_token in Flask-Security."""
    token = generate_change_email_confirmation_token(user, new_email)
    return (url_for("users.confirm_change_email", token=token, _external=True), token)


def generate_change_email_confirmation_token(user, new_email):
    """Generates a unique confirmation token for the specified user.
    Based on generate_confirmation_token in Flask-Security.
    :param user: The user to work with
    :param new_email: The user's new email address
    """
    data = [str(user.fs_uniquifier), hash_data(user.email), new_email]
    return _security.confirm_serializer.dumps(data)


def send_change_email_confirmation_instructions(user, new_email):
    """Sends the confirmation instructions email for the specified user.
    Based on send_confirmation_instructions in Flask-Security.
    :param user: The user to send the instructions to
    :param new_email: The user's new email address
    """

    confirmation_link, token = generate_change_email_confirmation_link(user, new_email)

    subject = "Please confim your change of email"
    msg_body = render_template(
        "confirm_change_email.html",
        user=user,
        new_email=new_email,
        confirmation_link=confirmation_link,
    )
    _security._mail_util.send_mail(
        template=None,
        subject=subject,
        recipient=new_email,
        sender=_security.email_sender,
        body="Change Email Confirmation",
        html=msg_body,
        user=None,
    )


def change_user_email(user, new_email):
    """Changes the email for the specified user
    Based on confirm_user in Flask-Security.
    :param user: The user to confirm
    :param new_email: The user's new email address
    """
    if user.email == new_email:
        return False

    user.email = new_email
    _datastore.put(user)

    return True


def confirm_change_email(token):
    """View function which handles a change email confirmation request.
    Based on confirm_email in Flask-Security."""
    expired, invalid, user, new_email = confirm_change_email_token_status(token)

    if not user or invalid:
        invalid = True
        m, c = get_message("INVALID_CONFIRMATION_TOKEN")
        if _security.redirect_behavior == "spa":
            return redirect(get_url(_security.confirm_error_view, qparams={c: m}))
        m, c = ("Invalid code", "error")
        return json_response({c: m})

    if expired:
        send_change_email_confirmation_instructions(user, new_email)
        m, c = (
            (
                "You did not confirm your change of email within {0}. "
                "New instructions to confirm your change of email have "
                "been sent to {1}."
            ).format(_security.confirm_email_within, new_email),
            "error",
        )
        if _security.redirect_behavior == "spa":
            return redirect(
                get_url(
                    _security.confirm_error_view,
                    qparams=user.get_redirect_qparams({c: m}),
                )
            )

        m, c = ("Expired code, resending", "error")
        return json_response({c: m})

    if invalid or expired:
        m, c = ("Invalid code", "error")
        return json_response({c: m})

    if user != current_user:
        logout_user()
        if config_value("AUTO_LOGIN_AFTER_CONFIRM"):
            # N.B. this is a (small) security risk if email went to wrong place.
            # and you have the LOGIN_WITH_CONFIRMATION flag since in that case
            # you can be logged in and doing stuff - but another person could
            # get the email.
            if config_value("TWO_FACTOR") and config_value("TWO_FACTOR_REQUIRED"):
                return tf_login(user, primary_authn_via="confirm")
            login_user(user, authn_via=["confirm"])

    if change_user_email(user, new_email):
        after_this_request(_commit)
        m, c = ("Thank you. Your change of email has been confirmed.", "success")
    else:
        m, c = ("Your change of email has already been confirmed.", "info")

    return json_response({c: m})


@auth_required("session")
def change_email():
    """Change email page."""
    if not _security.confirmable:
        abort(404)

    ret_json = request.accept_mimetypes.accept_json

    if request.is_json:
        form_data: ImmutableMultiDict = ImmutableMultiDict(request.get_json())
    else:
        form_data = request.form

    form = ChangeEmailForm(form_data)
    if form.validate_on_submit():
        new_email = form.new_email.data
        m, c = (
            (
                "Thank you. Confirmation instructions for changing "
                "your email have been sent to {0}."
            ).format(new_email),
            "success",
        )
        if config_value("SEND_REGISTER_EMAIL"):

            @after_this_request
            def prox(response=None):
                send_change_email_confirmation_instructions(current_user, new_email)
                return response

        if not ret_json:
            flash(m, c)

        if ret_json:
            return json_response({c: m})
        else:
            return redirect(url_for("users.get_settings_route"))

    if ret_json:
        return render_template("change_email.html", form=form)
    return base_render_json(form)
