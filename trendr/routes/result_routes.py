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
    return stock.history(period="1y", interval="1d").to_json()
