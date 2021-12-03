from trendr.extensions import db
from trendr.models.asset_model import Asset
from trendr.models.search_model import Search
from trendr.models.sentiment_model import SentimentDataPoint
from datetime import datetime


def get_sentiment_scores(
    asset_identifier: str,
    start: datetime,
    end: datetime,
):
    """
    Get calcualted sentiment scores for an asset over a time range

    :param asset_identifier: asset identifier to search data points for
    :param start: start datetime of data point search range
    :param end: end datetime of data point search range
    :return: list of dictionaries containing only relevant data point
        information
    """
    asset = Asset.query.filter_by(identifier=asset_identifier).first()
    if not asset:
        return None
    data_points = SentimentDataPoint.query.filter(
        SentimentDataPoint.asset_id == asset.id,
        SentimentDataPoint.datetime >= start,
        SentimentDataPoint.datetime < end,
    ).all()
    return [
        {
            "timestamp": dp.datetime.timestamp(),
            "twitter_sentiment": dp.twitter_sentiment,
            "reddit_sentiment": dp.reddit_sentiment,
        }
        for dp in data_points
    ]


def get_important_posts(
    asset_identifier: str,
    datetime: datetime,
):
    """
    Get embeddable url for most important posts for data point

    :param asset_identifier: asset identifier of data point
    :param datetime: datetime of data point
    :return: dictionary of lists of embeddable links to posts
    """
    asset = Asset.query.filter_by(identifier=asset_identifier).first()
    if not asset:
        return None
    data_point = SentimentDataPoint.query.filter_by(
        asset_id=asset.id, datetime=datetime
    ).first()
    if data_point is None:
        return None

    return {
        "tweets": [p.embed_url for p in data_point.tweets],
        "reddit_submissions": [p.embed_url for p in data_point.reddit_submissions],
        "reddit_comments": [p.embed_url for p in data_point.reddit_comments],
    }
