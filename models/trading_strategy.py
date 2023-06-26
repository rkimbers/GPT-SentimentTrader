# file: trading_strategy.py
from operator import itemgetter
from alpaca_trade_api import REST
from alpaca.trading.client import TradingClient
from .finance_utils import get_symbol, get_share_price, prepare_trades, calculate_total_sentiment
from .finance_utils import compile_and_average_scores, translate_symbols
from .account_utils import account_value, portfolio_positions
from database.db_manager import check_url_in_database, save_url_to_database
from my_alpaca.trading import submit_order
from dotenv import load_dotenv
from operator import itemgetter
from math import floor

import os
import requests

def prepare_buy_orders(sentiment_scores):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    
    portfolio_value = account_value()
    order_cap = portfolio_value * 0.10

    sentiment_scores_copy = sentiment_scores.copy()
    for k, v in sentiment_scores_copy.items():
        if check_url_in_database(k):  # Skip if this URL is already in the database
            del sentiment_scores[k]
            continue
        
        score = compile_and_average_scores(v)
        if score == 10 or score == -10:  # If the sentiment score is 10 or -10, prepare and submit an order immediately
            immediate_order = prepare_immediate_order(k, score, 'buy' if score > 0 else 'sell')
            print(f"Submitting immediate order: {immediate_order}")
            submit_order(immediate_order)
            continue

        sentiment_scores[k] = score
        #save_url_to_database(url, source, k, score)  # Save the URL and the sentiment score to the database

    # Translate sentiment_scores keys from company names to symbols
    sentiment_scores = {get_symbol(k): v for k, v in sentiment_scores.items()}

    # Filter out sentiment_scores with negative average scores
    sentiment_scores = {k: v for k, v in sentiment_scores.items() if v > 0}

    trades_preparation = prepare_trades(sentiment_scores)
    total_sentiment = calculate_total_sentiment(trades_preparation)
    
    trades_to_execute = []
    for trade in trades_preparation:
        symbol = trade['symbol']
        weight = trade['sentiment_score'] / total_sentiment  # Calculate weight for each stock
        allocated_money = order_cap * weight  # Allocate money based on weight

        share_price = get_share_price(symbol)
        if share_price is None:
            print(f"Skipping trade preparation for {symbol} due to inability to retrieve share price.")
            continue

        qty = floor(allocated_money / share_price)  # Calculate quantity to buy

        trades_to_execute.append({
            'symbol': symbol,
            'qty': qty,
            'side': 'buy',
            'type': 'market',
            'time_in_force': 'gtc'
        })

        order_cap -= qty * share_price

    return trades_to_execute

def prepare_sell_orders(sentiment_scores):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    positions = portfolio_positions(trading_client)

    sell_orders = []
    for position in positions:
        symbol = position['symbol']
        score = sentiment_scores.get(symbol)
        
        if score is not None and score < 0:
            fraction_to_sell = abs(score / 10)  # e.g. -2 becomes 0.2, -9 becomes 0.9
            qty_to_sell = int(fraction_to_sell * int(position['qty']))

            if qty_to_sell > 0:
                sell_orders.append({
                    'symbol': symbol,
                    'qty': qty_to_sell,
                    'side': 'sell',
                    'type': 'market',
                    'time_in_force': 'gtc'
                })

    return sell_orders


def prepare_immediate_order(company, score, side):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    portfolio_value = account_value()
    order_cap = portfolio_value * 0.01 #1% of portfolio value for immediate orders

    # Translate company name to symbol
    symbol = get_symbol(company)
    if symbol is None:
        print(f"Unable to translate company name to symbol for company: {company}")
        return None

    # Obtain the current price of the stock
    share_price = get_share_price(symbol)
    if share_price is None:
        print(f"Skipping trade preparation for {symbol} due to inability to retrieve share price.")
        return None

    # Calculate the weight of the order and the allocated money
    weight = abs(score) / 10  # Calculate weight based on score
    allocated_money = order_cap * weight  # Allocate money based on weight

    # Calculate the number of shares to purchase given the allocated money
    qty = floor(allocated_money / share_price)

    return {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': 'market',
        'time_in_force': 'gtc'
    }


if __name__ == '__main__':
    load_dotenv()


    sentiment_scores = {
        'Nvidia': -8,
        'Amazon': 5,
        'Target Corp': 5,
        'Advanced Micro Devices Inc': 2,
        'Apple Inc': -9  
    }

    #print(prepare_buy_orders(sentiment_scores))
    print(prepare_sell_orders(sentiment_scores))
