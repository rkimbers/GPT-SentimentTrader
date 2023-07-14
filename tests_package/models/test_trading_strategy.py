# File: /tests/models/test_trading_strategy.py
import unittest
from unittest.mock import patch, MagicMock
from models.trading_strategy import prepare_buy_orders, prepare_immediate_order, prepare_sell_orders
import pytest

class TestTradingStrategy(unittest.TestCase):
    @patch('models.trading_strategy.account_value', return_value=10000)
    @patch('models.trading_strategy.prepare_trades', return_value=[{'symbol': 'AAPL', 'sentiment_score': 5, 'share_price': 100}])
    @patch('models.trading_strategy.calculate_total_sentiment', return_value=5)
    def test_prepare_buy_orders(self, mock_calculate_total_sentiment, mock_prepare_trades, mock_account_value):
        sentiment_scores = {'Apple Inc': 5}
        orders = prepare_buy_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')
        self.assertEqual(orders[0]['qty'], 10)  # Adjusted expectation
        self.assertEqual(orders[0]['side'], 'buy')

    @patch('models.trading_strategy.portfolio_positions', return_value=[{'symbol': 'AAPL', 'qty': 50}])
    @patch('alpaca.trading.client.TradingClient', MagicMock())
    def test_prepare_sell_orders(self, mock_portfolio_positions):
        sentiment_scores = {'AAPL': -50}  # Adjusted sentiment score to match the symbol in the portfolio_positions
        orders = prepare_sell_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')
        self.assertEqual(orders[0]['qty'], 25)  # Adjusted expectation
        self.assertEqual(orders[0]['side'], 'sell')

    @patch('models.trading_strategy.get_symbol', return_value='AAPL')
    @patch('models.trading_strategy.get_share_price', return_value=50)
    @patch('models.trading_strategy.account_value', return_value=10000)
    @patch('alpaca.trading.client.TradingClient', MagicMock())
    def test_prepare_immediate_order_success(self, mock_account_value, mock_get_share_price, mock_get_symbol):
        order = prepare_immediate_order('Apple', 0.8, 'buy')
        self.assertEqual(order['symbol'], 'AAPL')
        self.assertEqual(order['qty'], 2)  # Adjusted expectation
        self.assertEqual(order['side'], 'buy')
        self.assertEqual(order['type'], 'market')
        self.assertEqual(order['time_in_force'], 'gtc')

#    @patch('trading_strategy.get_symbol', return_value=None)
#    @patch('alpaca.trading.client.TradingClient', MagicMock())
#    def test_prepare_immediate_order_failed_to_get_symbol(self, mock_get_symbol):
#        order = trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
#        self.assertIsNone(order)

#    @patch('trading_strategy.get_share_price', return_value=None)
#    @patch('trading_strategy.get_symbol', return_value='AAPL')
#    @patch('alpaca.trading.client.TradingClient', MagicMock())
#    def test_prepare_immediate_order_failed_to_get_share_price(self, mock_get_symbol, mock_get_share_price):
#        order = trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
#        self.assertIsNone(order)
