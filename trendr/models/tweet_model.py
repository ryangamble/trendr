from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text, DateTime
from sqlalchemy_utils import force_auto_coercion

from trendr.extensions import db
from trendr.models.association_tables import tweet_association_table


force_auto_coercion()


class TweetModel(db.Model):
    __tablename__ = "tweets"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    tweet_id = db.Column(Integer, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    tweeted_at = db.Column(DateTime, nullable=False)
    likes = db.Column(Integer, nullable=False)
    retweets = db.Column(Integer, nullable=False)
    sentiment_score = db.Column(Integer, nullable=False)

    # There is a many-many relationship between searches and tweets
    searches = relationship("SearchModel", secondary=tweet_association_table)
