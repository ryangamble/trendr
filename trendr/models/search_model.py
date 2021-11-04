from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.types import Integer, DateTime, String, Float

from trendr.extensions import db
from trendr.models.association_tables import (
    search_tweet_association,
    search_reddit_submission_association,
    search_reddit_comment_association,
)


class SearchType(Enum):
    TWITTER = 0
    REDDIT_SUBMISSION = 1
    REDDIT_COMMENT = 2


class Search(db.Model):
    __tablename__ = "search"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")

    ran_at = db.Column(DateTime, nullable=False)
    search_string = db.Column(String, nullable=False)

    twitter_sentiment = db.Column(Float, nullable=True)
    reddit_sentiment = db.Column(Float, nullable=True)

    # There is a many-many relationship between searches and tweets/reddit_submissions/reddit_comments
    tweets = relationship(
        "Tweet",
        secondary=search_tweet_association,
        back_populates="searches",
    )
    reddit_submissions = relationship(
        "RedditSubmission",
        secondary=search_reddit_submission_association,
        back_populates="searches",
    )
    reddit_comments = relationship(
        "RedditComment",
        secondary=search_reddit_comment_association,
        back_populates="searches",
    )

    user_id = db.Column(Integer, ForeignKey("user.id"))
    # There is a many-one relationship between search and user
    user = relationship("User", back_populates="searches")
