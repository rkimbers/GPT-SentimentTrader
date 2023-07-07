from unittest import TestCase, mock
from ...data.fetch_articles import fetch_article, yf_fetch_articles

class FetchArticlesTest(TestCase):
    @mock.patch('data.fetch_articles.create_webdriver')
    @mock.patch('data.fetch_articles.is_valid_url', return_value=True)
    def test_fetch_article(self, mock_is_valid_url, mock_create_webdriver):
        mock_create_webdriver().__enter__().get.return_value = None
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = fetch_article('https://example.com')
        self.assertEqual(result, "<html></html>")
        
    @mock.patch('data.fetch_articles.requests.get')
    @mock.patch('data.fetch_articles.BeautifulSoup')
    def test_yf_fetch_articles(self, mock_bs4, mock_requests):
        mock_requests.return_value.text = "<html></html>"
        mock_bs4.return_value.find_all.return_value = [{'href': '/news/example'}]
        result = yf_fetch_articles()
        self.assertEqual(result, ["https://finance.yahoo.com/news/example"])

