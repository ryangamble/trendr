import random
import string


def create_random_string(num_char: int) -> str:
    """
    Returns a random string of length num_char

    :param num_char: The number of characters to use
    :return: The random string
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(num_char))
