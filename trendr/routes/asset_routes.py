from flask import Blueprint, request, jsonify
import yfinance as yf
import yahooquery as yq
from textblob import TextBlob
import re

from trendr.connectors import twitter_connector
from trendr.connectors import fear_and_greed_connector
from trendr.tasks.reddit import reddit_sentiment
from trendr.tasks.social.twitter.gather import (
    store_tweets_mentioning_asset,
    store_tweet_by_id,
)
from trendr.tasks.social.reddit.gather import (
    store_comments,
    store_submissions,
    store_submissions_by_id,
    store_comments_by_id,
)
from .helpers.json_response import json_response

assets = Blueprint("assets", __name__, url_prefix="/assets")


@assets.route('/fear-greed', methods=['GET'])
def fear_and_greed():
    crypto_values = fear_and_greed_connector.get_current_crypto_fear_and_greed()
    stock_values = fear_and_greed_connector.get_current_stock_fear_and_greed()
    data = {'crypto_values': crypto_values, 'stock_values': stock_values}
    return jsonify(data)


@assets.route('/historic-fear-greed', methods=['GET'])
def historic_fear_and_greed_crypto():
    content = request.get_json()
    if content and 'days' in content:
        days = int(content['days'])
    else:
        days = 365
    values = fear_and_greed_connector.get_crypto_historic_values(days)
    return jsonify(values)


@assets.route('/search', methods=['POST'])
def search():
    content = request.get_json()
    data = yq.search(content['query'], news_count=0, quotes_count=10)
    return jsonify(data)


@assets.route('/sp500', methods=['GET'])
def sp_500():
    content = request.get_json()
    print("\nfetching history market data for S&P500" + "\n")

    stock = yf.Ticker('GSPC')
    p = content['period']

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }
    return stock.history(period=p, interval=period_to_interval.get(p), prepost="True", actions="False").to_json()


@assets.route('/gdow', methods=['GET'])
def gdow():
    content = request.get_json()
    print("\nfetching history market data for The Global Dow" + "\n")

    stock = yf.Ticker('GDOW')
    p = content['period']

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }
    return stock.history(period=p, interval=period_to_interval.get(p), prepost="True", actions="False").to_json()


@assets.route('/stats', methods=['POST'])
def stats():
    content = request.get_json()

    print("\nfetching general stats for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)


@assets.route("/history", methods=["POST"])
def history():
    content = request.get_json()

    print("\nfetching history market data for: " + content["name"] + "\n")

    stock = yf.Ticker(content["name"])
    p = content["period"]

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d",
    }

    return stock.history(
        period=p,
        interval=period_to_interval.get(p),
        prepost="True",
        actions="False",
    ).to_json()


@assets.route("/twitter_sentiment", methods=["POST"])
def twitter_sentiment():
    content = request.get_json()

    results = twitter_connector.get_tweets_mentioning_asset(content["name"])
    text = []

    for result in results:
        print(result.text)

        text_clean = re.sub(r'@[A-Za-z0-9]+', '', result.text)
        text_clean = re.sub(r'#', '', text_clean)
        text_clean = re.sub('\n', ' ', text_clean)

        # using this will take a lot longer that TextBlobs default analyzer
        # blob = TextBlob(result.text, analyzer=NaiveBayesAnalyzer())

        blob = TextBlob(text_clean)

        # first number: polarity (-1.0 = very negative, 0 = neutral, 1.0 = very positive)
        # second number: subjectivity (0.0 = objective, 1.0 = subjective)
        text.append([text_clean, blob.sentiment])

    return jsonify(text)


@assets.route("/reddit_sentiment", methods=["GET"])
def reddit_sentiment_route():

    res = store_tweet_by_id.delay(tweet_id=1450846775221399566)

    res_2 = store_submissions.delay(keywords=["apple"], limit=50)
    res_3 = store_comments.delay(keywords=["apple"], limit=50)

    return json_response(
        [res.get(timeout=100), res_2.get(timeout=100), res_3.get(timeout=100)]
    )
