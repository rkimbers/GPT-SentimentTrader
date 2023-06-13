# file: trading_strategy.py
from operator import itemgetter
from alpaca_trade_api import REST
from alpaca.trading.client import TradingClient
from finance_utils import get_symbol, get_share_price, prepare_trades, calculate_total_sentiment, translate_symbols
from account_utils import account_value, portfolio_positions
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

    # Translate sentiment_scores keys from company names to symbols
    sentiment_scores = {get_symbol(k): v for k, v in sentiment_scores.items()}

    trades_preparation = prepare_trades(sentiment_scores)
    total_sentiment = calculate_total_sentiment(trades_preparation)
    
    trades_to_execute = []
    for trade in trades_preparation:
        symbol = trade['symbol']
        weight = trade['sentiment_score'] / total_sentiment  # Calculate weight for each stock
        allocated_money = order_cap * weight  # Allocate money based on weight

        qty = floor(allocated_money / trade['share_price'])  # Calculate quantity to buy

        trades_to_execute.append({
            'symbol': symbol,
            'qty': qty,
            'side': 'buy',
            'type': 'market',
            'time_in_force': 'gtc'
        })

        order_cap -= qty * trade['share_price']

    return trades_to_execute


def prepare_sell_orders(sentiment_scores):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    # Translate sentiment_scores keys from company names to symbols
    sentiment_scores = {get_symbol(k): v for k, v in sentiment_scores.items()}
    
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
