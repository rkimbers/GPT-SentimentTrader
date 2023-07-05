import os
import logging
from alpaca.trading.client import TradingClient


def account_value():  
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    account = trading_client.get_account()
    if account is None:
        raise Exception("Error getting account")
    return float(account.non_marginable_buying_power)


def portfolio_positions():     
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    positions = trading_client.get_all_positions()
    if positions is None:
        raise Exception("Error getting positions")
    simplified_positions = [{'symbol': position.symbol, 'qty': position.qty} for position in positions]
    return simplified_positions
