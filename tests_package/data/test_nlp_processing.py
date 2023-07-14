from unittest import TestCase, mock
from data.nlp_processing import process_article_body


class TestNlpProcessing(TestCase):

    @mock.patch('nlp_processing.word_tokenize')
    @mock.patch('nlp_processing.WordNetLemmatizer')
    def test_process_article_body(self, mock_lemmatizer, mock_word_tokenize):
        # Define the behavior of the mock objects
        mock_word_tokenize.return_value = ['This', 'is', 'a', 'sample', 'text', '.']
        mock_lemmatizer().lemmatize.side_effect = ['This', 'be', 'a', 'sample', 'text', '.']
        
        # Call the function to be tested
        article_body = "This is a sample text."
        result = process_article_body(article_body)
        
        # Verify the result
        expected_result = 'This be a sample text .'
        self.assertEqual(result, expected_result)
        
        # Assert that the mock objects were called with the correct arguments
        mock_word_tokenize.assert_called_once_with(article_body)
        mock_lemmatizer().lemmatize.assert_has_calls([mock.call(word) for word in mock_word_tokenize.return_value])
