from sqlalchemy import ForeignKey, Table
from trendr.extensions import db

search_tweet_association = Table(
    "searches_tweets",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("searches.id")),
    db.Column("tweet_id", db.Integer(), ForeignKey("tweets.id")),
)

search_reddit_post_association = Table(
    "searches_reddit_posts",
    db.metadata,
    db.Column("search_id", db.Integer(), ForeignKey("searches.id")),
    db.Column("reddit_post_id", db.Integer(), ForeignKey("reddit_posts.id")),
)
