from datetime import timedelta, datetime
import json
import os
import re
import yfinance as yf
import yahooquery as yq
import finnhub
import pandas as pd
from flask import Blueprint, request, current_app
from textblob import TextBlob
from trendr.controllers.search_controller import new_search
from trendr.controllers.sentiment_data_point_controller import (
    get_important_posts,
    get_sentiment_scores,
)

from trendr.connectors import twitter_connector
from trendr.connectors import fear_and_greed_connector
from trendr.connectors import coin_gecko_connector as cg
from trendr.connectors import defi_connector as df
from trendr.extensions import db
from trendr.models.reddit_model import RedditSubmission
from trendr.models.search_model import Search, SearchType
from trendr.models.sentiment_model import SentimentDataPoint
from trendr.models.tweet_model import Tweet
from trendr.models.asset_model import Asset
from trendr.models.search_model import SearchType
from trendr.tasks.social.twitter.gather import store_tweet_by_id
from trendr.tasks.social.reddit.gather import store_comments, store_submissions
from trendr.tasks.search import perform_search
from trendr.routes.helpers.json_response import json_response
from trendr.config import FINNHUB_KEY

assets = Blueprint("assets", __name__, url_prefix="/assets")


@assets.route("/fear-greed", methods=["GET"])
def fear_greed():
    """
    Gets the current fear and greed values for stocks and cryptos
    :return: JSON response containing fear and greed values
    """
    crypto_values = fear_and_greed_connector.get_current_crypto_fear_and_greed()
    stock_values = fear_and_greed_connector.get_current_stock_fear_and_greed()

    response_body = {
        "crypto_values": crypto_values,
        "stock_values": stock_values,
    }

    current_app.logger.info("Getting current fear greed values")
    return json_response(response_body, status=200)


@assets.route("/sentiment_values", methods=["POST"])
def sentiment_values():
    current_app.logger.info(f"Getting sentiment data points")

    content = request.get_json()
    params = {"asset_identifier": None, "start_timestamp": None, "end_timestamp": None}
    for param in params:
        if param in content:
            val = content[param]
            if param.endswith("timestamp"):
                val = datetime.fromtimestamp(val)
            params[param] = val
        else:
            current_app.logger.error(f"No {param} given")
            return json_response(
                {"error": f"Parameter '{param}' is required"}, status=400
            )

    current_app.logger.info(
        f"Getting sentiment data points for {params['asset_identifier']} from {params['start_timestamp']} to {params['end_timestamp']}"
    )
    return json_response(
        {
            "data": get_sentiment_scores(
                params["asset_identifier"],
                params["start_timestamp"],
                params["end_timestamp"],
            )
        }
    )


@assets.route("/sentiment_important_posts", methods=["POST"])
def sentiment_important_posts():
    current_app.logger.info(f"Getting sentiment data points")

    content = request.get_json()
    params = {"asset_identifier": None, "timestamp": None}
    for param in params:
        if param in content:
            val = content[param]
            if param.endswith("timestamp"):
                val = datetime.fromtimestamp(val)
            params[param] = val
        else:
            current_app.logger.error(f"No {param} given")
            return json_response(
                {"error": f"Parameter '{param}' is required"}, status=400
            )

    current_app.logger.info(
        f"Getting post urls for {params['asset_identifier']} at {params['timestamp']}"
    )
    return json_response(
        {
            "data": get_important_posts(
                params["asset_identifier"],
                params["timestamp"],
            )
        }
    )
    # asset_identifier, start_time, end_time


@assets.route("/perform_asset_search", methods=["GET"])
def perform_asset_search():
    # TODO: Remove block, it's temporary while we have no assets
    asset = Asset.query.filter_by(identifier="AAPL").first()
    if asset is None:
        asset = Asset(
            identifier="AAPL", reddit_q="AAPL|apple", twitter_q="AAPL OR apple"
        )
        db.session.add(asset)
        db.session.commit()
    else:
        asset.reddit_q = "AAPL"
        asset.twitter_q = "AAPL OR apple"
        db.session.commit()

    search = new_search(asset)
    since = (search.ran_at - timedelta(days=1)).timestamp()
    perform_search.delay(
        asset_id=asset.id,
        search_types=[
            SearchType.TWITTER,
            SearchType.REDDIT_SUBMISSION,
            SearchType.REDDIT_COMMENT,
        ],
        earliest_ts=since,
        search_id=search.id,
    )
    return json_response({"search_id": search.id}, status=200)


