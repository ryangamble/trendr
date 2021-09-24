from flask import Flask, Blueprint, request, jsonify
import yfinance as yf

result = Blueprint('result', __name__, url_prefix="/api/result")

@result.route('/stats', methods=['POST'])
def stats():
    content = request.get_json()

    print("\nfetching general stock stats for: " + content['name'] + "\n")
    
    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)

@result.route('/history', methods=['POST'])
def history():
    content = request.get_json()
    
    print("\nfetching history market data for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    p = content['period']

    periodToInterval = {
        "1d" : "5m",
        "5d" : "30m",
        "1mo" : "1h",
        "3mo" : "1d",
        "1y" : "1d",
        "5y" : "5d"
    }

    return stock.history(period=p, interval=periodToInterval.get(p), prepost="True", actions="False").to_json()
