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
        sentiment_scores = {'Apple Inc': 5}
        orders = trading_strategy.prepare_buy_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')
        self.assertEqual(orders[0]['qty'], 2)
        self.assertEqual(orders[0]['side'], 'buy')

    @patch('alpaca.trading.client.TradingClient', MagicMock())
    @patch('models.account_utils.portfolio_positions', return_value=[{'symbol': 'AAPL', 'qty': 10}])
    def test_prepare_sell_orders(self, mock_portfolio_positions):
        sentiment_scores = {'Apple Inc': -5}
        orders = trading_strategy.prepare_sell_orders(sentiment_scores)
        self.assertEqual(orders[0]['symbol'], 'AAPL')
        self.assertEqual(orders[0]['qty'], 5)
        self.assertEqual(orders[0]['side'], 'sell')

    @patch('models.finance_utils.get_symbol', return_value='AAPL')
    @patch('models.finance_utils.get_share_price', return_value=150)
    @patch('models.account_utils.account_value', return_value=10000)
    @patch('alpaca.trading.client.TradingClient', MagicMock())
    def test_prepare_immediate_order_success(self, mock_account_value, mock_get_share_price, mock_get_symbol):
        order = trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
        self.assertEqual(order['symbol'], 'AAPL')
        self.assertEqual(order['qty'], 0)
        self.assertEqual(order['side'], 'buy')
        self.assertEqual(order['type'], 'market')
        self.assertEqual(order['time_in_force'], 'gtc')

if __name__ == '__main__':
    unittest.main()


#    @patch('models.finance_utils.get_symbol', return_value=None)
#    @patch('alpaca.trading.client.TradingClient')
#    def test_prepare_immediate_order_failed_to_get_symbol(self, MockClient, mock_get_symbol):
#        MockClient.return_value = MagicMock()
#        with pytest.raises(Exception, match="Unable to translate company name to symbol for company: Apple"):
#            trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')

#    @patch('models.finance_utils.get_symbol', return_value='AAPL')
#    @patch('models.finance_utils.get_share_price', return_value=None)
#    @patch('alpaca.trading.client.TradingClient')
#    def test_prepare_immediate_order_failed_to_get_share_price(self, MockClient, mock_get_share_price, mock_get_symbol):
#        MockClient.return_value = MagicMock()
#        with pytest.raises(Exception, match="Skipping trade preparation for AAPL due to inability to retrieve share price."):
#            trading_strategy.prepare_immediate_order('Apple', 0.8, 'buy')
