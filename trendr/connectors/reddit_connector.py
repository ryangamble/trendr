import datetime
import pmaw
import praw
from enum import Enum
from psaw import PushshiftAPI
from sqlalchemy import desc
from typing import List

from trendr.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
)
from trendr.models.reddit_model import RedditComment, RedditSubmission


class RedditItem(Enum):
    """
    RedditItem enum differentiates between submissions and comments
    when calling api wrappers
    """

    SUBMISSION = 0
    COMMENT = 1


def create_praw_pmaw_api(
    client_id: str = REDDIT_CLIENT_ID,
    client_secret: str = REDDIT_CLIENT_SECRET,
    user_agent: str = REDDIT_USER_AGENT,
) -> pmaw.PushshiftAPI:
    """
    Create pmaw api object wrapping praw api object

    :param client_id: reddit api client id, defaults to REDDIT_CLIENT_ID
    :param client_secret: reddit api client secret, defaults to REDDIT_CLIENT_SECRET
    :param user_agent: reddit api user agent, defaults to REDDIT_USER_AGENT
    :raises Exception: if secrets are not found or authentication fails
    :return: pushshift api object
    """

    if client_id and client_secret and user_agent:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        return pmaw.PushshiftAPI(praw=reddit)
    else:
        raise Exception(
            "Could not authenticate to Reddit because the necessary secrets were not available"
        )


def create_pmaw_api() -> pmaw.PushshiftAPI:
    """
    Create pmaw api object

    :return: pushshift api object
    """

    return pmaw.PushshiftAPI()


def get_latest_submission_timestamp(asset_identifier: str) -> int or None:
    """
    Returns the timestamp of the latest submission stored in the database for a given identifier

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: A tweet id
    """
    asset = Asset.query.filter_by(identifier=asset_identifier)
    submission = (
        RedditSubmission.query.filter(
            RedditSubmission.assets.any(id=asset.id)
        )
        .order_by(desc(RedditSubmission.tweeted_at))
        .first()
    )
    if submission:
        return submission.posted_at.timestamp()
    return None


def get_latest_comment_timestamp(asset_identifier: str) -> int or None:
    """
    Returns the timestamp of the latest comment stored in the database for a given identifier

    :param asset_identifier: The identifier for the asset (AAPL, BTC), not a database id
    :return: A tweet id
    """
    comment = (
        RedditComment.query.filter(RedditComment.text.ilike(f"%{asset_identifier}%"))
        .order_by(desc(RedditComment.tweeted_at))
        .limit(1)
        .all()
    )
    if comment:
        return (comment[0].posted_at - datetime.datetime(1970, 1, 1)).total_seconds()
    return None


def gather_items(
    api: pmaw.PushshiftAPI,
    item: RedditItem,
    search_str: str,
    subreddits: List[str] = None,
    **kwargs,
) -> list:
    """
    Gather all reddit comments/submissions from subreddits between
    after and before which contain any keywords

    :param api: api object to use when gathering
    :param item: item to collect (comment or submission)
    :param search_str: string to use as q
    :param before: limit query to content posted before timestamp
    :param after: limit query to content posted after timestamp
    :param subreddits: strings of subreddit names to search,
        defaults to None (search all subreddits)
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :param limit: limit number of results to this maximum
    :return: res
    :rtype: list[pmaw.PushshiftAPI.comment or pmaw.PushshiftAPI.submission]
    """

    kwargs["q"] = search_str
    if subreddits:
        kwargs["subreddit"] = ",".join(subreddits)

    if item == RedditItem.SUBMISSION:
        # generator for submissions
        gen = api.search_submissions(**kwargs)
    elif item == RedditItem.COMMENT:
        # generator for comments
        gen = api.search_comments(**kwargs)

    return gen


def gather_submissions(**kwargs) -> list:
    """
    Gather all reddit submissions from subreddits between
    after and before which contain any keywords

    :param api: api object to use when gathering
    :param search_str: string to use as q
    :param before: limit query to content posted before timestamp
    :param after: limit query to content posted after timestamp
    :param subreddits: strings of subreddit names to search,
        defaults to None (search all subreddits)
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.submission]
    """
    if "keywords" in kwargs and "after" not in kwargs:
        timestamp = get_latest_submission_timestamp(kwargs["keywords"][0])
        if timestamp:
            kwargs["after"] = timestamp

    kwargs["item"] = RedditItem.SUBMISSION
    return gather_items(**kwargs)


