import enum
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text, DateTime, String
from trendr.extensions import db
from trendr.models.association_tables import search_reddit_post_association


class RedditPostType(enum.Enum):
    TEXT = 1
    LINK = 2
    IMAGE = 3


class RedditPost(db.Model):
    __tablename__ = "reddit_posts"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    title = db.Column(String, nullable=False, unique=True)
    text = db.Column(Text, nullable=False)
    type = db.Column(Enum(RedditPostType))
    posted_at = db.Column(DateTime, nullable=False)
    up_votes = db.Column(Integer, nullable=False)
    down_votes = db.Column(Integer, nullable=False)
    sentiment_score = db.Column(Integer, nullable=True)

    # There is a many-many relationship between searches and reddit posts
    searches = relationship(
        "Search",
        secondary=search_reddit_post_association,
        back_populates="reddit_posts",
    )
