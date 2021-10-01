from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text, DateTime, String
from sqlalchemy_utils import force_auto_coercion

from trendr.extensions import db
from trendr.models.association_tables import reddit_post_association_table


force_auto_coercion()


class RedditPostModel(db.Model):
    __tablename__ = "reddit_posts"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    posted_at = db.Column(DateTime, nullable=False)
    up_votes = db.Column(Integer, nullable=False)
    down_votes = db.Column(Integer, nullable=False)
    sentiment_score = db.Column(Integer, nullable=False)

    # There is a many-many relationship between searches and reddit posts
    searches = relationship("SearchModel", secondary=reddit_post_association_table)
