from trendr.connectors import twitter_connector


# Positive tests

def test_twitter_connector_positive():
    tweet_id = "need-a-valid-id"  # TODO: Replace this with a valid id
    tweet = twitter_connector.get_tweet_by_id(tweet_id)
    assert tweet
    # TODO: Add assertions for the structure of the tweet


# Negative tests


def test_twitter_connector_invalid_id():
    """
    Tests what happens when you try to retrieve a tweet that doesn't exist
    """
    tweet_id = "invalid-id"
    tweet = twitter_connector.get_tweet_by_id(tweet_id)
    # TODO: Add assertions for error condition (exception raised?, tweet value, etc.)
