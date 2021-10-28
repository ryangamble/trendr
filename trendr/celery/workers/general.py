from trendr.app import init_celery
from trendr.tasks.basic import *
from trendr.tasks.mail import *

celery = init_celery()
