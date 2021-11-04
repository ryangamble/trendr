from typing import Union
from statistics import mean
from trendr.models.reddit_model import RedditComment, RedditSubmission
from trendr.models.tweet_model import Tweet


def aggregate_sentiment_simple_mean(
    socials: Union[list[Tweet], list[RedditSubmission], list[RedditComment]]
):
    return mean([s.polarity for s in socials])
