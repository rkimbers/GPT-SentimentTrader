from unittest import TestCase, mock
from ...data.process_articles import process_article

class ProcessArticlesTest(TestCase):
    @mock.patch('data.process_articles.create_webdriver')
    @mock.patch('data.process_articles.BeautifulSoup')
    def test_process_article(self, mock_bs4, mock_create_webdriver):
        mock_bs4.return_value.find.return_value.get_text.return_value = 'Article Content'
        mock_create_webdriver().__enter__().get.return_value = None
        mock_create_webdriver().__enter__().page_source = "<html></html>"
        result = process_article('yahoo_finance', 'https://example.com')
        self.assertEqual(result, 'Article Content')
