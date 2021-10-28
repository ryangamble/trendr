from trendr.app import create_app
from trendr.extensions import celery
from trendr.tasks.basic import *
from trendr.tasks.mail import *
from trendr.tasks.reddit import *

app = create_app()
