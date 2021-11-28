from typing import List
import datetime
import praw
import pmaw
from enum import Enum
from sqlalchemy import desc

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
    submission = (
        RedditSubmission.query.filter(
            RedditSubmission.text.ilike(f"%{asset_identifier}%")
        )
        .order_by(desc(RedditSubmission.tweeted_at))
        .limit(1)
        .all()
    )
    if submission:
        return (submission[0].posted_at - datetime.datetime(1970, 1, 1)).total_seconds()
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
    keywords: List[str],
    subreddits: List[str] = None,
    **kwargs,
) -> list:
    """
    Gather all reddit comments/submissions from subreddits between
    after and before which contain any keywords

    :param api: api object to use when gathering
    :param item: item to collect (comment or submission)
    :param keywords: strings to search for
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

    search_str = "|".join(keywords)

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
    :param keywords: strings to search for
    :param before: limit query to content posted before timestamp
    :param after: limit query to content posted after timestamp
    :param subreddits: strings of subreddit names to search,
        defaults to None (search all subreddits)
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.submission]
    """
    if kwargs["keywords"] and not kwargs["after"]:
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
    :param keywords: strings to search for
    :param before: limit query to content posted before timestamp
    :param after: limit query to content posted after timestamp
    :param subreddits: strings of subreddit names to search,
        defaults to None (search all subreddits)
    :param filters: fields to collect from each matching entity,
        defaults to None (collect all attributes)
    :return: res
    :rtype: list[pmaw.PushshiftAPI.comment]
    """
    if kwargs["keywords"] and not kwargs["after"]:
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


if __name__ == "__main__":
    api = create_pmaw_api()
    subs = list(gather_submissions_by_id(api, ["ptacat"]))
    print(type(subs[0]))
