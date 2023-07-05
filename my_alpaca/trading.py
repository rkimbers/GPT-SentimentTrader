import os
import logging
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def list_positions():
    try:
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        positions = trading_client.get_all_positions()
        for position in positions:
            for property_name, value in position:
                logging.info(f"\"{property_name}\": {value}")
    except Exception as e:
        logging.error(f"Failed to list positions. Error: {e}")

def submit_order(order):
    try:
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
            error_message = f"Invalid side: {side} for symbol: {symbol}. Skipping..."
            logging.error(error_message)
            return error_message

        # Assemble the order data
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            type=type_,
            time_in_force=TimeInForce.GTC if time_in_force == 'gtc' else None
        )

        # Try to submit the order
        order_response = trading_client.submit_order(order_data)
        return order_response  # Return the order_response if successful

    except Exception as e:
        error_message = f"Failed to submit order for {symbol}. Error: {e}"
        logging.error(error_message)
        return error_message  # Return the error message if order submission failed
