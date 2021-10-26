from trendr.app import init_celery
from trendr.tasks.social.reddit.gather import *
from trendr.tasks.social.twitter.gather import *

celery = init_celery()
