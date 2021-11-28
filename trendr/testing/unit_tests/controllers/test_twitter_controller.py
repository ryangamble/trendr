import pytest
from unittest.mock import MagicMock

from trendr.controllers.social_controller.tweet_controller import store_twitter_results


@pytest.mark.parametrize("existing", [True, False])
def test_store_twitter_results(mocker, existing):
    result_mock = MagicMock()
    result_mock.id = 1
    result_mock.text = "text"
    result_mock.created_at = 1
    result_mock.favorite_count = 1
    result_mock.retweet_count = 1
    result_mock.user.followers_count = 1
    result_mock.user.friends_count = 1
    result_mock.user.created_at = 1
    result_mock.user.verified = True
    mock_results = result_mock

    mocker.patch(
        "trendr.controllers.social_controller.tweet_controller.isinstance",
        return_value=True,
    )
    db_mock = mocker.patch("trendr.controllers.social_controller.tweet_controller.db")
    search_mock = mocker.patch(
        "trendr.controllers.social_controller.tweet_controller.Search"
    )
    tweet_mock = mocker.patch(
        "trendr.controllers.social_controller.tweet_controller.Tweet"
    )

    sub_tweet_filter_mock = MagicMock()
    tweet_mock.query.filter_by.return_value = sub_tweet_filter_mock
    if existing:
        sub_tweet_filter_mock.first.return_value = result_mock
    else:
        sub_tweet_filter_mock.first.return_value = None

    store_twitter_results(mock_results, False, None)
    search_mock.assert_not_called()
    if existing:
        tweet_mock.assert_not_called()
    else:
        tweet_mock.assert_called_once_with(
            tweet_id=1,
            text="text",
            tweeted_at=1,
            likes=1,
            retweets=1,
            tweeter_num_followers=1,
            tweeter_num_following=1,
            tweeter_created_at=1,
            tweeter_verified=1,
        )
    db_mock.session.add_all.assert_called_once()
    db_mock.session.commit.assert_called_once()
