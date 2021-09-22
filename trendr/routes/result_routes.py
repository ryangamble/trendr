from flask import Flask, Blueprint, request, jsonify
import yfinance as yf

result = Blueprint('result', __name__, url_prefix="/result")

@result.route('/general', methods=['GET', 'POST'])
def general():
    content = request.get_json()

    print("\nfetching general stock info for: " + content['name'] + "\n")
    
    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)
