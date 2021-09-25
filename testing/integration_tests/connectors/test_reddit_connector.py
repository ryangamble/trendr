import pytest
import pmaw
import datetime
from trendr.connectors import reddit_connector


@pytest.fixture
def praw_pmaw_api() -> pmaw.PushshiftAPI:
    """
    Creates pushshift api object wrapping praw api object

    :return: pushshift api object
    """
    return reddit_connector.create_praw_pmaw_api()


@pytest.fixture
def pmaw_api() -> pmaw.PushshiftAPI:
    """
    Creates pushshift api object

    :return: pushshift api object
    """
    return reddit_connector.create_pmaw_api()


# Positive tests


def test_get_post_by_id_positive(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving post by id

    :param pmaw_api: pushshift api object
    """

    submission_id = "ptacat"
    submissions = reddit_connector.gather_submissions_by_id(
        api=pmaw_api, ids=[submission_id]
    )

    assert len(submissions) == 1
    submission = next(submissions)
    assert submission["id"] == submission_id
    assert (
        submission["selftext"]
        == "Trendr is a project for Purdue's CS407 software engineering course. "
        "The goal of this project is to allow any investor to benefit from "
        "sentiment analysis of social media posts!"
    )


def test_get_comment_by_id_positive(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving comment by id

    :param pmaw_api: pushshift api object

    https://www.reddit.com/r/undefined/comments/ptacat/comment/hdvagh1/?utm_source=share&utm_medium=web2x&context=3
    """

    comment_id = "hd9f49u"
    comments = reddit_connector.gather_comments_by_id(api=pmaw_api, ids=[comment_id])

    assert len(comments) == 1
    comment = next(comments)
    assert comment["id"] == comment_id
    assert (
        comment["body"] == "&gt;2) rich people being able to create jobs and "
        "stimulate the economy.\n\n* I don't think that rich people should be "
        "taxed out of existence. It would probably be just fine if we could "
        "just get them to pay the sticker price when it comes to taxes.\n* "
        'I will push back on the "rich people being able to create jobs '
        "and stimulate the economy\" though. Not that they don't just "
        "that they are not necessary.\n   * Imagine a world where only "
        "rich people exist, could you have a successful Apple, Google, "
        "Facebook or Samsung?\n   * Imagine a world where only non-rich "
        "people existed, could you fund a successful Apple, Google, "
        "Facebook or Samsung?"
    )


def test_get_post_mentioning_asset_positive(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving posts matching keyword

    :param pmaw_api: pushshift api object
    """
    after = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
    keyword = "apple"
    submissions = reddit_connector.gather_submissions(
        api=pmaw_api, keywords=[keyword], after=after, limit=1
    )

    assert len(submissions) >= 1
    submission = next(submissions)
    assert (keyword in submission["selftext"].lower()) or (
        keyword in submission["title"].lower()
    )


def test_get_comment_mentioning_asset_positive(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving comments matching keyword

    :param pmaw_api: pushshift api object
    """
    after = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
    keyword = "apple"
    comments = reddit_connector.gather_comments(
        api=pmaw_api, keywords=[keyword], after=after, limit=1
    )

    assert len(comments) >= 1
    comment = next(comments)
    assert keyword in comment["body"].lower()


# Negative tests


def test_get_post_by_id(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving post by id that doesnt exist

    :param pmaw_api: pushshift api object
    """

    submission_id = "lkjlkjoin"
    with pytest.warns(UserWarning, match="items were not found in Pushshift"):
        submissions = reddit_connector.gather_submissions_by_id(
            api=pmaw_api, ids=[submission_id]
        )
    assert len(submissions) == 0


def test_get_comment_by_id(pmaw_api: pmaw.PushshiftAPI):
    """
    Tests retreiving comment by id that doesnt exist

    :param pmaw_api: pushshift api object
    """

    comment_id = "lkjlkjoin"
    with pytest.warns(UserWarning, match="items were not found in Pushshift"):
        comments = reddit_connector.gather_submissions_by_id(
            api=pmaw_api, ids=[comment_id]
        )
    assert len(comments) == 0
