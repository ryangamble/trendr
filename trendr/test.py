from trendr.connectors import twitter_connector
from extensions import db


# api = twitter_connector.auth_to_api("Z9O6ST99noLo6n4e1B5Gi1EL6", "8XT3XvL6pWlX5pOnBxZGTOEPuxUXHRlg8ezIa0Hx1Kq9TlJc6c")
# tweets = twitter_connector.get_tweet_by_id("1440481481755824144", api=api)
# print(tweets)
db.drop_all()


# @users.route("/follow-asset/<user_id>", methods=["PUT"])
# def add_followed_asset_to_user(user_id):
#     """
#     Adds a followed asset association to a user
#     :param user_id: The database user id to add a followed asset to
#     :return: Response 200 if successful
#     """
#     pass
#
#
# @users.route("/unfollow-asset/<user_id>", methods=["PUT"])
# def remove_followed_asset_from_user(user_id):
#     """
#     Removes a followed asset association from a user
#     :param user_id: The database user id to remove a followed asset from
#     :return: Response 200 if successful
#     """
#     pass
#
# def add_followed_asset(user_id: int, asset_identifier: str) -> bool:
#     """
#     Adds a followed asset association to a user
#     :param user_id: The database user id to add a followed asset to
#     :param asset_identifier: The database user id to add a followed asset to
#     :return: True if successful
#     """
#     asset = Asset.query.filter(Asset.identifier == asset_identifier).one()
#     if asset:
#         asset_id = asset.id
#     else:
#         new_asset = Asset(identifier=asset_identifier)
#         asset_id = new_asset.id
#     user_asset_association.insert().values(user_id=user_id, asset_id=asset_id)