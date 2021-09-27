from trendr.extensions import celery
from trendr.extensions import db
from trendr.models import *


@celery.task
def add(x, y):
    return x + y


@celery.task
def test(arg):
    print(arg)
