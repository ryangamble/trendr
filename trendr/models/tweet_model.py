from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import Integer, Text, DateTime, Float

from trendr.extensions import db
from trendr.models.association_tables import (
    search_tweet_association,
    asset_tweet_association,
    sentiment_data_point_tweet_association,
)


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    tweet_id = db.Column(Integer, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    tweeted_at = db.Column(DateTime, nullable=False)
    likes = db.Column(Integer, nullable=False)
    retweets = db.Column(Integer, nullable=False)
    embed_url = db.Column(Text, nullable=True)
    polarity = db.Column(Float, nullable=True)
    subjectivity = db.Column(Float, nullable=True)
    sentiment_score = db.Column(Float, nullable=True)

    # There is a many-many relationship between searches and tweets
    searches = relationship(
        "Search",
        secondary=search_tweet_association,
        back_populates="tweets",
    )

    # There is a one-way many-many relationship between tweet and asset
    assets = relationship(
        "Asset",
        secondary=asset_tweet_association,
        backref=backref("tweets", lazy=None),
    )

    # There is a many-many relationship between sentiment_data_points and tweets
    sentiment_data_points = relationship(
        "SentimentDataPoint",
        secondary=sentiment_data_point_tweet_association,
        back_populates="tweets",
    )
