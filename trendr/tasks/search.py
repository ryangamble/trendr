from enum import Enum
import datetime
from functools import wraps
from typing import List
from celery.canvas import chord, chain
from trendr.extensions import celery, db
from trendr.models.search_model import Search, SearchType
from trendr.models.asset_model import Asset
from trendr.tasks.social.twitter.gather import store_tweets_mentioning_asset
from trendr.tasks.social.reddit.gather import store_submissions, store_comments
from trendr.tasks.sentiment.sentiment_analysis import analyze_by_ids
from trendr.analyzers.aggregators import create_datapoints as create_datapoints_ntask


@celery.task
def perform_search(
    asset_id: int,
    search_types: List[SearchType],
    earliest_ts: int,
    latest_ts: int = None,
    search_id: int = None,
    reddit_limit: int = None,
):
    asset = Asset.query.filter_by(id=asset_id).one()
    if search_id is None:
        now = datetime.datetime.now()
        search = Search(ran_at=now, asset=asset)
        search_id = search.id
    else:
        search = Search.query.filter_by(id=search_id).one()
        now = search.ran_at

    earliest = datetime.datetime.fromtimestamp(earliest_ts)
    latest = None
    if latest_ts:
        latest = datetime.datetime.fromtimestamp(latest_ts)
    else:
        latest = now

    if earliest > now:
        raise Exception("Can not perform search on data that doesn't exist")
    if latest < earliest:
        latest = now

    searched_types = set()
    chains = []

    reddit_args = {
        "search_str": asset.reddit_q,
        "after": int(earliest_ts),
        "limit": reddit_limit,
        "search_id": search_id,
    }
    if earliest is None:
        del reddit_args["after"]
    if reddit_limit is None:
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
                    kwargs={"asset_identifier": asset.twitter_q, "search_id": search_id}
                ),
                analyze_by_ids.signature(kwargs={"social_type": SearchType.TWITTER}),
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
        create_datapoints.signature(
            (search_id, earliest.timestamp(), latest.timestamp()), immutable=True
        ),
    )

    res_chord.delay()


@celery.task
def create_datapoints(*args, **kwargs):
    return create_datapoints_ntask(*args, **kwargs)
