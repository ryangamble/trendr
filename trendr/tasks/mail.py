from flask_mail import Message
from trendr.extensions import celery
from trendr.extensions import mail


@celery.task
def send_flask_mail(**kwargs):
    mail.send(Message(**kwargs))