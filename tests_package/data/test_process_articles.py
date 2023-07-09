from unittest import TestCase, mock
from data.process_articles import process_article, fetch_article
import re


class ProcessArticlesTest(TestCase):
    @mock.patch('data.process_articles.create_webdriver')
    @mock.patch('data.process_articles.BeautifulSoup')
    def test_process_article(self, mock_bs4, mock_create_webdriver):
        mock_bs4.return_value.find.return_value.get_text.return_value = 'Article Content'
        mock_create_webdriver().__enter__().get.return_value = None
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = process_article('yahoo_finance', 'https://finance.yahoo.com/news/1-amazon-workers-uk-warehouse-211200564.html')
        expected_result = {'content': 'Article Content'}
        self.assertEqual(result, expected_result)
        
    @mock.patch('data.fetch_articles.create_webdriver')
    @mock.patch('data.fetch_articles.is_valid_url', return_value=True)
    def test_fetch_article(self, mock_is_valid_url, mock_create_webdriver):
        mock_create_webdriver().__enter__().get.return_value = None
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = fetch_article('https://finance.yahoo.com/news/1-amazon-workers-uk-warehouse-211200564.html')
        #self.assertEqual(result, "<html></html>")
        self.assertRegex(result, r'(?s)<html>.+</html>')
