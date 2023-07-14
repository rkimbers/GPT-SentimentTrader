# File: /tests/models/test_trading_strategy.py
import unittest
from unittest.mock import patch, MagicMock
from models import trading_strategy
import pytest

class TestTradingStrategy(unittest.TestCase):
    @patch('models.finance_utils.prepare_trades', return_value=[{'symbol': 'AAPL', 'sentiment_score': 5, 'share_price': 100}])
    @patch('models.finance_utils.calculate_total_sentiment', return_value=5)
    @patch('models.account_utils.account_value', return_value=10000)
    def test_prepare_buy_orders(self, mock_account_value, mock_calculate_total_sentiment, mock_prepare_trades):
        sentiment_scores = {'AAPL': 5}
        orders = trading_strategy.prepare_buy_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')

    @patch('alpaca.trading.client.TradingClient')
    @patch('models.account_utils.portfolio_positions', return_value=[{'symbol': 'AAPL', 'qty': 10}])
    def test_prepare_sell_orders(self, mock_portfolio_positions, mock_trading_client):
        sentiment_scores = {'AAPL': -5}
        orders = trading_strategy.prepare_sell_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')

    @patch('models.finance_utils.get_symbol', return_value='AAPL')
    @patch('models.finance_utils.get_share_price', return_value=150)
    @patch('models.account_utils.account_value', return_value=10000)
    @patch('alpaca.trading.client.TradingClient')
    def test_prepare_immediate_order_success(self, MockClient, mock_account_value, mock_get_share_price, mock_get_symbol):
        MockClient.return_value = MagicMock()
        order = trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
        assert order['symbol'] == 'AAPL'
        assert order['qty'] == 0
        assert order['side'] == 'buy'
        assert order['type'] == 'market'
        assert order['time_in_force'] == 'gtc'

#    @patch('models.finance_utils.get_symbol', return_value=None)
#    @patch('alpaca.trading.client.TradingClient')
#    def test_prepare_immediate_order_failed_to_get_symbol(self, MockClient, mock_get_symbol):
#        MockClient.return_value = MagicMock()
#        with pytest.raises(Exception, match="Unable to translate company name to symbol for company: Apple"):
#            trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')

    @patch('models.finance_utils.get_symbol', return_value='AAPL')
    @patch('models.finance_utils.get_share_price', return_value=None)
    @patch('alpaca.trading.client.TradingClient')
    def test_prepare_immediate_order_failed_to_get_share_price(self, MockClient, mock_get_share_price, mock_get_symbol):
        MockClient.return_value = MagicMock()
        with pytest.raises(Exception, match="Skipping trade preparation for AAPL due to inability to retrieve share price."):
            trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
