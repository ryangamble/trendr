from flask_security import MailUtil


class CeleryMailUtil(MailUtil):
    def send_mail(
        self, template, subject, recipient, sender, body, html, user, **kwargs
    ):
        # prevent being discovered on app creation
        from trendr.tasks.mail import send_flask_mail

        html = html.replace(":5000/auth/reset/", ":3000/set-password:")
        html = html.replace(":5000/auth/confirm/", ":3000/confirm-email:")
        html = html.replace(
            ":5000/users/confirm-change-email/", ":3000/confirm-change-email:"
        )
        # If the first replacement didn't occur, use this one
        html = html.replace("/auth/reset/", "/set-password:")
        html = html.replace("/auth/confirm/", "/confirm-email:")
        html = html.replace(
            "/users/confirm-change-email/", "/confirm-change-email:"
        )
        send_flask_mail.delay(
            subject=subject,
            sender=sender,
            recipients=[recipient],
            body=body,
            html=html,
        )