@assets.route("/search", methods=["GET"])
def search():
    """
    Searches for assets (stocks and cryptos) matching a query
    :return: JSON response containing basic asset info (symbol, name, etc.)
    """
    query = request.args.get("query")
    if not query:
        current_app.logger.error("No query given")
        return json_response({"error": "Parameter 'query' is required"}, status=400)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(SITE_ROOT, "../connectors", "CoinGeckoCoins.json")
    crypto_list = json.loads(open(json_path, encoding="utf8").read())

    crypto_filtered = [
        v
        for v in crypto_list
        if query.lower() == v["symbol"].lower()
        or query.lower() == v["name"].lower()
        or query.lower() in v["symbol"].lower()
        or query.lower() in v["name"].lower()
    ]

    short_list = sorted(crypto_filtered, key=lambda d: len(d["name"]))

    # print(filtered[0:10])

    stock_filtered = yq.search(query, news_count=0, quotes_count=10)

    response_body = []
    # print (data)

    for item in stock_filtered["quotes"][0:5]:
        if item["typeDisp"] == "Equity" or item["typeDisp"] == "ETF":
            item["typeDisp"] = item.pop("typeDisp").lower()
            if "shortname" in item:
                item["name"] = item.pop("shortname")
            if "longname" in item:
                item["name"] = item.pop("longname")
            item.pop("isYahooFinance")
            item.pop("quoteType")
            item.pop("index")
            item.pop("score")
            response_body.append(item)

    for item in short_list[0:5]:
        item["typeDisp"] = "crypto"
        item["symbol"] = item.pop("symbol").upper()
        response_body.append(item)

    print("\n\nSearch Results for " + query + ":\n")
    print(response_body)

    current_app.logger.info("Getting search results for " + query)

    return json_response(response_body, status=200)


@assets.route("/historic-fear-greed", methods=["GET"])
def historic_fear_greed():
    """
    Gets historic fear and greed values for stocks and cryptos
    :return: JSON response containing fear and greed values
    """
    days = request.args.get("days", default=365, type=int)

    # TODO: Figure out a way to get historic stock values
    crypto_values = fear_and_greed_connector.get_crypto_historic_values(days)
    response_body = {"crypto_values": crypto_values, "stock_values": []}

    current_app.logger.info("Getting historic fear greed values")

    return json_response(response_body, status=200)


@assets.route("/stocks/listed-exchanges", methods=["GET"])
def stocks_listed_exchanges():
    """
    Gets the exchanges that list a stock.
    NOTE: Extremely slow
    :return: JSON response containing official channels
    """
    symbol = request.args.get("symbol")
    if not symbol:
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    symbol = symbol.upper()
    finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    exchangesPath = os.path.join(SITE_ROOT, "../connectors", "FinnhubExchanges.csv")
    df = pd.read_csv(exchangesPath)

    exchangeList = []
    try:
        for index, contents in df.iterrows():
            exchangeCode = contents["code"]
            for c in finnhub_client.stock_symbols(exchangeCode):
                if c["symbol"] == symbol:
                    exchangeList.append(contents["name"])
    except:
        return json_response("Time out", status=500)
    return json_response(exchangeList, status=200)


@assets.route("/crypto/stats", methods=["GET"])
def crypto_stats():
    """
    Gets general statistics for cryptos
    :return: JSON response containing crypto statistics
    """
    id = request.args.get("id")
    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)

    response_body = cg.get_coin_live_stats(id)
    current_app.logger.info("Getting crypto stats for " + id)
    return json_response(response_body, status=200)


@assets.route("/stock/stats", methods=["GET"])
def stock_stats():
    """
    Gets general statistics for stocks and etf
    :return: JSON response containing stock/etf statistics
    """
    symbol = request.args.get("symbol")
    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker or not hasattr(asset_ticker, "info"):
        current_app.logger.error("Couldn't retrieve statistics for " + symbol)
        return json_response({"error": "Couldn't retrieve statistics"}, status=500)

    response_body = asset_ticker.info
    current_app.logger.info("Getting stock stats for " + symbol)
    return json_response(response_body, status=200)


@assets.route("/crypto/eth-address", methods=["GET"])
def crypto_eth_address():
    id = request.args.get("id")
    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)

    response_body = cg.get_id_eth_address(id)
    return json_response(response_body, status=200)


@assets.route("/token/info", methods=["GET"])
def token_info():
    address = request.args.get("address")
    if not address:
        current_app.logger.error("No address given")
        return json_response({"error": "Parameter 'address' is required"}, status=400)

    response_body = df.get_token_info(address)
    return json_response(response_body, status=200)


