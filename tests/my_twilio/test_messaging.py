# File: /tests/my_twilio/messaging.py

import unittest
from unittest.mock import patch, MagicMock
from ...my_twilio import messaging

class TestMessaging(unittest.TestCase):

    @patch('my_twilio.messaging.create_twilio_client')
    @patch('my_twilio.messaging.os.getenv', return_value='+1234567890')
    def test_send_order_text(self, mock_getenv, mock_create_twilio_client):
        mock_client = MagicMock()
        mock_create_twilio_client.return_value = mock_client
        orders = [{'symbol': 'AAPL', 'qty': 10, 'side': 'buy', 'type': 'market'}]
        messaging.send_order_text(orders)
        mock_client.messages.create.assert_called()

    @patch('my_twilio.messaging.create_twilio_client')
    @patch('my_twilio.messaging.os.getenv', return_value='+1234567890')
    def test_send_immediate_order_text(self, mock_getenv, mock_create_twilio_client):
        mock_client = MagicMock()
        mock_create_twilio_client.return_value = mock_client
        order = {'symbol': 'AAPL', 'qty': 10, 'side': 'buy', 'type': 'market'}
        messaging.send_immediate_order_text(order)
        mock_client.messages.create.assert_called()

    @patch('my_twilio.messaging.create_twilio_client')
    @patch('my_twilio.messaging.os.getenv', return_value='+1234567890')
    def test_send_market_open_message(self, mock_getenv, mock_create_twilio_client):
        mock_client = MagicMock()
        mock_create_twilio_client.return_value = mock_client
        messaging.send_market_open_message('no_trades')
        mock_client.messages.create.assert_called()
