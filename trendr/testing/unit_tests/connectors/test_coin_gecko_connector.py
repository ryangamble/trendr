import pytest
from trendr.connectors import coin_gecko_connector


def test_convert_time(date_list):
    """
    Returns a list of RFC 1123 time strings from a list of unix timestamp
    :param date_list: a list of unix times
    :return: a python dataframe from this unix time
    """
    pass

def test_get_historic_prices(coin, days):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :return: a list of prices
    """
    pass


def test_get_historic_volumes(coin, days):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :returns a list of volumes
    """
    pass


def test_print_historic_price(dict_of_prices):
    """
    prints the provided dictionary
    :param dict_of_prices: A dictionary of the time and price
    """
    pass

def test_get_market_cap_history(coin: str, days: int = 3):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :return: a dictionary of the coins market cap and time of capture
    """
    pass


def test_get_coin_live_stats(coin):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :return: current live stats of a coin as a dictionary
    """
    pass


def test_convert_symbol_to_id(symbol):
    """
    :param symbol: The ticker of a coin/token
    :return: if this symbl exists, we return the corresponding ID used by coingecko API
    """
    pass


def test_get_symbol_eth_address(symbol):
    """
    :param symbol: The ticker of a coin/token
    :return: the eth token contract address if it exists, or None of it's not an ETH token
    """
    pass


def test_get_id_eth_address(id):
    """
    :param id: The id of a coin/token
    :returns the eth token contract address if it exists, or None of it's not an ETH token
    """
    pass

def test_get_coin_links(coin_id):
    """
    :param coin_id: The ID of the coin, as stored in coin gecko coins json file
    :return: a dictionary with the available links for the passed coin
    """
    pass