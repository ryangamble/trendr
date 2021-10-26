from trendr.extensions import security
from trendr.models.user_model import Role, User
from trendr.models.search_model import Search
from trendr.models.tweet_model import Tweet
from trendr.models.reddit_model import RedditAuthor, RedditSubmission, RedditComment, Subreddit
from .test_data import (
    new_role_data,
    new_user_data,
    new_searches_data,
    new_tweets_data,
    new_reddit_submissions_data,
    new_reddit_comments_data,
    new_reddit_authors_data,
    new_subreddits_data,
)


def test_all(db_session, app):
    """
    Generate complex data and ensure database can handle it
    and adds correctly

    :param db_session: sqlalchemy database session
    """
    # add role
    new_role = security.datastore.create_role(**new_role_data)
    db_session.commit()

    query_res = db_session.query(Role).filter_by(name=new_role_data["name"]).first()
    
    assert query_res is new_role

    # add user belonging to new_role
    new_user = security.datastore.create_user(**new_user_data)
    security.datastore.add_role_to_user(new_user, new_role)
    db_session.commit()

    query_res = (
        db_session.query(User).filter_by(username=new_user_data["username"]).first()
    )
    assert query_res is new_user
    assert new_role in new_user.roles

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

    # add reddit authors
    new_reddit_authors = [
        RedditAuthor(**new_reddit_author_data)
        for new_reddit_author_data in new_reddit_authors_data
    ]
    db_session.add_all(new_reddit_authors)

    # add subreddits
    new_subreddits = [
        Subreddit(**new_subreddit_data)
        for new_subreddit_data in new_subreddits_data
    ]
    db_session.add_all(new_subreddits)

    # add reddit_posts to new_reddit_search
    new_reddit_submissions = [
        RedditSubmission(**new_reddit_post_data)
        for new_reddit_post_data in new_reddit_submissions_data
    ]
    db_session.add_all(new_reddit_submissions)

    for submission in new_reddit_submissions:
        submission.author = new_reddit_authors[0]
        submission.subreddit = new_subreddits[0]

    # add reddit comments to new_reddit_search
    new_reddit_comments = [
        RedditComment(**new_reddit_comment_data)
        for new_reddit_comment_data in new_reddit_comments_data
    ]
    db_session.add_all(new_reddit_comments)

    for comment in new_reddit_comments:
        comment.author = new_reddit_authors[1]
        comment.subreddit = new_subreddits[1]

    new_reddit_search.reddit_submissions.extend(new_reddit_submissions)
    new_reddit_search.reddit_comments.extend(new_reddit_comments)

    db_session.commit()

    for new_reddit_submission in new_reddit_submissions:
        query_res = (
            db_session.query(RedditSubmission).filter_by(id=new_reddit_submission.id).first()
        )
        assert query_res is new_reddit_submission
        assert new_reddit_submission in new_reddit_search.reddit_submissions
        assert new_reddit_search in new_reddit_submission.searches
        assert query_res.author == new_reddit_authors[0]
        assert new_reddit_submission in new_reddit_authors[0].comments
        assert query_res.subreddit == new_subreddits[0]
        assert new_reddit_submission in new_subreddits[1].comments

    for new_reddit_comment in new_reddit_comments:
        query_res = (
            db_session.query(RedditSubmission).filter_by(id=new_reddit_comment.id).first()
        )
        assert query_res is new_reddit_comment
        assert new_reddit_comment in new_reddit_search.reddit_comments
        assert new_reddit_search in new_reddit_comment.searches
        assert query_res.author == new_reddit_authors[1]
        assert new_reddit_comment in new_reddit_authors[1].comments
        assert query_res.subreddit == new_subreddits[1]
        assert new_reddit_comment in new_subreddits[1].comments
