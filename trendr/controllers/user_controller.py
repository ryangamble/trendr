from trendr.models.user_model import UserModel


def create_user(name: str, password: str):
    """
    Creates a user in the database

    :param name: The name of the new user
    :param password: The password of the new user
    :return: UserModel
    """
    new_user = UserModel
    UserModel.name = name
    UserModel.password = password
    return new_user
