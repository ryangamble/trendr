import tweepy
import pmaw
import datetime
import functools
import inspect
from enum import Enum
from typing import Union
from trendr.extensions import db
from trendr.models import Tweet, RedditSubmission, RedditSubmissionType


class SocialType(Enum):
    TWITTER = 0
    REDDIT_SUBMISSION = 1
    REDDIT_COMMENT = 2


def store_results(
    results: Union[tweepy.models.SearchResults, tweepy.models.Status, pmaw.Response],
    overwrite: bool = True,
) -> list[int]:
    """Store results from social connector endpoint in db

    :param results: list of social posts (or single twitter post) to add to database (ALL MUST BE SAME TYPE)
    :return: list of db ids of newly added objects
    """

    if not results:
        return []

    res_type = None
    if isinstance(results, tweepy.models.SearchResults):
        res_type = SocialType.TWITTER
    elif isinstance(results, tweepy.models.Status):
        res_type = SocialType.TWITTER
        results = [results]
    elif isinstance(results[0], pmaw.PushshiftAPI.submission):
        res_type = SocialType.REDDIT_SUBMISSION
    elif isinstance(results[0], pmaw.PushshiftAPI.comment):
        res_type = SocialType.REDDIT_COMMENT
    else:
        raise Exception(f"Unsupported type for results: {type(results)}")

    if res_type == SocialType.TWITTER:
        to_add = []
        for result in results:
            # do not accepted mixed-type results
            if not isinstance(result, tweepy.models.Status):
                raise Exception(f"Unsupported type for result: {type(result)}")

            # print(result.id)
            # print(result.text)
            # print(result.created_at)
            # print(result.favorite_count)
            # print(result.retweet_count)

            # generate new db row
            new_tweet = Tweet(
                tweet_id=result.id,
                text=result.text,
                tweeted_at=result.created_at,
                likes=result.favorite_count,
                retweets=result.retweet_count,
            )
            to_add.append(new_tweet)

        # add batch
        db.session.add_all(to_add)
        db.session.commit()

        # return ids
        return [tw.id for tw in to_add]

    elif res_type == SocialType.REDDIT_SUBMISSION:
        to_add = []
        for result in results:
            if not isinstance(result, pmaw.PushshiftAPI.submission):
                raise Exception(f"Unsupported type for result: {type(result)}")

            new_submission = RedditSubmission(
                reddit_id=result.id,
                permalink=result.permalink,
                title=result.title,
                text=result.selftext,
                type=(
                    RedditSubmissionType.TEXT
                    if result.selftext
                    else RedditSubmissionType.OTHER
                ),
                posted_at=datetime.datetime.fromtimestamp(result.created_utc),
                score=result.score,
            )
            to_add.append(new_submission)
        db.session.add_all(to_add)
        db.session.commit()
        return [sub.id for sub in to_add]
    elif res_type == SocialType.REDDIT_COMMENT:
        raise NotImplementedError("Reddit comments not yet implemented")


def store_in_db(
    api: Union[tweepy.API, pmaw.PushshiftAPI],
    overwrite: bool = True,
    wraps: callable = None,
) -> list[int]:
    """Decorator for twitter post retreival methods

    :param api: api to use for decorated function calls
    :param overwrite: whether to overwrite posts' data if they already exist, defaults to True
    :param wraps: if function being decorated is a wrapper for another function, pass original function as wraps
        and signature will be copied (do not do this yourself after wrapping, this returns a partial)
    :return: list of db ids in Tweet table
    """

    def wrapper(func):
        # copy signature
        if wraps:
            func.__signature__ = inspect.signature(wraps)

        @functools.wraps(func)
        def with_storing(*args, **kwargs):
            # insert arg
            kwargs["api"] = api

            # call wrapped function
            # NOTE: If you are getting exceptions here, stop passing api
            #   when calling function, it is already supplied
            res = func(*args, **kwargs)

            print("Got results, storing")

            return store_results(res)

        return with_storing

    return wrapper
