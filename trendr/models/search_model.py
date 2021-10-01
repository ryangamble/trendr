from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime, String
from sqlalchemy_utils import force_auto_coercion

from trendr.extensions import db
from trendr.models.association_tables import tweet_association_table, reddit_post_association_table


force_auto_coercion()


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
