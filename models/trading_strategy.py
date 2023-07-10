# file: trading_strategy.py
from operator import itemgetter
from alpaca.trading.client import TradingClient
from .finance_utils import get_symbol, get_share_price, prepare_trades, calculate_total_sentiment
from .finance_utils import compile_and_average_scores, translate_symbols
from .account_utils import account_value, portfolio_positions
from dotenv import load_dotenv
from operator import itemgetter
from math import floor
import os
import logging


def prepare_buy_orders(sentiment_scores):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    
    try:
        portfolio_value = account_value()
        order_cap = portfolio_value * 0.10

        # Prepare trades and filter out any with a non-positive sentiment score
        trades_preparation = [trade for trade in prepare_trades(sentiment_scores) if trade['sentiment_score'] > 0]
        total_sentiment = calculate_total_sentiment(trades_preparation)
        
        trades_to_execute = []
        for score in trades_preparation:
            try:
                if score['sentiment_score'] > 0:
                    symbol = score['symbol']
                    sentiment_score = score['sentiment_score']
                    share_price = score['share_price']  # Get the share price from the score dictionary

                    weight = sentiment_score / total_sentiment  # Calculate weight for each stock
                    allocated_money = order_cap * weight  # Allocate money based on weight

                    qty = floor(allocated_money / share_price)  # Calculate quantity to buy

                    trades_to_execute.append({
                        'symbol': symbol,
                        'qty': qty,
                        'side': 'buy',
                        'type': 'market',
                        'time_in_force': 'gtc'
                    })

                    order_cap -= qty * share_price  # Decrement the available order capital
            except Exception as e:
                logging.error(f"Error preparing buy order for {symbol}: {str(e)}")
                continue

        return trades_to_execute
    except Exception as e:
        logging.error(f"Exception occurred in prepare_buy_orders: {e}")
        raise e
        return []



def prepare_sell_orders(sentiment_scores):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    try:
        positions = portfolio_positions()

        sell_orders = []
        for position in positions:
            symbol = position['symbol']
            score = sentiment_scores.get(symbol)
            
            if score is not None and score < 0:
                fraction_to_sell = abs(score / 10)  # ex -2 becomes 0.2, -9 becomes 0.9
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
    except Exception as e:
        logging.error(f"Exception occurred in prepare_sell_orders: {e}")
        raise e
        return []


def prepare_immediate_order(company, score, side):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    try:
        portfolio_value = account_value()
        order_cap = portfolio_value * 0.01  # 1% of portfolio value for immediate orders

        # Translate company name to symbol
        try:
            symbol = get_symbol(company)
        except Exception as e:
            logging.error(f"Failed to get the symbol for company '{company}': {str(e)}")
            return None
        if symbol is None:
            logging.info(f"Unable to translate company name to symbol for company: {company}")
            return None

        # Obtain the current share value
        share_price = get_share_price(symbol)
        if share_price is None:
            logging.info(f"Skipping trade preparation for {symbol} due to inability to retrieve share price.")
            return None

        # Calculate the weight of the order and the allocated money
        #weight = abs(score)
        #allocated_money = order_cap * weight  # Allocate money based on weight

        # Calculate the number of shares to purchase given the allocated money
        qty = floor(order_cap / share_price)

        return {
            'symbol': symbol,
            'qty': qty,
            'side': side,
            'type': 'market',
            'time_in_force': 'gtc'
        }
    except Exception as e:
        logging.error(f"Exception occurred in prepare_immediate_order: {e}")
        raise e
        return None


if __name__ == '__main__':
    load_dotenv()

    sentiment_scores = {
        'Nvidia': -8,
        'Amazon': 5,
        'Target Corp': 5,
        'Advanced Micro Devices Inc': 2,
        'Apple Inc': -9  
    }

    print(prepare_buy_orders(sentiment_scores))
    print(prepare_sell_orders(sentiment_scores))