def gather_comments(**kwargs) -> list:
    """
    Gather all reddit comments from subreddits between
    after and before which contain any keywords

    :param api: api object to use when gathering
    :param search_str: string to use as q
    :param before: limit query to content posted before timestamp
    :param after: limit query to content posted after timestamp
    :param subreddits: strings of subreddit names to search,
        defaults to None (search all subreddits)
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.comment]
    """
    if "keywords" in kwargs and "after" not in kwargs:
        timestamp = get_latest_comment_timestamp(kwargs["keywords"][0])
        if timestamp:
            kwargs["after"] = timestamp

    kwargs["item"] = RedditItem.COMMENT
    return gather_items(**kwargs)


def gather_items_by_id(api: pmaw.PushshiftAPI, item: RedditItem, **kwargs) -> list:
    """
    Gather all reddit comments/submissions by their ids

    :param api: api object to use when gathering
    :param item: item to collect (comment or submission)
    :param ids: ids to collect
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.comment or pmaw.PushshiftAPI.submission]
    """

    if item == RedditItem.SUBMISSION:
        # generator for submissions
        gen = api.search_submissions(**kwargs)
    elif item == RedditItem.COMMENT:
        # generator for comments
        gen = api.search_comments(**kwargs)

    return gen


def gather_submissions_by_id(**kwargs) -> list:
    """
    Gather all reddit submissions by their ids

    :param api: api object to use when gathering
    :param ids: ids to collect
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.submission]
    """

    kwargs["item"] = RedditItem.SUBMISSION
    return gather_items_by_id(**kwargs)


def gather_comments_by_id(**kwargs) -> list:
    """
    Gather all reddit comments by their ids

    :param api: api object to use when gathering
    :param ids: ids to collect
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.comment]
    """

    kwargs["item"] = RedditItem.COMMENT
    return gather_items_by_id(**kwargs)


def convert_time(unix_time) -> datetime:
    """
    Returns an RFC 1123 time string from a unix timestamp
    :param unix_time: time unix_time format
    :return: time as a datetime object
    """
    return datetime.datetime.utcfromtimestamp(unix_time)


def reddit_count_mentioning_asset(asset_identifier: str):
    """
    Queries Reddit for the count of posts and comments mentioning the asset.
    :param asset_identifier: The name of the asset (AAPL, BTC, Bitcoin, etc.)
    :return: a Python dictionary with the count data(startingHour: count)
     for each hour. The number of hours depends on the frequncy of mentions,
     for a max of 2000 posts(can be changed by changing the POST_COUNT variable)
     but it's left at 1,000 to not exceed api limits and for speed.
    """
    POSTS_COUNT = 1000
    psaw_api = PushshiftAPI()
    gen_subs = psaw_api.search_submissions(q=asset_identifier, limit=POSTS_COUNT)
    gen_comments = psaw_api.search_comments(q=asset_identifier, limit=POSTS_COUNT)

    results_comments = list(gen_comments)
    results_subs = list(gen_subs)

    timeDict = {}
    for i in results_comments:
        if type(i[len(i) - 1]) == float:
            time = convert_time(i[len(i) - 1])
            time2 = datetime.datetime(time.year, time.month, time.day, time.hour, 0, 0)
            if time2 not in timeDict:
                timeDict[time2] = 1
            else:
                timeDict[time2] += 1
        else:
            time = convert_time(i[len(i) - 1]["created"])
            time2 = datetime.datetime(time.year, time.month, time.day, time.hour, 0, 0)

            if time2 not in timeDict:
                timeDict[time2] = 1
            else:
                timeDict[time2] += 1

    for i in results_subs:
        if type(i[len(i) - 1]) == float:
            time = convert_time(i[len(i) - 1])
            time2 = datetime.datetime(time.year, time.month, time.day, time.hour, 0, 0)
            if time2 not in timeDict:
                timeDict[time2] = 1
            else:
                timeDict[time2] += 1
        else:
            time = convert_time(i[len(i) - 1]["created"])
            time2 = datetime.datetime(time.year, time.month, time.day, time.hour, 0, 0)
            if time2 not in timeDict:
                timeDict[time2] = 1
            else:
                timeDict[time2] += 1
    newDict = {}
    for key, value in timeDict.items():
        string_date_time = str(key)
        newDict[string_date_time] = value
    return newDict
