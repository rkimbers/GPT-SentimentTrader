from unittest import TestCase, mock
from data.fetch_articles import yf_fetch_articles

class FetchArticlesTest(TestCase):     
    @mock.patch('data.fetch_articles.requests.get')
    @mock.patch('data.fetch_articles.BeautifulSoup')
    def test_yf_fetch_articles(self, mock_bs4, mock_requests):
        mock_requests.return_value.text = "<html></html>"
        mock_bs4.return_value.find_all.return_value = [{'href': '/news/example'}]
        result = yf_fetch_articles()
        self.assertEqual(result, ["https://finance.yahoo.com/news/example"])

