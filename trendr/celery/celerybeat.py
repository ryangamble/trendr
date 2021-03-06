from celery.schedules import crontab
from trendr.app import init_celery
from trendr.tasks.basic import *
from trendr.tasks.mail import *
from trendr.tasks import *

celery = init_celery()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s("hello"), name="add every 10")

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(
    #     30.0,
    #     send_flask_mail.s(
    #         subject="Test",
    #         sender="admin@trendr.dev",
    #         recipients=["admin@trendr.dev"],
    #         body="test",
    #         html="<h1>Title</h1><br><p>Paragraph</p>",
    #     ),
    #     expires=10,
    # )

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s("Happy Mondays!"),
    )
