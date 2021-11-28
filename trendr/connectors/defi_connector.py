"""
Ethplrer API Documentation: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
Uniswap API documenation: https://docs.uniswap.org/protocol/V2/reference/API/overview
"""
import json
import requests

from trendr.connectors.coin_gecko_connector import get_symbol_eth_address
from trendr.config import ETHPLORERE_KEY

ETHPLORER_URL = "https://api.ethplorer.io/"
UNISWAP_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"


def get_top_token_holders(token_address, number):
    """
    :param token_address: Contract address of the token on the eth chain
    :param number: How many of the top holders are returned(max is 100)
    :return: the top holders in a dictionary
    """
    path = (
        ETHPLORER_URL
        + "getTopTokenHolders/"
        + str(token_address)
        + "?apiKey="
        + ETHPLORERE_KEY
        + "&limit="
        + str(number)
    )
    response = requests.get(path)
    return response.json()["holders"]


def volume_history(token_address):
    """
    :param token_address: Contract address of the token on the eth chain
    :return: the volume of the token across available data
    """
    path = (
        ETHPLORER_URL
        + "getTokenPriceHistoryGrouped/"
        + str(token_address)
        + "?apiKey="
        + ETHPLORERE_KEY
    )
    response = requests.get(path)
    return response.json()


def get_token_info(token_address):
    """
    :param token_address: Contract address of the token on the eth chain
    :return: a json of token data from ethplorer API
    """
    path = (
        ETHPLORER_URL
        + "getTokenInfo/"
        + str(token_address)
        + "?apiKey="
        + ETHPLORERE_KEY
    )
    response = requests.get(path)
    return response.json()


def get_symbol_address(symbol):
    """
    :param symbol: ticker of the token
    :return: the eth address of a token. If not available, returns None
    """
    address = get_symbol_eth_address(symbol)
    return address if address else None


def get_token_liquidity(token_address):
    try:
        single_token_liquidity_query = """
        {{
        token(id: "{0}"){{
        name
        symbol
        tradeVolumeUSD
        totalLiquidity
        }}
        }}
        """
        response = requests.post(
            UNISWAP_URL,
            json={"query": single_token_liquidity_query.format(token_address)},
        )
        response = json.loads(response.text)
        liquidity_total = response["data"]["token"]["totalLiquidity"]
        return float("{0:.2f}".format(float(liquidity_total)))
    except:
        return None


class TokenInfo:
    """
    This class is a wrapper that combines Defi. Just supplying the symbol of a token
    to the constructor will fill all the data of in an object.
    """

    def __init__(self, symbol: str, number: int = 100):
        """
        creates an object for the token and will fill all its info at creation.
        :param symbol: ticker of the crypto currency token0
        :param number: the number of top holders to return(max is 100)
        """
        if number > 100:
            number = 100
        address = get_symbol_address(symbol)
        token_info = get_token_info(address)
        self.attributes = {
            "address": address,
            "name": token_info["name"],
            "available_supply": "{0:.2f}".format(
                float(token_info["price"]["availableSupply"])
            ),
            # 'totalSupply': info['totalSupply'],
            "holder_count": token_info["holdersCount"],
            "official_website": token_info["website"],
            "official_telegram": token_info["telegram"],
            "official_twitter": token_info["twitter"],
            "volume_24h": str("$")
            + "{0:.2f}".format(float(token_info["price"]["volume24h"])),
            # 'vol_diff_1': info['price']["volDiff1"],
            "liquidity": str("$") + str(get_token_liquidity(address)),
        }
        holder_info = self.get_top_token_holders(address, number)
        self.top_100_holders_list = holder_info[0]
        self.top_100_ownership = str("%") + "{0:.2f}".format(float(holder_info[1]))

    @staticmethod
    def get_top_token_holders(token_address, number):
        """
        :param token_address: The ETH address of the token
        :param number: How many of the top holders are returned(max is 100)
        :return: two values, a list of lists, where each list has the number of tokens of holder,
        and the total ownership of the total supply. The second value is how many of the total supply
        this number of holders own.
        """
        holders = get_top_token_holders(token_address, number)
        top_100_total_ownership = 0
        top_100_holder_list = []
        for holder in holders:
            top_100_total_ownership += float(holder["share"])
            top_100_holder_list.append(
                [holder["balance"], str("%") + str(holder["share"])]
            )
        # print(type(Top100HoldersList[0][0]))
        return top_100_holder_list, top_100_total_ownership

    def print_summary(self):
        """
        prints a summary of all the information of this token object.
        """
        for key in self.attributes:
            print(key + ":" + str(self.attributes[key]))
        self.print_holder_summary()

    def print_holder_summary(self):
        """
        prints a summary of the top holders of this token object
        """
        print("Top", len(self.top_100_holders_list), "holders:")
        for holder in self.top_100_holders_list:
            print(holder)
        print(
            "Total Ownership of Top",
            len(self.top_100_holders_list),
            ":",
            self.top_100_ownership,
        )

    def get_address(self):
        """
        returns the token contract address of this token object
        """
        return self.attributes["address"]
