from trendr.models import *
from .test_data import *


def test_add_user(db_session):
    """
    Generate new user and make sure database can add it

    :param db_session: sqlalchemy database session
    """
    # add role
    new_role = Role(**new_role_data)
    db_session.add(new_role)
    db_session.commit()

    query_res = db_session.query(Role).filter_by(name=new_role_data["name"]).first()
    assert query_res is new_role

    # add user belonging to new_role
    new_user = User(**new_user_data)
    new_user.roles.append(new_role)
    db_session.add(new_user)
    db_session.commit()

    query_res = (
        db_session.query(User).filter_by(username=new_user_data["username"]).first()
    )
    assert query_res is new_user
    assert new_role in new_user.roles
    assert new_user in new_role.users

    # add twitter search belonging to new_user
    new_twitter_search = Search(**new_searches_data[0])
    new_user.searches.append(new_twitter_search)
    db_session.add(new_twitter_search)
    db_session.commit()

    query_res = db_session.query(Search).filter_by(id=new_twitter_search.id).first()
    assert query_res is new_twitter_search
    assert new_twitter_search in new_user.searches
    assert new_twitter_search.user == new_user

    # add tweets to new_twitter_search
    new_tweets = [Tweet(**new_tweet_data) for new_tweet_data in new_tweets_data]
    new_twitter_search.tweets.extend(new_tweets)
    db_session.add_all(new_tweets)
    db_session.commit()

    for new_tweet in new_tweets:
        query_res = db_session.query(Tweet).filter_by(id=new_tweet.id).first()
        assert query_res is new_tweet
        assert new_tweet in new_twitter_search.tweets
        assert new_twitter_search in new_tweet.searches
    
    # add reddit search belonging to new_user
    new_reddit_search = Search(**new_searches_data[0])
    new_user.searches.append(new_reddit_search)
    db_session.add(new_reddit_search)
    db_session.commit()

    query_res = db_session.query(Search).filter_by(id=new_reddit_search.id).first()
    assert query_res is new_reddit_search
    assert new_reddit_search in new_user.searches
    assert new_reddit_search.user == new_user

    # add reddit_posts to new_reddit_search
    new_reddit_posts = [RedditPost(**new_reddit_post_data) for new_reddit_post_data in new_reddit_posts_data]
    new_reddit_search.reddit_posts.extend(new_reddit_posts)
    db_session.add_all(new_reddit_posts)
    db_session.commit()

    for new_reddit_post in new_reddit_posts:
        query_res = db_session.query(RedditPost).filter_by(id=new_reddit_post.id).first()
        assert query_res is new_reddit_post
        assert new_reddit_post in new_reddit_search.reddit_posts
        assert new_reddit_search in new_reddit_post.searches
