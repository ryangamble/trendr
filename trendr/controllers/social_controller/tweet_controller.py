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
                existing.tweeter_num_followers = result.user.followers_count
                existing.tweeter_num_following = result.user.friends_count
                existing.tweeter_created_at = result.user.created_at
                existing.tweeter_verified = result.user.verified

            if search:
                search.tweets.append(existing)
            if asset and asset not in existing.assets:
                existing.assets.append(asset)

            db.session.commit()
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
                tweeter_num_followers=result.user.followers_count,
                tweeter_num_following=result.user.friends_count,
                tweeter_created_at=result.user.created_at,
                tweeter_verified=result.user.verified,
                embed_url=embed_url,
            )

            if asset:
                new_tweet.assets.append(asset)
            if search:
                search.tweets.append(new_tweet)

            db.session.add(new_tweet)
            db.session.commit()
            res_ids.append(new_tweet.id)

    # return ids
    return res_ids
