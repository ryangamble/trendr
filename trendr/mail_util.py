from flask_security import MailUtil
from trendr.tasks.mail import send_flask_mail

class CeleryMailUtil(MailUtil):
    def send_mail(self, template, subject, recipient, sender, body, html, user, **kwargs):
        send_flask_mail.delay(
            subject=subject,
            sender=sender,
            recipients=[recipient],
            body=body,
            html=html
        )