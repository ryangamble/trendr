from sqlalchemy import ForeignKey, Table

from trendr.extensions import db

tweet_association_table = Table(
    'association',
    db.metadata,
    db.Column('search_id', ForeignKey('searches.id')),
    db.Column('tweet_id', ForeignKey('tweets.id'))
)

reddit_post_association_table = Table(
    'association',
    db.metadata,
    db.Column('search_id', ForeignKey('searches.id')),
    db.Column('reddit_post_id', ForeignKey('reddit_posts.id'))
)
