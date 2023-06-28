# file: account_utils.py

import os
#import alpaca_trade_api as tradeapi

#from alpaca_trade_api import REST
from alpaca.trading.client import TradingClient


# Getting non-marginable account value and printing it
def account_value():  
    
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    
    
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    account = trading_client.get_account()
    return float(account.non_marginable_buying_power)



def portfolio_positions(trading_client):     
    ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    
    positions = trading_client.get_all_positions()

    simplified_positions = [{'symbol': position.symbol, 'qty': position.qty} for position in positions]

    return simplified_positions

