from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime, String

from trendr.extensions import db
from trendr.models.association_tables import (
    search_tweet_association,
    search_reddit_post_association,
)


class Search(db.Model):
    __tablename__ = "searches"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")

    ran_at = db.Column(DateTime, nullable=False)
    search_string = db.Column(String, nullable=False)

    # There is a many-many relationship between searches and tweets/reddit_posts
    tweets = relationship(
        "Tweet",
        secondary=search_tweet_association,
        back_populates="searches",
    )
    reddit_posts = relationship(
        "RedditPost",
        secondary=search_reddit_post_association,
        back_populates="searches",
    )

    user_id = db.Column(Integer, ForeignKey("users.id"))
    # There is a many-one relationship between search and user
    user = relationship("User", back_populates="searches")
