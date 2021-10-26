import pmaw
import datetime
from typing import Union
from trendr.extensions import db
from trendr.models.reddit_model import (
    RedditAuthor,
    RedditSubmission,
    RedditSubmissionType,
    RedditComment,
    Subreddit,
)


def attach_to(
    parent: Union[RedditAuthor, Subreddit, RedditSubmission],
    submissions: list[RedditSubmission] = [],
    submission_ids: list[int] = [],
    comments: list[RedditComment] = [],
    comment_ids: list[int] = [],
):
    """
    Attach submissions/comments to parent (author, subreddit, submission)

    :param parent: parent object to attach to (author, subreddit or submission)
    :param submissions: list of RedditSubmission objects, defaults to []
    :param submission_ids: list of RedditSubmission ids, defaults to []
    :param comments: list of RedditComment objects, defaults to []
    :param comment_ids: list of RedditComment ids, defaults to []
    """

    submissions_from_ids = []
    for submission_id in submission_ids:
        submission = RedditSubmission.query.filter_by(id=submission_id).first()
        if submission:
            submissions_from_ids.append(submission)

    comments_from_ids = []
    for comment_id in comment_ids:
        comment = RedditComment.query.filter_by(id=comment_id).first()
        if comment:
            comments_from_ids.append(comment)

    tot_submissions = submissions + submissions_from_ids
    tot_comments = comments + comments_from_ids

    if tot_submissions:
        parent.submissions.extend(tot_submissions)
    if tot_comments:
        parent.comments.extend(tot_comments)


def store_subreddit(
    name: str,
    reddit_id: str,
) -> Subreddit:
    """
    Store subreddit in database if it is not present

    :param name: name of subreddit
    :param reddit_id: reddit id of subreddit
    :return: newly created subreddit
    """

    subreddit = Subreddit.query.filter_by(reddit_id=reddit_id).first()
    if not subreddit:
        subreddit = Subreddit(name=name, reddit_id=reddit_id)
        db.session.add(subreddit)
        db.session.commit()
    return subreddit


def store_reddit_author(username: str) -> int:
    """
    Store reddit author in database if it is not present

    :param username: Author's username
    :return: newly created author
    """

    author = RedditAuthor.query.filter_by(username=username).first()
    if not author:
        author = RedditAuthor(username=username)
        db.session.add(author)
        db.session.commit()
    return author


def store_reddit_results(
    results: pmaw.Response, overwrite: bool = True
) -> tuple[Union[RedditSubmission, RedditComment], list[int]]:
    """
    Store reddit result (comments or submissions) in database

    :param result: [description]
    :param overwrite: [description], defaults to True
    :return: tuple containing (db model results stored in, list of newly-created submission ids)
    """

    if not results:
        return None, []

    # determine type
    if "title" in results.responses[results.i]:
        return RedditSubmission, store_reddit_submissions(
            submissions=results, overwrite=overwrite
        )
    else:
        return RedditComment, store_reddit_comments(
            comments=results, overwrite=overwrite
        )


def store_reddit_comments(comments: pmaw.Response, overwrite: bool = True) -> list[int]:
    """
    Store reddit comments from a pmaw Response

    :param comments: pmaw.Response object containing comment dicts
    :param overwrite: overwrite existing comments if updated information is found, defaults to True
    :return: list of newly-created comment ids
    """

    if not comments:
        return []

    res_ids = []
    to_add = []

    for result in comments:

        existing = RedditComment.query.filter_by(reddit_id=result["id"]).first()
        if existing:
            res_ids.append(existing.id)

            # overwrite with new data
            if overwrite:
                if existing.text != result["body"]:
                    # Only overwrite on change
                    existing.sentiment_score = None
                existing.text = result["body"]
                existing.score = result["score"]
        else:
            # generate new db row
            new_comment = RedditComment(
                reddit_id=result["id"],
                text=result["body"],
                posted_at=datetime.datetime.fromtimestamp(result["created_utc"]),
                score=result["score"],
            )

            # assign submission if exists
            existing_submission = RedditSubmission.query.filter_by(
                reddit_id=result["link_id"]
            ).first()
            if existing_submission:
                new_comment.submission = existing_submission

            # assign author
            author = store_reddit_author(username=result["author"])
            new_comment.author = author

            # assign subreddit
            subreddit = store_subreddit(
                name=result["subreddit"], reddit_id=result["subreddit_id"]
            )
            new_comment.subreddit = subreddit

            # update subscribers
            if ("subreddit_subscribers" in result) and (subreddit.subscribers != result["subreddit_subscribers"]):
                subreddit.subscribers = result["subreddit_subscribers"]

            to_add.append(new_comment)

    # add batch
    db.session.add_all(to_add)
    db.session.commit()

    res_ids.extend([added.id for added in to_add])

    # return ids
    return res_ids


def store_reddit_submissions(
    submissions: pmaw.Response, overwrite: bool = True
) -> list[int]:
    """
    Store reddit submissions from a pmaw Response

    :param submissions: pmaw.Response object containing comment dicts
    :param overwrite: overwrite existing submissions if updated information is found, defaults to True
    :return: list of newly-created submissions ids
    """
    if not submissions:
        return []

    res_ids = []
    to_add = []

    for result in submissions:

        existing = RedditSubmission.query.filter_by(reddit_id=result["id"]).first()
        if existing:
            res_ids.append(existing.id)

            # overwrite with new data
            if overwrite:
                if existing.text != result["selftext"]:
                    # Only overwrite on change
                    existing.sentiment_score = None
                existing.text = result["selftext"]
                existing.score = result["score"]
        else:
            # generate new db row
            new_submission = RedditSubmission(
                reddit_id=result["id"],
                permalink=result["permalink"],
                title=result["title"],
                text=result["selftext"],
                type=(
                    RedditSubmissionType.TEXT
                    if result["selftext"]
                    else RedditSubmissionType.OTHER
                ),
                posted_at=datetime.datetime.fromtimestamp(result["created_utc"]),
                score=result["score"],
            )

            # assign author
            author = store_reddit_author(username=result["author"])
            new_submission.author = author

            # assign subreddit
            subreddit = store_subreddit(
                name=result["subreddit"], reddit_id=result["subreddit_id"]
            )
            new_submission.subreddit = subreddit

            to_add.append(new_submission)

    # add batch
    db.session.add_all(to_add)
    db.session.commit()

    res_ids.extend([added.id for added in to_add])

    # return ids
    return res_ids
