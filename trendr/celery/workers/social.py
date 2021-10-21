from trendr.app import create_app
from trendr.extensions import celery
from trendr.tasks.social import *

app = create_app()
