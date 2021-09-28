from sqlalchemy import ForeignKey, Table
from sqlalchemy_utils import force_auto_coercion

from trendr.extensions import db

force_auto_coercion()

tweet_association_table = Table(
    'searches_tweets_association_table',
    db.metadata,
    db.Column('search_id', ForeignKey('searches.id')),
    db.Column('tweet_id', ForeignKey('tweets.id'))
)

reddit_post_association_table = Table(
    'searches_reddit_posts_association_table',
    db.metadata,
    db.Column('search_id', ForeignKey('searches.id')),
    db.Column('reddit_post_id', ForeignKey('reddit_posts.id'))
)
