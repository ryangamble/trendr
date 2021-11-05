from enum import Enum
from datetime import timedelta, datetime
from typing import List, Type, Union

from celery.canvas import chord, chain
from sqlalchemy.sql.base import Immutable
from trendr.extensions import celery, db
from trendr.models.search_model import Search, SearchType
from trendr.models.tweet_model import Tweet
from trendr.models.reddit_model import RedditSubmission, RedditComment
from trendr.tasks.social.twitter.gather import store_tweets_mentioning_asset
from trendr.tasks.social.reddit.gather import store_submissions, store_comments
from trendr.tasks.sentiment.sentiment_analysis import analyze_by_ids
from trendr.analyzers.aggregators import aggregate_sentiment_simple_mean


@celery.task
def perform_search(
    keyword: str,
    search_types: List[SearchType],
    search_id: int = None,
    time: int = None,
    limit: int = None,
):
    now = datetime.now()

    if search_id is None:
        search = Search(search_string=keyword, ran_at=now)
        search_id = search.id

    searched_types = set()
    chains = []

    reddit_args = {
        "keywords": [keyword],
        "after": time,
        "limit": limit,
        "search_id": search_id,
    }
    if time is None:
        del reddit_args["after"]
    if limit is None:
        del reddit_args["limit"]

    # 1. retreive socials, store and then get sentiment
    for search_type in search_types:
        # ignore duplicates
        if search_type in searched_types:
            continue

        curr_chain = None
        if search_type == SearchType.TWITTER:
            curr_chain = chain(
                store_tweets_mentioning_asset.signature(
                    kwargs={"asset_identifier": keyword, "search_id": search_id}
                ),
                analyze_by_ids.signature(
                    kwargs={"social_type": SearchType.TWITTER}
                ),
            )
        elif search_type == SearchType.REDDIT_SUBMISSION:
            curr_chain = chain(
                store_submissions.signature(kwargs=reddit_args),
                analyze_by_ids.signature(
                    kwargs={"social_type": SearchType.REDDIT_SUBMISSION}
                ),
            )
        elif search_type == SearchType.REDDIT_COMMENT:
            curr_chain = chain(
                store_comments.signature(kwargs=reddit_args),
                analyze_by_ids.signature(
                    kwargs={"social_type": SearchType.REDDIT_COMMENT}
                ),
            )
        chains.append(curr_chain)
        searched_types.add(search_type)

    # wait for all chains to complete, then aggregate sentiment
    res_chord = chord(
        chains,
        aggregate_sentiment_simple_mean_search.signature(
            (search_id,), immutable=True
        ),
    )

    res_chord.delay()


@celery.task
def aggregate_sentiment_simple_mean_search(search_id: int):
    search = Search.query.filter_by(id=search_id).one()
    if search.tweets:
        search.twitter_sentiment = aggregate_sentiment_simple_mean(
            search.tweets, 1)

    if search.reddit_submissions:
        search.reddit_sentiment = aggregate_sentiment_simple_mean(
            search.reddit_submissions, 2
        )

    elif search.reddit_comments:
        search.reddit_sentiment = aggregate_sentiment_simple_mean(
            search.reddit_comments, 3
        )
    # if search.tweets:
    #     search.twitter_sentiment = aggregate_sentiment_simple_mean(
    #         search.tweets
    #     )
    # search.reddit_sentiment = aggregate_sentiment_simple_mean(
    #     search.reddit_submissions
    # )
    # search.reddit_sentiment = aggregate_sentiment_simple_mean(
    #     search.reddit_comments
    # )
    db.session.commit()
