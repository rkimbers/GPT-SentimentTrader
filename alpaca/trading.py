# file: alpaca/trading.py

# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


API_KEY = "PKZY38RL61L47HOO01LM"
SECRET_KEY = "7beQlGpjRpm4Gagq5anmSbbE6dAkSfx4et2g0p15"

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Getting account information and printing it
def account_info():
    account = trading_client.get_account()
    for property_name, value in account:
        print(f"\"{property_name}\": {value}")


# Get all open positions and print each of them
def list_positions():
    positions = trading_client.get_all_positions()
    for position in positions:
        for property_name, value in position:
            print(f"\"{property_name}\": {value}")

"""
Submit an order to the Alpaca API.

param trade: A dictionary representing the trade. It should contain the keys "symbol", "qty" and "side".
:return: The API's response to the order.
"""
def submit_order(trade):


    symbol = trade["symbol"]
    qty = trade["qty"]
    side = trade["side"]

    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.GTC
    )

    market_order = trading_client.submit_order(market_order_data)
    
    for property_name, value in vars(market_order).items():
        print(f"\"{property_name}\": {value}")
    
    return market_order