@assets.route("/token/top-holders", methods=["GET"])
def token_top_holders():
    address = request.args.get("address")
    if not address:
        current_app.logger.error("No address given")
        return json_response({"error": "Parameter 'address' is required"}, status=400)

    response_body = df.get_top_token_holders(address, 20)
    return json_response(response_body, status=200)


@assets.route("/crypto/price-history", methods=["GET"])
def crypto_price_history():
    id = request.args.get("id")
    days = request.args.get("days")
    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)
    if not days:
        current_app.logger.error("No days given")
        return json_response({"error": "Parameter 'days' is required"}, status=400)

    response_body = cg.get_historic_prices(id, days)
    current_app.logger.info(
        "Getting crypto price history for " + id + " over " + days + " days"
    )
    return json_response(response_body, status=200)


@assets.route("/crypto/volume-history", methods=["GET"])
def crypto_volume_history():
    id = request.args.get("id")
    days = request.args.get("days")
    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)
    if not days:
        current_app.logger.error("No days given")
        return json_response({"error": "Parameter 'days' is required"}, status=400)

    response_body = cg.get_historic_volumes(id, days)
    current_app.logger.info(
        "Getting crypto volume history for " + id + " over " + days + " days"
    )
    return json_response(response_body, status=200)


@assets.route("/stock/history", methods=["GET"])
def stock_history():
    """
    Gets historical data for an asset (stock or crypto)
    :return: JSON response containing historical data
    """
    period = request.args.get("period")
    symbol = request.args.get("symbol")
    if not period:
        current_app.logger.error("No period given")
        return json_response({"error": "Parameter 'period' is required"}, status=400)
    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    period_to_interval_map = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d",
    }

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker:
        current_app.logger.error("Couldn't retrieve history for " + symbol)
        return json_response({"error": "Couldn't retrieve history"}, status=500)

    current_app.logger.info(
        "Getting stock pirce and volume history for " + symbol + " over " + period
    )
    # TODO: Figure out how to return this like the other endpoints w/o breaking the frontend
    return asset_ticker.history(
        period=period,
        interval=period_to_interval_map.get(period),
        prepost="True",
        actions="False",
    ).to_json()


@assets.route("/twitter_sentiment", methods=["GET"])
def twitter_sentiment():
    """
    Gets twitter sentiment for an asset (stock or crypto)
    :return: JSON response containing twitter sentiment
    """
    symbol = request.args.get("symbol")
    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    response_body = []
    results = twitter_connector.get_tweets_mentioning_asset(symbol)
    for result in results:
        text_clean = re.sub(r"@[A-Za-z0-9]+", "", result.text)
        text_clean = re.sub(r"#", "", text_clean)
        text_clean = re.sub("\n", " ", text_clean)

        # using this will take a lot longer than TextBlob's default analyzer
        # blob = TextBlob(result.text, analyzer=NaiveBayesAnalyzer())

        blob = TextBlob(text_clean)

        # first number: polarity (-1.0 = very negative, 0 = neutral, 1.0 = very positive)
        # second number: subjectivity (0.0 = objective, 1.0 = subjective)
        response_body.append([text_clean, blob.sentiment])

    current_app.logger.info("Getting twitter sentiment data for " + symbol)
    return json_response(response_body, status=200)


@assets.route("/reddit_sentiment", methods=["GET"])
def reddit_sentiment():
    """
    Gets reddit sentiment for an asset (stock or crypto)
    :return: JSON response containing reddit sentiment
    """
    res_1 = store_tweet_by_id.delay(tweet_id=1450846775221399566)
    res_2 = store_submissions.delay(keywords=["apple"], limit=50)
    res_3 = store_comments.delay(keywords=["apple"], limit=50)

    response_body = [
        res_1.get(timeout=100),
        res_2.get(timeout=100),
        res_3.get(timeout=100),
    ]
    current_app.logger.info("Getting reddit sentiment")
    return json_response(response_body, status=200)


@assets.route("/tweet-summary/<asset_identifier>", methods=["GET"])
def tweet_summary(asset_identifier):
    """
    Generates statistics related to the types of users tweeting about an asset
    :param asset_identifier: The asset identifier (AAPL, BTC) to generate a tweet summary for
    :return: JSON response containing tweet summary for the requested asset
    """
    summary_data = twitter_connector.twitter_accounts_mentioning_asset_summary(
        asset_identifier
    )
    current_app.logger.info("Getting twitter user statistics for " + asset_identifier)
    return json_response(summary_data, status=200)
