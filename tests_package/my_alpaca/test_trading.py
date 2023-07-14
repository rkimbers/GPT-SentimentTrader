import os
import unittest
from unittest.mock import patch, Mock
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from my_alpaca import trading

class TradingTest(unittest.TestCase):
    @patch.object(TradingClient, "get_all_positions")
    @patch.object(TradingClient, "__init__", return_value=None)
    def test_list_positions(self, mock_init, mock_get_all_positions):
        mock_get_all_positions.return_value = [{"property_name": "value"}]
        trading.list_positions()
        mock_get_all_positions.assert_called_once()

    @patch.object(MarketOrderRequest, "__init__", return_value=None)
    @patch.object(TradingClient, "submit_order")
    @patch.object(TradingClient, "__init__", return_value=None)
    def test_submit_order(self, mock_init, mock_submit_order, mock_order_request):
        mock_submit_order.return_value = "Order response"
        order = {
            'symbol': 'AAPL',
            'qty': 1,
            'side': 'BUY',
            'type': 'market',
            'time_in_force': 'gtc',
        }
        result = trading.submit_order(order)
        self.assertEqual(result, "Order response")
        mock_order_request.assert_called_once_with(
            symbol='AAPL',
            qty=1,
            side=OrderSide.BUY,
            type='market',
            time_in_force=TimeInForce.GTC
        )
        mock_submit_order.assert_called_once()

        # Add test to check if it raises ValueError for invalid side
        order = {
            'symbol': 'AAPL',
            'qty': 1,
            'side': 'INVALID',
            'type': 'market',
            'time_in_force': 'gtc',
        }
        with self.assertRaises(ValueError):
            trading.submit_order(order)
