from sqlalchemy import ForeignKey, Table
from trendr.extensions import db

# search associations
search_tweet_association = Table(
    "searches_tweets",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("searches.id")),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweets.id")),
)
search_reddit_submission_association = Table(
    "searches_reddit_submission",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("searches.id")),
    db.Column("reddit_submission_id", db.Integer(), ForeignKey("reddit_submissions.id")),
)
search_reddit_comment_association =(
    "searches_reddit_comment",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("searches.id")),
    db.Column("reddit_comment_id", db.Integer(), ForeignKey("reddit_comments.id")),
)