import os
import logging
from alpaca.trading.client import TradingClient


# Getting non-marginable account value and printing it
def account_value():  
    
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

    try:
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        account = trading_client.get_account()
        return float(account.non_marginable_buying_power)
    except Exception as e:
        logging.error("Error getting account value: %s", e)
        return None


def portfolio_positions():     
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

    try:
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        positions = trading_client.get_all_positions()
        simplified_positions = [{'symbol': position.symbol, 'qty': position.qty} for position in positions]
        return simplified_positions
    except Exception as e:
        logging.error("Error getting portfolio positions: %s", e)
        return None
