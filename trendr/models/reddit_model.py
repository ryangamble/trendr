import enum
from sqlalchemy import Enum
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import Integer, Text, DateTime, String, Float
from trendr.extensions import db
from trendr.models.association_tables import (
    search_reddit_submission_association,
    search_reddit_comment_association,
    asset_reddit_submission_association,
    asset_reddit_comment_association,
    sentiment_data_point_reddit_submission_association,
    sentiment_data_point_reddit_comment_association,
)


class RedditSubmissionType(enum.Enum):
    TEXT = 0
    OTHER = 1


class RedditSubmission(db.Model):
    __tablename__ = "reddit_submission"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    permalink = db.Column(String, nullable=False)
    title = db.Column(String, nullable=False)
    text = db.Column(Text, nullable=True)
    type = db.Column(Enum(RedditSubmissionType))
    posted_at = db.Column(DateTime, nullable=False)
    up_votes = db.Column(Integer, nullable=True)
    down_votes = db.Column(Integer, nullable=True)
    score = db.Column(Integer, nullable=True)
    embed_url = db.Column(Text, nullable=False)
    polarity = db.Column(Float, nullable=True)
    subjectivity = db.Column(Float, nullable=True)
    sentiment_score = db.Column(Float, nullable=True)

    # There is a one-many relationship between subreddits and reddit_submissions
    subreddit_id = db.Column(Integer, ForeignKey("subreddit.id"))
    subreddit = relationship("Subreddit", back_populates="submissions")

    # There is a one-many relationship between reddit posts and reddit comments
    comments = relationship("RedditComment", back_populates="submission")

    # There is a many-many relationship between searches and reddit posts
    searches = relationship(
        "Search",
        secondary=search_reddit_submission_association,
        back_populates="reddit_submissions",
    )

    # There is a one-way many-many relationship between reddit_submission and asset
    assets = relationship(
        "Asset",
        secondary=asset_reddit_submission_association,
        backref=backref("reddit_submissions", lazy=None),
    )

    # There is a many-many relationship between sentiment_data_points and tweets
    sentiment_data_points = relationship(
        "SentimentDataPoint",
        secondary=sentiment_data_point_reddit_submission_association,
        back_populates="reddit_submissions",
    )

    # There is a one-many relationship between authors and reddit_submissions
    author_id = db.Column(Integer, ForeignKey("reddit_author.id"))
    author = relationship(
        "RedditAuthor",
        back_populates="submissions",
    )


class RedditComment(db.Model):
    __tablename__ = "reddit_comment"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    text = db.Column(Text, nullable=True)
    posted_at = db.Column(DateTime, nullable=False)
    up_votes = db.Column(Integer, nullable=True)
    down_votes = db.Column(Integer, nullable=True)
    score = db.Column(Integer, nullable=True)
    embed_url = db.Column(Text, nullable=False)
    polarity = db.Column(Float, nullable=True)
    subjectivity = db.Column(Float, nullable=True)
    sentiment_score = db.Column(Float, nullable=True)

    # There is a one-many relationship between reddit posts and reddit comments
    submission_id = db.Column(Integer, ForeignKey("reddit_submission.id"))
    submission = relationship("RedditSubmission", back_populates="comments")

    # There is a one-many relationship between subreddits and reddit_comments
    subreddit_id = db.Column(Integer, ForeignKey("subreddit.id"))
    subreddit = relationship("Subreddit", back_populates="comments")

    # There is a many-many relationship between searches and reddit comments
    searches = relationship(
        "Search",
        secondary=search_reddit_comment_association,
        back_populates="reddit_comments",
    )

    # There is a one-way many-many relationship between reddit_comment and asset
    assets = relationship(
        "Asset",
        secondary=asset_reddit_comment_association,
        backref=backref("reddit_comments", lazy=None),
    )

    # There is a many-many relationship between sentiment_data_points and tweets
    sentiment_data_points = relationship(
        "SentimentDataPoint",
        secondary=sentiment_data_point_reddit_comment_association,
        back_populates="reddit_comments",
    )

    # There is a one-many relationship between authors and reddit_comments
    author_id = db.Column(Integer, ForeignKey("reddit_author.id"))
    author = relationship(
        "RedditAuthor",
        back_populates="comments",
    )


class Subreddit(db.Model):
    __tablename__ = "subreddit"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    reddit_id = db.Column(String, nullable=False, unique=True)
    name = db.Column(Text, nullable=False, unique=True)
    subscribers = db.Column(Integer, nullable=True)

    # There is a one-many relationship between subreddits and reddit_comments
    submissions = relationship("RedditSubmission", back_populates="subreddit")

    # There is a one-many relationship between subreddits and reddit_comments
    comments = relationship("RedditComment", back_populates="subreddit")


class RedditAuthor(db.Model):
    __tablename__ = "reddit_author"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    username = db.Column(String, nullable=False, unique=True)

    # There is a many-many relationship between authors and reddit_submissions
    submissions = relationship(
        "RedditSubmission",
        back_populates="author",
    )

    # There is a many-many relationship between authors and reddit_comments
    comments = relationship(
        "RedditComment",
        back_populates="author",
    )
