from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text, DateTime, Float, Boolean, BigInteger

from trendr.extensions import db
from trendr.models.association_tables import search_tweet_association


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    tweet_id = db.Column(BigInteger, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    tweeted_at = db.Column(DateTime, nullable=False)
    likes = db.Column(Integer, nullable=False)
    retweets = db.Column(Integer, nullable=False)
    polarity = db.Column(Float, nullable=True)
    subjectivity = db.Column(Float, nullable=True)
    tweeter_num_followers = db.Column(Integer, nullable=False)
    tweeter_num_following = db.Column(Integer, nullable=False)
    tweeter_created_at = db.Column(DateTime, nullable=False)
    tweeter_verified = db.Column(Boolean, nullable=False)

    # There is a many-many relationship between searches and tweets
    searches = relationship(
        "Search",
        secondary=search_tweet_association,
        back_populates="tweets",
    )
