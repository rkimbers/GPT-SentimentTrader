# File: /tests/models/test_account_utils.py

import unittest
from unittest.mock import patch, MagicMock
from models import account_utils


class TestAccountUtils(unittest.TestCase):

    @patch('models.account_utils.TradingClient.get_account')
    def test_account_value(self, mock_get_account):
        mock_account = MagicMock()
        mock_account.non_marginable_buying_power = 1000
        mock_get_account.return_value = mock_account
        self.assertEqual(account_utils.account_value(), 1000)

    @patch('models.account_utils.TradingClient.get_all_positions')
    def test_portfolio_positions(self, mock_get_all_positions):
        mock_position = MagicMock()
        mock_position.symbol = 'AAPL'
        mock_position.qty = 10
        mock_get_all_positions.return_value = [mock_position]
        positions = account_utils.portfolio_positions()
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0]['symbol'], 'AAPL')
        self.assertEqual(positions[0]['qty'], 10)

# Similar structure would be used for other methods in `account_utils.py` 

if __name__ == '__main__':
    unittest.main()
