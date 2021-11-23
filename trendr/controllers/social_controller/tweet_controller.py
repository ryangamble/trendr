import tweepy
from typing import Union
from trendr.extensions import db
from trendr.models.search_model import Search
from trendr.models.tweet_model import Tweet
from tweepy.models import Status

def store_twitter_results(
    results: Union[tweepy.models.SearchResults, tweepy.models.Status],
    overwrite: bool = True,
    search_id: int = None,
) -> list[int]:
    if not results:
        return []

    if isinstance(results, tweepy.models.Status):
        results = [results]

    res_ids = []
    to_add = []

    search = None
    asset = None
    if search_id is not None:
        search = Search.query.filter_by(id=search_id).one()
        asset = search.asset

    for result in results:
        # do not accepted mixed-type results
        if not isinstance(result, tweepy.models.Status):
            raise Exception(f"Unsupported type for result: {type(result)}")

        existing = Tweet.query.filter_by(tweet_id=result.id).first()
        if existing:
            res_ids.append(existing.id)

            # overwrite with new data
            if overwrite:
                existing.text = result.text
                existing.likes = result.favorite_count
                existing.retweets = result.retweet_count
                # TODO: determine if we should overwrite sentiment scores
                existing.sentiment_score = None

            if search:
                search.tweets.append(existing)
            if asset and asset not in existing.assets:
                existing.assets.append(asset)
        else:
            if result.entities["urls"]:
                embed_url = result.entities["urls"][0]["expanded_url"]
            else:
                embed_url = None

            # generate new db row
            new_tweet = Tweet(
                tweet_id=result.id,
                text=result.text,
                tweeted_at=result.created_at,
                likes=result.favorite_count,
                retweets=result.retweet_count,
                embed_url=embed_url,
            )

            if asset:
                new_tweet.assets.append(asset)

            to_add.append(new_tweet)

    # add batch
    db.session.add_all(to_add)

    if search:
        search.tweets.extend(to_add)

    db.session.commit()

    res_ids.extend([added.id for added in to_add])

    # return ids
    return res_ids
