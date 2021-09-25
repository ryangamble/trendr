from sqlalchemy.types import Integer, Text, DateTime, String

from trendr.extensions import db


class RedditPostModel(db.Model):
    __tablename__ = "reddit_posts"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    posted_at = db.Column(DateTime, nullable=False)
    up_votes = db.Column(Integer, nullable=False)
    down_votes = db.Column(Integer, nullable=False)
    sentiment_score = db.Column(Integer, nullable=False)

