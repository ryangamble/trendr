from ..extensions import celery
from ..extensions import db
from ..models import *

@celery.task
def add(x, y):
    return x + y