import pytest
import datetime
from unittest.mock import MagicMock

from trendr.controllers.social_controller import reddit_controller
from trendr.models.reddit_model import RedditSubmissionType


def test_attach_to(mocker):
    parent_mock = MagicMock()
    submission_mock = MagicMock()
    comment_mock = MagicMock()
    submissions = [submission_mock]
    submission_ids = [1]
    comments = [comment_mock]
    comment_ids = [1]

    reddit_submission_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditSubmission"
    )
    reddit_comment_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditComment"
    )

    sub_submission_filter_mock = MagicMock()
    reddit_submission_mock.query.filter_by.return_value = sub_submission_filter_mock
    sub_submission_filter_mock.first.return_value = submission_mock

    sub_comment_filter_mock = MagicMock()
    reddit_comment_mock.query.filter_by.return_value = sub_comment_filter_mock
    sub_comment_filter_mock.first.return_value = comment_mock

    reddit_controller.attach_to(
        parent_mock, submissions, submission_ids, comments, comment_ids
    )

    parent_mock.submissions.extend.assert_called_once_with(
        [submission_mock, submission_mock]
    )
    parent_mock.comments.extend.assert_called_once_with([comment_mock, comment_mock])


@pytest.mark.parametrize("existing", [True, False])
def test_store_subreddit(mocker, existing):
    name = "name"
    reddit_id = "1"
    mocked_subreddit = MagicMock()

    db_mock = mocker.patch("trendr.controllers.social_controller.reddit_controller.db")
    subreddit_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.Subreddit",
        return_value=mocked_subreddit,
    )

    sub_subreddit_filter_mock = MagicMock()
    subreddit_mock.query.filter_by.return_value = sub_subreddit_filter_mock

    if existing:
        sub_subreddit_filter_mock.first.return_value = mocked_subreddit
    else:
        sub_subreddit_filter_mock.first.return_value = None

    assert reddit_controller.store_subreddit(name, reddit_id) == mocked_subreddit

    if existing:
        db_mock.session.add.assert_not_called()
        db_mock.session.commit.assert_not_called()
    else:
        subreddit_mock.assert_called_once_with(name=name, reddit_id=reddit_id)
        db_mock.session.add.assert_called_once_with(mocked_subreddit)
        db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize("existing", [True, False])
def test_store_reddit_author(mocker, existing):
    username = "username"
    mocked_reddit_author = MagicMock()

    db_mock = mocker.patch("trendr.controllers.social_controller.reddit_controller.db")
    reddit_author_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditAuthor",
        return_value=mocked_reddit_author,
    )

    sub_reddit_author_filter_mock = MagicMock()
    reddit_author_mock.query.filter_by.return_value = sub_reddit_author_filter_mock

    if existing:
        sub_reddit_author_filter_mock.first.return_value = mocked_reddit_author
    else:
        sub_reddit_author_filter_mock.first.return_value = None

    assert reddit_controller.store_reddit_author(username) == mocked_reddit_author

    if existing:
        db_mock.session.add.assert_not_called()
        db_mock.session.commit.assert_not_called()
    else:
        reddit_author_mock.assert_called_once_with(username=username)
        db_mock.session.add.assert_called_once_with(mocked_reddit_author)
        db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize("existing", [True, False])
