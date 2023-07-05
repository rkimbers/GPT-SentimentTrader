# file: alpaca/trading.py

# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Get all open positions and print each of them
def list_positions():
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    positions = trading_client.get_all_positions()
    for position in positions:
        for property_name, value in position:
            print(f"\"{property_name}\": {value}")

"""
Submit an order to the Alpaca API.

param trade: A dictionary representing the trade. It should contain the keys "symbol", "qty" and "side".
:return: The API's response to the order.
"""
def submit_order(order):
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

    symbol = order['symbol']
    qty = order['qty']
    side = order['side']
    type_ = order['type']
    time_in_force = order['time_in_force']

    # Convert side to uppercase as it's expected by the SDK
    side = side.upper()

    # Verify that the side is either BUY or SELL
    if side not in ["BUY", "SELL"]:
        print(f"Invalid side: {side} for symbol: {symbol}. Skipping...")
        return f"Invalid side: {side} for symbol: {symbol}. Skipping..."

    # Assemble the order data
    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
        type=type_,
        time_in_force=TimeInForce.GTC if time_in_force == 'gtc' else None
    )

    # Try to submit the order
    try:
        order_response = trading_client.submit_order(order_data)
        return order_response  # Return the order_response if successful
    except Exception as e:
        error_message = f"Failed to submit order for {symbol}. Error: {e}"
        print(error_message)
        return error_message  # Return the error message if order submission failed


