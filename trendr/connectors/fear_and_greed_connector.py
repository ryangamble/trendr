import requests
from datetime import datetime


def convert_time(unix_time) -> str:
    """
    Returns an RFC 1123 time string from a unix timestamp
    :param unix_time: time unix_time format
    :return: time as a datetime object
    """
    return datetime.utcfromtimestamp(unix_time).strftime("%a, %d %b %Y %H:%M:%S GMT")


def get_current_crypto_fear_and_greed():
    """
    :return: the current value of the fear and greed index with its representation
    """
    response = requests.get("https://api.alternative.me/fng/?limit=1")
    values = {
        "value": response.json()["data"][0]["value"],
        "valueText": response.json()["data"][0]["value_classification"]
        # 'timestamp': convert_time(float(response.json()['data'][0]['timestamp']))
    }
    return values


def get_current_stock_fear_and_greed():
    """
    :return: the stock market current fear and greed index value
    """
    url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
    headers = {
        "x-rapidapi-host": "fear-and-greed-index.p.rapidapi.com",
        "x-rapidapi-key": "b5ba7967dcmsh69f36a951adbe11p1d2ff4jsnabfb5a0d224e",
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()["fgi"]["now"]


def get_crypto_historic_values(days: int = 365):
    """
    :param days: how many days of crypto fear and index values are requested
    :return: historic values of crypto fear and greed index up to 2018
    """
    if days == 0:
        days = 1
    response = requests.get("https://api.alternative.me/fng/?limit=" + str(days))
    value_list = []
    for stamp in response.json()["data"]:
        values = {
            "value": stamp["value"],
            "value_classification": stamp["value_classification"],
            "timestamp": convert_time(float(stamp["timestamp"])),
        }
        value_list.append(values)

    return value_list


def print_historic_values(values: []):
    for value in values:
        print(value)
