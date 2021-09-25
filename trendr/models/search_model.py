from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime, String

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


class SearchModel(db.Model):
    __tablename__ = "searches"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")

    ran_at = db.Column(DateTime, nullable=False)
    search_string = db.Column(String, nullable=False)

    # There is a one-many relationship between users and searches
    user_id = db.Column(Integer, ForeignKey('users.id'))
    # There is a many-many relationship between searches and tweets/reddit_posts
    tweets = relationship("TweetModel", secondary=tweet_association_table)
    reddit_posts = relationship("RedditPostModel", secondary=reddit_post_association_table)
