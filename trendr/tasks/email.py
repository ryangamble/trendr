from trendr.extensions import celery
from trendr.extensions import db
from trendr.models import *

@celery.task
def send_flask_mail(**kwargs):
    pass