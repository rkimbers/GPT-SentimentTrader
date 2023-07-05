import os
import logging
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def list_positions():
    try:
        ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
        ALPACA_SECRET_KEY = os.getenv("APCA_SECRET_KEY")
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        positions = trading_client.get_all_positions()
        for position in positions:
            for property_name, value in position:
                logging.info(f"\"{property_name}\": {value}")
    except Exception as e:
        logging.error(f"Failed to list positions. Error: {e}")
        raise e


def submit_order(order):
    try:
        ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
        ALPACA_SECRET_KEY = os.getenv("APCA_SECRET_KEY")
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

        symbol = order['symbol']
        qty = order['qty']
        side = order['side']
        type_ = order['type']
        time_in_force = order['time_in_force']

        side = side.upper()

        if side not in ["BUY", "SELL"]:
            error_message = f"Invalid side: {side} for symbol: {symbol}. Skipping..."
            logging.error(error_message)
            raise ValueError(error_message)

        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            type=type_,
            time_in_force=TimeInForce.GTC if time_in_force == 'gtc' else None
        )

        order_response = trading_client.submit_order(order_data)
        return order_response  

    except Exception as e:
        error_message = f"Failed to submit order for {symbol}. Error: {e}"
        logging.error(error_message)
        raise e
