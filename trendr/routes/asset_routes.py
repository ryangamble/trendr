import json
import os
import re
import yfinance as yf
import yahooquery as yq

from flask import Blueprint, request
from textblob import TextBlob

from trendr.connectors import twitter_connector
from trendr.connectors import fear_and_greed_connector
from trendr.connectors import coin_gecko_connector
from trendr.tasks.social.twitter.gather import store_tweet_by_id
from trendr.tasks.social.reddit.gather import (
    store_comments,
    store_submissions
)
from trendr.routes.helpers.json_response import json_response

assets = Blueprint("assets", __name__, url_prefix="/assets")


@assets.route('/fear-greed', methods=['GET'])
def fear_greed():
    """
    Gets the current fear and greed values for stocks and cryptos
    :return: JSON response containing fear and greed values
    """
    crypto_values = fear_and_greed_connector.get_current_crypto_fear_and_greed()
    stock_values = fear_and_greed_connector.get_current_stock_fear_and_greed()

    response_body = {
        'crypto_values': crypto_values,
        'stock_values': stock_values
    }
    return json_response(response_body, status=200)


@assets.route('/cryptos/historic-fear-greed', methods=['GET'])
def cryptos_historic_fear_greed():
    """
    Gets historic fear and greed values for cryptos
    :return: JSON response containing fear and greed values
    """
    days = request.args.get('days', default=365, type=int)

    response_body = fear_and_greed_connector.get_crypto_historic_values(days)
    return json_response(response_body, status=200)


@assets.route('/stocks/official-channels', methods=['GET'])
def stock_official_channels():
    """
    Gets the official channels (website) of a stock
    :return: JSON response containing official channels
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker or not hasattr(asset_ticker, "info") or "website" not in asset_ticker.info:
        return json_response({"error": "Couldn't retrieve official channels"}, status=500)

    response_body = {
        'website': asset_ticker.info['website']
    }
    return json_response(response_body, status=200)


@assets.route('/cryptos/official-channels', methods=['GET'])
def cryptos_official_channels():
    """
    Gets the official channels (homepage, socials, etc.) of a crypto
    :return: JSON response containing official channels
    """
    name = request.args.get('name')
    if not name:
        return json_response({"error": "Parameter 'name' is required"}, status=400)

    response_body = coin_gecko_connector.get_coin_links(name)
    return json_response(response_body, status=200)


@assets.route('/search', methods=['GET'])
def search():
    """
    Searches for assets (stocks and cryptos) matching a query
    :return: JSON response containing basic asset info (symbol, name, etc.)
    """
    query = request.args.get("query")
    if not query:
        return json_response({"error": "Parameter 'query' is required"}, status=400)

    response_body = []

    # TODO: Load valid coins from the assets table and delete CoinGeckoCoins.json
    base_path = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(base_path, '../connectors', 'CoinGeckoCoins.json')
    crypto_list = json.loads(open(json_path).read())
    crypto_filtered = [
        v for v in crypto_list
        if query.lower() == v['symbol'].lower() or query.lower() == v['name'].lower()
        or query.lower() in v['symbol'].lower() or query.lower() in v['name'].lower()
    ]
    crypto_filtered = sorted(crypto_filtered, key=lambda d: len(d['name']))
    for item in crypto_filtered[0:5]:
        item['typeDisp'] = 'crypto'
        item['symbol'] = item.pop('symbol').upper()
        response_body.append(item)

    stock_filtered = yq.search(query, news_count=0, quotes_count=10)
    for item in stock_filtered['quotes'][0:5]:
        if item['typeDisp'] == 'Equity' or item['typeDisp'] == 'ETF':
            item['typeDisp'] = item.pop('typeDisp').lower()
            if 'shortname' in item:
                item['name'] = item.pop('shortname')
            if 'longname' in item:
                item['name'] = item.pop('longname')
            item.pop('isYahooFinance')
            item.pop('quoteType')
            item.pop('index')
            item.pop('score')
            response_body.append(item)

    return json_response(response_body, status=200)


@assets.route("/stats", methods=["GET"])
def stats():
    """
    Gets general statistics for an asset (stock or crypto)
    :return: JSON response containing asset statistics
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker or not hasattr(asset_ticker, "info"):
        return json_response({"error": "Couldn't retrieve statistics"}, status=500)

    response_body = asset_ticker.info
    return json_response(response_body, status=200)


@assets.route("/history", methods=["GET"])
def history():
    """
    Gets historical data for an asset (stock or crypto)
    :return: JSON response containing historical data
    """
    period = request.args.get('period')
    symbol = request.args.get('symbol')
    if not period:
        return json_response({"error": "Parameter 'period' is required"}, status=400)
    if not symbol:
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    period_to_interval_map = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }

    asset_ticker = yf.Ticker(symbol)
    if not asset_ticker:
        return json_response({"error": "Couldn't retrieve history"}, status=500)

    response_body = asset_ticker.history(
        period=period, interval=period_to_interval_map.get(period), prepost="True", actions="False"
    ).to_json()
    return json_response(response_body, status=200)


@assets.route("/twitter_sentiment", methods=["GET"])
def twitter_sentiment():
    """
    Gets twitter sentiment for an asset (stock or crypto)
    :return: JSON response containing twitter sentiment
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return json_response({"error": "Parameter 'symbol' is required"}, status=400)

    response_body = []
    results = twitter_connector.get_tweets_mentioning_asset(symbol)
    for result in results:
        text_clean = re.sub(r'@[A-Za-z0-9]+', '', result.text)
        text_clean = re.sub(r'#', '', text_clean)
        text_clean = re.sub('\n', ' ', text_clean)

        # using this will take a lot longer than TextBlob's default analyzer
        # blob = TextBlob(result.text, analyzer=NaiveBayesAnalyzer())

        blob = TextBlob(text_clean)

        # first number: polarity (-1.0 = very negative, 0 = neutral, 1.0 = very positive)
        # second number: subjectivity (0.0 = objective, 1.0 = subjective)
        response_body.append([text_clean, blob.sentiment])

    return json_response(response_body, status=200)


@assets.route("/reddit_sentiment", methods=["GET"])
def reddit_sentiment_route():
    """
    Gets reddit sentiment for an asset (stock or crypto)
    :return: JSON response containing reddit sentiment
    """
    res_1 = store_tweet_by_id.delay(tweet_id=1450846775221399566)
    res_2 = store_submissions.delay(keywords=["apple"], limit=50)
    res_3 = store_comments.delay(keywords=["apple"], limit=50)

    response_body = [res_1.get(timeout=100), res_2.get(timeout=100), res_3.get(timeout=100)]
    return json_response(response_body, status=200)
