from flask import Blueprint, request, jsonify
import yfinance as yf
import yahooquery as yq

assets = Blueprint('assets', __name__, url_prefix="/assets")


@assets.route('/search', methods=['POST'])
def search():
    content = request.get_json()

    data = yq.search(content['query'], news_count=0, quotes_count=10)

    return jsonify(data)


@assets.route('/stats', methods=['POST'])
def stats():
    content = request.get_json()

    print("\nfetching general stats for: " + content['name'] + "\n")
    
    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)


@assets.route('/history', methods=['POST'])
def history():
    content = request.get_json()
    
    print("\nfetching history market data for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
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
