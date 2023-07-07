# File: /tests/models/test_finance_utils.py

import unittest
from unittest.mock import patch, MagicMock
from models import finance_utils

class TestFinanceUtils(unittest.TestCase):

    def test_compile_and_average_scores(self):
        scores = [[5, 6, 7], [1, 2, 3]]
        self.assertEqual(finance_utils.compile_and_average_scores(scores), 4.0)

    @patch('models.finance_utils.get_symbol', return_value='AAPL')
    def test_translate_symbols(self, mock_get_symbol):
        scores_dict = {'Apple Inc': 5}
        translated_scores = finance_utils.translate_symbols(scores_dict)
        self.assertEqual(translated_scores['AAPL'], 5)

    @patch('requests.get')
    def test_get_symbol(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'bestMatches': [{'4. region': 'United States', '1. symbol': 'AAPL'}]}
        mock_get.return_value = mock_response
        symbol = finance_utils.get_symbol('Apple Inc')
        self.assertEqual(symbol, 'AAPL')

    @patch('requests.get')
    def test_get_share_price(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'Time Series (5min)': {'2023-07-05 12:00:00': {'4. close': '150.00'}}}
        mock_get.return_value = mock_response
        price = finance_utils.get_share_price('AAPL')
        self.assertEqual(price, 150.00)

    @patch('models.finance_utils.get_symbol', return_value='AAPL')
    @patch('models.finance_utils.get_share_price', return_value=150.0)
    def test_prepare_trades(self, mock_get_share_price, mock_get_symbol):
        sentiment_scores = {'Apple Inc': [5, 6, 7, 8, 9]}
        trades_preparation = finance_utils.prepare_trades(sentiment_scores)
        self.assertEqual(trades_preparation[0]['symbol'], 'AAPL')
        self.assertEqual(trades_preparation[0]['share_price'], 150.0)
        self.assertEqual(trades_preparation[0]['sentiment_score'], 7.0)

    def test_calculate_total_sentiment(self):
        trades_preparation = [{'symbol': 'AAPL', 'sentiment_score': 5, 'share_price': 150.0}]
        total_sentiment = finance_utils.calculate_total_sentiment(trades_preparation)
        self.assertEqual(total_sentiment, 5)
