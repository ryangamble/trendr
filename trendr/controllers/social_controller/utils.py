from re import search
import tweepy
import pmaw
import functools
import inspect
from typing import Union

from .reddit_controller import store_reddit_results
from .tweet_controller import store_twitter_results


def store_results(
    results: Union[
        tweepy.models.SearchResults, tweepy.models.Status, pmaw.Response
    ],
    overwrite: bool = True,
    search_id: int = None,
) -> list[int]:
    """Store results from social connector endpoint in db

    :param results: list of social posts (or single twitter post) to add to database (ALL MUST BE SAME TYPE)
    :return: list of db ids of newly added objects
    """

    if isinstance(results, tweepy.models.SearchResults) or isinstance(
        results, tweepy.models.Status
    ):
        return store_twitter_results(results, overwrite, search_id)
    elif isinstance(results, pmaw.Response):
        # do not return database model class becuase its unnecessary to serialize
        #   caller should know which type of results it is passing
        return store_reddit_results(results, overwrite, search_id)[1]
    else:
        raise Exception(f"Unsupported type for results: {type(results)}")


def store_in_db(
    # api: Union[tweepy.API, pmaw.PushshiftAPI],
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
        # if wraps:
        #     func.__signature__ = inspect.signature(wraps)

        @functools.wraps(func)
        def with_storing(*args, **kwargs):
            # insert arg
            # kwargs["api"] = api

            search_id = None
            if "search_id" in kwargs:
                search_id = kwargs.pop("search_id")

            # call wrapped function
            # NOTE: If you are getting exceptions here, stop passing api
            #   when calling function, it is already supplied
            res = func(*args, **kwargs)

            return store_results(res, overwrite=overwrite, search_id=search_id)

        return with_storing

    return wrapper
