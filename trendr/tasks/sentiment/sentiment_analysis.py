from trendr.extensions import celery


@celery.task
def tweet_analysis(**kwargs):
    pass


@celery.task
def reddit_submission_analysis(**kwargs):
    pass


@celery.task
def reddit_comment_analysis(**kwargs):
    pass

