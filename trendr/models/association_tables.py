from sqlalchemy import ForeignKey, Table

from trendr.extensions import db

# search associations
search_tweet_association = Table(
    "search_tweet",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id")),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweet.id")),
)
search_reddit_submission_association = Table(
    "search_reddit_submission",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id")),
    db.Column("reddit_submission_id", db.Integer(), ForeignKey("reddit_submission.id")),
)
search_reddit_comment_association = Table(
    "search_reddit_comment",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id")),
    db.Column("reddit_comment_id", db.Integer(), ForeignKey("reddit_comment.id")),
)

user_asset_association = Table(
    "user_asset",
    db.metadata,
    db.Column("user_id", db.Integer(), ForeignKey("user.id")),
    db.Column("asset_id", db.Integer(), ForeignKey("asset.id")),
)
