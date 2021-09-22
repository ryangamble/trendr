from flask import Flask, Blueprint, request, jsonify
import yfinance as yf

result = Blueprint('result', __name__, url_prefix="/result")

@result.route('/stats', methods=['GET', 'POST'])
def general():
    content = request.get_json()

    print("\nfetching general stock stats for: " + content['name'] + "\n")
    
    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)
