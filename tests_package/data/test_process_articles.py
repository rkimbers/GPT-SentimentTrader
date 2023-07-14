from unittest import TestCase, mock
from data.process_articles import process_article, fetch_article
import re

class ProcessArticlesTest(TestCase):
    @mock.patch('data.process_articles.create_webdriver')
    @mock.patch('bs4.BeautifulSoup')
    def test_process_article(self, mock_bs4, mock_create_webdriver):
        # Mock BeautifulSoup instance's find method to return a mock with text attribute
        instance = mock_bs4.return_value
        instance.find.return_value = mock.Mock(text='Article Content')
        
        mock_create_webdriver().__enter__().get.return_value = None
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = process_article('yahoo_finance', 'https://finance.yahoo.com/news/2-auto-related-stocks-buy-011500740.html')
        self.assertEqual(result, {'content': 'Article Content'})
        
    @mock.patch('data.process_articles.create_webdriver')
    @mock.patch('data.process_articles.is_valid_url', return_value=True)
    def test_fetch_article(self, mock_is_valid_url, mock_create_webdriver):
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = fetch_article('https://example.com')
        self.assertEqual(result, "<html></html>")
