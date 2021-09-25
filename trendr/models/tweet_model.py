from sqlalchemy.types import Integer, Text, DateTime

from trendr.extensions import db


class TweetModel(db.Model):
    __tablename__ = "tweets"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    tweet_id = db.Column(Integer, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    tweeted_at = db.Column(DateTime, nullable=False)
    likes = db.Column(Integer, nullable=False)
    retweets = db.Column(Integer, nullable=False)
    sentiment_score = db.Column(Integer, nullable=False)

