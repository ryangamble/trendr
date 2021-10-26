import datetime
import string
from trendr.models.reddit_model import RedditSubmissionType

new_user_data = {
    "username": "test_username",
    "email": "test@test.test",
    "password": "test_password",
    "active": True,
    "fs_uniquifier": "test",
}
new_role_data = {
    "name": "test_role",
    "description": "This is a test role designed to test the role model",
}

new_searches_data = []
for i in range(0, 2):
    new_search_data = {
        "ran_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "search_string": string.ascii_lowercase[i]*4
    }
    new_searches_data.append(new_search_data)

new_tweets_data = []
for i in range(0, 2):
    new_tweet_data = {
        "tweet_id": int(str(i)*4),
        "text": f"This is test tweet {i}",
        "tweeted_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "likes": i,
        "retweets": i
    }
    new_tweets_data.append(new_tweet_data)

new_reddit_submissions_data = []
for i in range(0,2):
    new_reddit_post_data = {
        "reddit_id": str(i)*4,
        "permalink": f"This is test permalink {i}",
        "title": f"This is test title {i}",
        "text": f"This is test text {i}",
        "type": RedditSubmissionType.TEXT,
        "posted_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "up_votes": i,
        "down_votes": i,
        "score": 0,
    }
    new_reddit_submissions_data.append(new_reddit_post_data)


new_reddit_comments_data = []
for i in range(0,2):
    new_reddit_comment_data = {
        "reddit_id": str(i)*4,
        "text": f"This is test text {i}",
        "posted_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "up_votes": i,
        "down_votes": i,
        "score": 0,
    }
    new_reddit_comments_data.append(new_reddit_comment_data)

new_reddit_authors_data = []
for i in range(0,2):
    new_reddit_author_data = {
        "username": str(i)*4
    }
    new_reddit_authors_data.append(new_reddit_author_data)

new_subreddits_data = []
for i in range(0,2):
    new_subreddit_data = {
        "reddit_id": str(i)*4,
        "name": f"This is test name {i}",
        "subscribers": i
    }
    new_subreddits_data.append(new_subreddit_data)
