# File: /tests/my_openai/test_sentiment_analysis.py

import unittest
from unittest.mock import patch, MagicMock
from my_openai import sentiment_analysis

class TestSentimentAnalysis(unittest.TestCase):
    @patch('my_openai.sentiment_analysis.openai.ChatCompletion.create')
    def test_analyze_sentiment(self, mock_chat_completion):
        mock_chat_completion.return_value.choices = [MagicMock(message=MagicMock(content="Company: 5"))]
        article = {'content': 'Some content about the company.'}
        scores = sentiment_analysis.analyze_sentiment(article)
        self.assertEqual(scores['Company'][0], 5)
