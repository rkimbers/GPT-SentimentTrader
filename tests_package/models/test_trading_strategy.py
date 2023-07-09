# File: /tests/models/test_trading_strategy.py

import unittest
from unittest.mock import patch, MagicMock
from models import trading_strategy
from unittest.mock import patch, MagicMock
import os
import pytest

class TestTradingStrategy(unittest.TestCase):
    @patch('models.trading_strategy.prepare_trades', return_value=[{'symbol': 'AAPL', 'sentiment_score': 5, 'share_price': 100}])
    @patch('models.trading_strategy.calculate_total_sentiment', return_value=5)
    @patch('models.trading_strategy.account_value', return_value=10000)
    def test_prepare_buy_orders(self, mock_prepare_trades, mock_calculate_total_sentiment, mock_account_value):
        sentiment_scores = {'AAPL': 5}
        orders = trading_strategy.prepare_buy_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')

    @patch('models.trading_strategy.TradingClient')
    @patch('models.trading_strategy.portfolio_positions', return_value=[{'symbol': 'AAPL', 'qty': 10}])
    def test_prepare_sell_orders(self, mock_trading_client, mock_portfolio_positions):
        sentiment_scores = {'AAPL': -5}
        orders = trading_strategy.prepare_sell_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')

    def test_prepare_immediate_order_success(self):
        with patch('models.get_symbol', return_value='AAPL'), \
            patch('models.get_share_price', return_value=150), \
            patch('models.account_value', return_value=10000), \
            patch('models.TradingClient') as MockClient:
            MockClient.return_value = MagicMock()
            order = trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
            assert order['symbol'] == 'AAPL'
            assert order['qty'] == 0
            assert order['side'] == 'buy'
            assert order['type'] == 'market'
            assert order['time_in_force'] == 'gtc'

    def test_prepare_immediate_order_failed_to_get_symbol(self):
        with patch('models.get_symbol', return_value=None), \
            patch('models.TradingClient') as MockClient:
            MockClient.return_value = MagicMock()
            with pytest.raises(Exception, match="Unable to translate company name to symbol for company: Apple"):
                trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')

    def test_prepare_immediate_order_failed_to_get_share_price(self):
        with patch('models.get_symbol', return_value='AAPL'), \
            patch('models.get_share_price', return_value=None), \
            patch('models.TradingClient') as MockClient:
            MockClient.return_value = MagicMock()
            with pytest.raises(Exception, match="Skipping trade preparation for AAPL due to inability to retrieve share price."):
                trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
