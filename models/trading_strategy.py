#file: trading_strategy.py
from operator import itemgetter
from alpaca_trade_api import REST
from alpaca.trading.client import TradingClient
from finance_utils import get_symbol 
from dotenv import load_dotenv

import os
import requests
from operator import itemgetter
from math import floor

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Getting non-marginable account value and printing it
def account_value():  
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    account = trading_client.get_account()
    return float(account.non_marginable_buying_power)

# Gets share price given a ticker symbol
def get_share_price(ticker):
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"

    # Send the GET request and get the response
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()
    # Ensure the response contains the key "Time Series (5min)"
    if "Time Series (5min)" in data:
        # Get the most recent timestamp
        recent_timestamp = max(data["Time Series (5min)"].keys())

        # Get the closing price at the most recent timestamp
        recent_price = data["Time Series (5min)"][recent_timestamp]["4. close"]

        return float(recent_price)
    else:
        print(f"Unable to get price for ticker {ticker}.")
        return None


def decide_trades(sentiment_scores):
    portfolio_value = account_value()
    order_cap = portfolio_value * 0.10

    # Convert company names to ticker symbols and get share prices
    trades_preparation = []
    for company, sentiment_score in sentiment_scores.items():
        symbol = get_symbol(company)
        if symbol is not None:
            share_price = get_share_price(symbol)
            trades_preparation.append({
                'symbol': symbol,
                'sentiment_score': sentiment_score,
                'share_price': share_price,
            })

    # Sort trades in descending order of sentiment score
    trades_preparation.sort(key=itemgetter('sentiment_score'), reverse=True)

    # Calculate the total sentiment score
    total_sentiment = sum([trade['sentiment_score'] for trade in trades_preparation])

    # Decide on trades to execute
    trades_to_execute = []
    for trade in trades_preparation:
        weight = trade['sentiment_score'] / total_sentiment  # Calculate weight for each stock
        allocated_money = portfolio_value * 0.10 * weight  # Allocate money based on weight

        if allocated_money > order_cap:  # Ensure that allocated money is not greater than available budget
            allocated_money = order_cap

        qty = floor(allocated_money / trade['share_price'])  # Calculate quantity to buy

        # Ensure qty * share_price doesn't exceed order_cap
        if qty * trade['share_price'] > order_cap:
            qty = floor(order_cap / trade['share_price'])

        trades_to_execute.append({
            'symbol': trade['symbol'],
            'qty': qty,
            'sentiment_score': trade['sentiment_score'],
            'share_price': trade['share_price'],
        })

        # Update the order cap
        order_cap -= qty * trade['share_price']

    return trades_to_execute


if __name__ == '__main__':
    load_dotenv()
    
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    
    sentiment_scores = {
        'Nvidia': 8,
        'Amazon': 5,
        'Target Corporation': 5,
        'Advanced Micro Devices, Inc.': 2,
        'Apple Inc.': 9
    }
    
    print(decide_trades(sentiment_scores))