from datetime import timedelta, datetime
import json
import os
import yfinance as yf
import yahooquery as yq
import finnhub
import pandas as pd

from flask import Blueprint, request, current_app, redirect
from trendr.controllers.search_controller import new_search
from trendr.controllers.sentiment_data_point_controller import (
    get_important_posts,
    get_sentiment_scores,
)
from trendr.connectors import (
    twitter_connector,
    reddit_connector,
    fear_and_greed_connector,
    coin_gecko_connector as cg,
    defi_connector as df,
)
from trendr.extensions import db
from trendr.models.asset_model import Asset
from trendr.models.search_model import SearchType, Search
from trendr.models.tweet_model import Tweet
from trendr.models.reddit_model import RedditComment
from trendr.tasks.social.twitter.gather import store_tweet_by_id
from trendr.tasks.social.reddit.gather import store_comments, store_submissions
from trendr.tasks.search import perform_search
from trendr.routes.helpers.json_response import json_response
from trendr.config import FINNHUB_KEY
from trendr.tasks.symbols import populate_database

assets = Blueprint("assets", __name__, url_prefix="/assets")


@assets.route("/populate_assets", methods=["POST"])
def populate_assets():
    message = populate_database.populate_database_with_symbols()
    return json_response({"Result": message}, status=200)


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


@assets.route("/sentiment_values", methods=["GET"])
def sentiment_values():
    current_app.logger.info(f"Getting sentiment data points")

    content = request.args
    params = {"asset_identifier": None, "start_timestamp": None, "end_timestamp": None}
    for param in params:
        if param in content:
            val = content[param]
            if param.endswith("timestamp"):
                val = datetime.fromtimestamp(int(val))
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


@assets.route("/sentiment_important_posts", methods=["GET"])
def sentiment_important_posts():
    current_app.logger.info(f"Getting sentiment data points")

    content = request.args
    params = {"asset_identifier": None, "timestamp": None}
    for param in params:
        if param in content:
            val = content[param]
            if param.endswith("timestamp"):
                val = datetime.fromtimestamp(int(val))
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
    symbol = request.args.get("symbol")
    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    asset = Asset.query.filter_by(identifier=symbol).first()
    if not asset:
        current_app.logger.error("Asset not supported")
        return json_response({"error": f"Asset {symbol} not supported"}, status=400)

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
    currency = request.args.get("currency")

    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)
    if not currency:
        currency = "usd"
    response_body = cg.get_coin_live_stats(id, currency)
    current_app.logger.info("Getting crypto stats for " + id)
    return json_response(response_body, status=200)


