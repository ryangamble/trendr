from trendr.extensions import celery


@celery.task
def add(x, y):
    return x + y


@celery.task
def test(arg):
    print(arg)
