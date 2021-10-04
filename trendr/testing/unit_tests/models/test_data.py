import datetime
import string
from trendr.models.reddit_post_model import RedditPostType

new_user_data = {
    "username": "test_username",
    "first_name": "test firstname",
    "last_name": "test_lastname",
    "email": "test@test.test",
    "password": "test_password",
}
new_role_data = {
    "name": "test_role",
    "description": "This is a test role designed to test the role model",
}

new_searches_data = []
for i in range(0,2):
    new_search_data = {
        "ran_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "search_string": string.ascii_lowercase[i]*4
    }
    new_searches_data.append(new_search_data)

new_tweets_data = []
for i in range(0,2):
    new_tweet_data = {
        "tweet_id": int(str(i)*4),
        "text": f"This is test tweet {i}",
        "tweeted_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "likes": i,
        "retweets": i
    }
    new_tweets_data.append(new_tweet_data)

new_reddit_posts_data = []
for i in range(0,2):
    new_reddit_post_data = {
        "reddit_id": str(i)*4,
        "title": f"This is test title {i}",
        "text": f"This is test text {i}",
        "type": RedditPostType.TEXT,
        "posted_at": datetime.datetime.now() + datetime.timedelta(hours=i),
        "up_votes": i,
        "down_votes": i
    }
    new_reddit_posts_data.append(new_reddit_post_data)