@assets.route("/stock/stats", methods=["GET"])
def stock_stats():
    """
    Gets general statistics for stocks and etf
    :return: JSON response containing stock/etf statistics
    """
    currency_affected_values = [
        "operatingCashflow",
        "ebitda",
        "targetLowPrice",
        "grossProfits",
        "freeCashflow",
        "targetMedianPrice",
        "currentPrice",
        "targetMeanPrice",
        "debtToEquity",
        "targetHighPrice",
        "totalCash",
        "totalDebt",
        "totalRevenue",
        "totalCashPerShare",
        "revenuePerShare",
        "heldPercentInstitutions",
        "netIncomeToCommon",
        "enterpriseValue",
        "sharesShortPriorMonth",
        "previousClose",
        "regularMarketOpen",
        "twoHundredDayAverage",
        "volume24Hr",
        "regularMarketDayHigh",
        "navPrice",
        "averageDailyVolume10Day",
        "regularMarketPreviousClose",
        "fiftyDayAverage",
        "open",
        "averageVolume10days",
        "regularMarketDayLow",
        "regularMarketVolume",
        "marketCap",
        "averageVolume",
        "dayLow",
        "ask",
        "volume",
        "fiftyTwoWeekHigh",
        "fiftyTwoWeekLow",
        "bid",
        "dayHigh",
        "regularMarketPrice",
    ]
    symbol = request.args.get("symbol")
    currency = request.args.get("currency")

    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    multiplier = 1
    if currency == None or currency == "USD":
        pass
    else:
        currency = currency.upper()
        # check for a currency
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        currencies_path = os.path.join(
            SITE_ROOT, "../routes/helpers", "YahooCurrencies.csv"
        )
        df_currencies = pd.read_csv(currencies_path)
        currency_symbol = ""
        for i in range(len(df_currencies)):
            y_symbol = currency + "/USD"
            if df_currencies.iloc[i]["Name"] == y_symbol:
                currency_symbol = df_currencies.iloc[i]["Ticker"]
                break

        if len(currency_symbol) == 0:
            current_app.logger.error("Wrong Currency provided")
            return json_response(
                {"error": "Parameter 'curreny', Wrong Currency provided"}, status=400
            )

        curr_ticker = yf.Ticker(currency_symbol)
        hist = curr_ticker.history(period="1d")
        multiplier = float(hist.iloc[-1]["Open"])

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker or not hasattr(asset_ticker, "info"):
        current_app.logger.error("Couldn't retrieve statistics for " + symbol)
        return json_response({"error": "Couldn't retrieve statistics"}, status=500)

    response_body = asset_ticker.info

    if type(multiplier) == int:
        # it's in U.S dollar, don;t change anything
        pass
    else:
        response_body["financialCurrency"] = currency
        response_body["currency"] = currency
        for term in currency_affected_values:
            if term in response_body and response_body[term] != None:
                response_body[term] = response_body[term] / multiplier

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
    currency = request.args.get("currency")
    if not id:
        current_app.logger.error("No id given")
        return json_response({"error": "Parameter 'id' is required"}, status=400)
    if not days:
        current_app.logger.error("No days given")
        return json_response({"error": "Parameter 'days' is required"}, status=400)

    response_body = cg.get_historic_prices(id, days, currency)
    if response_body == None:
        return json_response(
            {"error": "Parameter 'currency' value is unsupported"}, status=400
        )

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
    currency = request.args.get("currency")

    multiplier = 1
    if currency == None or currency == "USD":
        pass
    else:
        # check for a currency
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        currencies_path = os.path.join(
            SITE_ROOT, "../routes/helpers", "YahooCurrencies.csv"
        )
        df_currencies = pd.read_csv(currencies_path)
        currency_symbol = ""
        for i in range(len(df_currencies)):
            y_symbol = currency + "/USD"
            if df_currencies.iloc[i]["Name"] == y_symbol:
                currency_symbol = df_currencies.iloc[i]["Ticker"]
                break

        if len(currency_symbol) == 0:
            current_app.logger.error("Wrong Currency provided")
            return json_response(
                {"error": "Parameter 'curreny',Wrong Currency provided"}, status=400
            )

        curr_ticker = yf.Ticker(currency_symbol)
        hist = curr_ticker.history(period="1d")
        multiplier = float(hist.iloc[-1]["Open"])

    if not period:
        current_app.logger.error("Wrong Currency symbol")
        return json_response(
            {"error": "Parameter 'symbol' is unsuppoerted"}, status=400
        )
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
    history_df = asset_ticker.history(
        period=period,
        interval=period_to_interval_map.get(period),
        prepost="True",
        actions="False",
    )
    if type(multiplier) == int:
        pass
    else:
        # convert prices to this currency
        history_df["Open"] = history_df["Open"] / multiplier
        history_df["High"] = history_df["High"] / multiplier
        history_df["Low"] = history_df["Low"] / multiplier
        history_df["Close"] = history_df["Close"] / multiplier
        history_df["Volume"] = history_df["Volume"] / multiplier

    return history_df.to_json()


@assets.route("/reddit_mentions_count", methods=["GET"])
def reddit_mentions_count():
    """
    Gets a dictionary with the count data(starting hour: count(ex. "2021/1/1:17" : 123)
    for each hour. The number of hours is based on the count, with a max of 2000 posts.
    symbol can be any keyword. ex. BTC or Bitcoin.
    """
    symbol = request.args.get("symbol")

    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    # res = reddit_connector.get_mentions_count(symbol='Bitcoin')
    res = reddit_connector.reddit_count_mentioning_asset(asset_identifier=symbol)
    return json_response(res, status=200)