def test_store_reddit_comments(mocker, existing):
    comment_dict = {
        "id": 1,
        "body": "body",
        "created_utc": 1,
        "score": 0.5,
        "link_id": 1,
        "author": "author",
        "subreddit": "subreddit",
        "subreddit_id": 1,
        "permalink": "/permalink"
    }
    mock_reddit_comment = MagicMock()
    mock_reddit_comment.id = 1
    mock_reddit_comment.body = "body"
    mock_reddit_comment.posted_at = 1
    mock_reddit_comment.score = 0.5

    mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.isinstance",
        return_value=True,
    )
    db_mock = mocker.patch("trendr.controllers.social_controller.reddit_controller.db")
    search_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.Search"
    )
    reddit_comment_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditComment"
    )
    reddit_submission_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditSubmission"
    )
    store_author_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.store_reddit_author"
    )
    store_subreddit_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.store_subreddit"
    )

    sub_reddit_comment_filter_mock = MagicMock()
    reddit_comment_mock.query.filter_by.return_value = sub_reddit_comment_filter_mock
    if existing:
        sub_reddit_comment_filter_mock.first.return_value = mock_reddit_comment
    else:
        sub_reddit_comment_filter_mock.first.return_value = None

    sub_reddit_submission_filter_mock = MagicMock()
    reddit_submission_mock.query.filter_by.return_value = (
        sub_reddit_submission_filter_mock
    )
    sub_reddit_submission_filter_mock.first.return_value = None

    reddit_controller.store_reddit_comments([comment_dict], False, None)

    search_mock.assert_not_called()
    if existing:
        reddit_comment_mock.assert_not_called()
        reddit_submission_mock.query.filter_by.assert_not_called()
        store_author_mock.assert_not_called()
        store_subreddit_mock.assert_not_called()
    else:
        reddit_comment_mock.assert_called_once_with(
            reddit_id=1,
            text="body",
            posted_at=datetime.datetime.fromtimestamp(1),
            score=0.5,
            embed_url="https://www.reddit.com/permalink"
        )
        reddit_submission_mock.query.filter_by.assert_called_once_with(reddit_id=1)
        store_author_mock.assert_called_once_with(username="author")
        store_subreddit_mock.assert_called_once_with(name="subreddit", reddit_id=1)
    db_mock.session.add_all.assert_called_once()
    db_mock.session.commit.assert_called_once()


@pytest.mark.parametrize("existing", [True, False])
def test_store_reddit_submissions(mocker, existing):
    submission_dict = {
        "id": 1,
        "permalink": "permalink",
        "title": "title",
        "selftext": "selftext",
        "created_utc": 1,
        "score": 0.5,
        "author": "author",
        "subreddit": "subreddit",
        "subreddit_id": 1,
        "url": "url"
    }
    mock_reddit_submission = MagicMock()
    mock_reddit_submission.id = 1
    mock_reddit_submission.body = "body"
    mock_reddit_submission.posted_at = 1
    mock_reddit_submission.score = 0.5

    mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.isinstance",
        return_value=True,
    )
    db_mock = mocker.patch("trendr.controllers.social_controller.reddit_controller.db")
    search_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.Search"
    )
    reddit_submission_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.RedditSubmission"
    )
    store_author_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.store_reddit_author"
    )
    store_subreddit_mock = mocker.patch(
        "trendr.controllers.social_controller.reddit_controller.store_subreddit"
    )

    sub_reddit_submission_filter_mock = MagicMock()
    reddit_submission_mock.query.filter_by.return_value = (
        sub_reddit_submission_filter_mock
    )
    if existing:
        sub_reddit_submission_filter_mock.first.return_value = mock_reddit_submission
    else:
        sub_reddit_submission_filter_mock.first.return_value = None

    reddit_controller.store_reddit_submissions([submission_dict], False, None)

    search_mock.assert_not_called()
    if existing:
        reddit_submission_mock.assert_not_called()
        store_author_mock.assert_not_called()
        store_subreddit_mock.assert_not_called()
    else:
        reddit_submission_mock.assert_called_once_with(
            reddit_id=1,
            permalink="permalink",
            title="title",
            text="selftext",
            type=RedditSubmissionType.TEXT,
            posted_at=datetime.datetime.fromtimestamp(1),
            score=0.5,
            embed_url="url"
        )
        store_author_mock.assert_called_once_with(username="author")
        store_subreddit_mock.assert_called_once_with(name="subreddit", reddit_id=1)
    db_mock.session.add_all.assert_called_once()
    db_mock.session.commit.assert_called_once()
