from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.types import Integer, DateTime, Float

from trendr.extensions import db
from trendr.models.association_tables import (
    sentiment_data_point_tweet_association,
    sentiment_data_point_reddit_submission_association,
    sentiment_data_point_reddit_comment_association,
)


class SentimentDataPoint(db.Model):
    __tablename__ = "sentiment_data_point"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")

    # datetime field
    datetime = db.Column(
        DateTime,
        nullable=False,
    )

    # There is a many-one relationship between sentiment_data_point and asset
    asset_id = db.Column(Integer, ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="sentiment_data_points")

    # There is a many-one relationship between sentiment_data_point and search
    search_id = db.Column(Integer, ForeignKey("search.id"))
    search = relationship("Search", back_populates="sentiment_data_points")

    twitter_sentiment = db.Column(Float, nullable=True)
    reddit_sentiment = db.Column(Float, nullable=True)

    # There is a many-many relationship between searches and tweets/reddit_submissions/reddit_comments
    tweets = relationship(
        "Tweet",
        secondary=sentiment_data_point_tweet_association,
        back_populates="sentiment_data_points",
    )
    reddit_submissions = relationship(
        "RedditSubmission",
        secondary=sentiment_data_point_reddit_submission_association,
        back_populates="sentiment_data_points",
    )
    reddit_comments = relationship(
        "RedditComment",
        secondary=sentiment_data_point_reddit_comment_association,
        back_populates="sentiment_data_points",
    )

    # create composite index to help when searching for asset setiment in time range
    __table_args__ = (Index("asset_time_sentiment_index", "asset_id", "datetime"),)