@assets.route("/twitter_sentiment", methods=["GET"])
def twitter_sentiment():
    """
    Gets twitter sentiment for an asset (stock or crypto)
    :return: JSON response containing twitter sentiment
    """
    query = request.args.get("query")
    if not query:
        current_app.logger.error("No query given")
        return json_response({"error": "Parameter 'query' is required"}, status=400)

    asset = Asset.query.filter_by(identifier=query).first()
    if not asset:
        current_app.logger.error("Asset not supported")
        return json_response({"error": f"Asset {query} not supported"}, status=400)

    # If the last two searches failed to return any tweets, return error
    recent_searches = (
        db.session.query(Search)
        .filter(Search.asset_id == asset.id)
        .order_by(Search.ran_at.desc())
        .limit(2)
    )

    failed_searches = 0
    for search in recent_searches:
        if search.twitter_sentiment == None:
            failed_searches += 1

    if failed_searches >= 2:
        current_app.logger.error("Cannot get Twitter sentiment for " + query)
        return json_response(
            {"error": "Cannot get Twitter sentiment for " + query}, status=400
        )

    # Gets the most recent search for given keyword
    most_recent_search_id = (
        db.session.query(Search.id)
        .filter(Search.search_string == query)
        .order_by(Search.ran_at.desc())
        .limit(1)
        .all()
    )

    if not most_recent_search_id:
        current_app.logger.warning("No Tweets for " + query)
        current_app.logger.info(
            "Sending request to get Twitter sentiment data for " + query
        )
        return redirect("/assets/perform-asset-search?query=" + query)

    # Gets the Tweets of the given search id
    results = (
        db.session.query(Tweet)
        .select_from(Search)
        .join(Search.tweets)
        .filter(Search.id == most_recent_search_id[0][0])
        .all()
    )

    if len(results) == 0:
        current_app.logger.warning("No Tweets for most recent search of " + query)
        current_app.logger.info(
            "Sending request to get Twitter sentiment data for " + query
        )
        return redirect("/assets/perform-asset-search?query=" + query)

    response_body = []
    for result in results:
        response_body.append([result.text, result.polarity, result.subjectivity])

    current_app.logger.info("Getting twitter sentiment data for " + query)
    return json_response(response_body, status=200)


@assets.route("/twitter_mentions_count", methods=["GET"])
def twitter_mentions_count():
    """
    Gets a list with the count data(start, end, tweet_count) for each hour for the previous 7 days.
    symbol can be any keyword. ex. BTC or Bitcoin.
    """
    symbol = request.args.get("symbol")

    if not symbol:
        current_app.logger.error("No symbol given")
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    res = twitter_connector.tweet_count_mentioning_asset(asset_identifier=symbol)
    return json_response(res, status=200)


@assets.route("/reddit_sentiment", methods=["GET"])
def reddit_sentiment():
    """
    Gets reddit sentiment for an asset (stock or crypto)
    :return: JSON response containing reddit sentiment
    """

    query = request.args.get("query")
    if not query:
        current_app.logger.error("No query given")
        return json_response({"error": "Parameter 'query' is required"}, status=400)

    asset = Asset.query.filter_by(identifier=query).first()
    if not asset:
        current_app.logger.error("Asset not supported")
        return json_response({"error": f"Asset {query} not supported"}, status=400)

    # If the last two searches failed to return any comments, return error
    recent_searches = (
        db.session.query(Search)
        .filter(Search.asset_id == asset.id)
        .order_by(Search.ran_at.desc())
        .limit(2)
    )

    failed_searches = 0
    for search in recent_searches:
        if search.reddit_sentiment == None:
            failed_searches += 1

    if failed_searches >= 2:
        current_app.logger.error("Cannot get Reddit sentiment for " + query)
        return json_response(
            {"error": "Cannot get Reddit sentiment for " + query}, status=400
        )

    # Gets the most recent search for given keyword
    most_recent_search_id = (
        db.session.query(Search.id)
        .filter(Search.search_string == query)
        .order_by(Search.ran_at.desc())
        .filter(Search.reddit_sentiment != None)
        .limit(1)
        .all()
    )

    if not most_recent_search_id:
        current_app.logger.warning("No Reddit comments for " + query)
        current_app.logger.info(
            "Sending request to get Reddit sentiment data for " + query
        )
        return redirect("/assets/perform-asset-search?query=" + query)

    # Gets the reddit submissions of the given search id
    results = (
        db.session.query(RedditComment)
        .select_from(Search)
        .join(Search.reddit_comments)
        .filter(Search.id == most_recent_search_id[0][0])
        .all()
    )

    if len(results) == 0:
        current_app.logger.warning(
            "No Reddit comments for most recent search of " + query
        )
        current_app.logger.info(
            "Sending request to get Reddit sentiment data for " + query
        )
        return redirect("/assets/perform-asset-search?query=" + query)

    response_body = []
    for result in results:
        response_body.append([result.text, result.polarity, result.subjectivity])

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
