from sqlalchemy import ForeignKey, Table

from trendr.extensions import db

# search associations
search_tweet_association = Table(
    "search_tweet",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id"), primary_key=True),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweet.id"), primary_key=True),
)
search_reddit_submission_association = Table(
    "search_reddit_submission",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id"), primary_key=True),
    db.Column(
        "reddit_submission_id",
        db.Integer(),
        ForeignKey("reddit_submission.id"),
        primary_key=True,
    ),
)
search_reddit_comment_association = Table(
    "search_reddit_comment",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("search.id"), primary_key=True),
    db.Column(
        "reddit_comment_id",
        db.Integer(),
        ForeignKey("reddit_comment.id"),
        primary_key=True,
    ),
)

# asset associations
asset_tweet_association = Table(
    "asset_tweet",
    db.metadata,
    db.Column("asset_id", db.Integer(), ForeignKey("asset.id"), primary_key=True),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweet.id"), primary_key=True),
)
asset_reddit_submission_association = Table(
    "asset_reddit_submission",
    db.metadata,
    db.Column("asset_id", db.Integer(), ForeignKey("asset.id"), primary_key=True),
    db.Column(
        "reddit_submission_id",
        db.Integer(),
        ForeignKey("reddit_submission.id"),
        primary_key=True,
    ),
)
asset_reddit_comment_association = Table(
    "asset_reddit_comment",
    db.metadata,
    db.Column("asset_id", db.Integer(), ForeignKey("asset.id"), primary_key=True),
    db.Column(
        "reddit_comment_id",
        db.Integer(),
        ForeignKey("reddit_comment.id"),
        primary_key=True,
    ),
)

# sentiment_data_point associations
sentiment_data_point_tweet_association = Table(
    "sentiment_data_point_tweet",
    db.metadata,
    db.Column(
        "sentiment_data_point_id",
        db.Integer(),
        ForeignKey("sentiment_data_point.id"),
        primary_key=True,
    ),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweet.id"), primary_key=True),
)
sentiment_data_point_reddit_submission_association = Table(
    "sentiment_data_point_reddit_submission",
    db.metadata,
    db.Column(
        "sentiment_data_point_id",
        db.Integer(),
        ForeignKey("sentiment_data_point.id"),
        primary_key=True,
    ),
    db.Column(
        "reddit_submission_id",
        db.Integer(),
        ForeignKey("reddit_submission.id"),
        primary_key=True,
    ),
)
sentiment_data_point_reddit_comment_association = Table(
    "sentiment_data_point_reddit_comment",
    db.metadata,
    db.Column(
        "sentiment_data_point_id",
        db.Integer(),
        ForeignKey("sentiment_data_point.id"),
        primary_key=True,
    ),
    db.Column(
        "reddit_comment_id",
        db.Integer(),
        ForeignKey("reddit_comment.id"),
        primary_key=True,
    ),
)

user_asset_association = Table(
    "user_asset",
    db.metadata,
    db.Column("user_id", db.Integer(), ForeignKey("user.id"), primary_key=True),
    db.Column("asset_id", db.Integer(), ForeignKey("asset.id"), primary_key=True),
)
