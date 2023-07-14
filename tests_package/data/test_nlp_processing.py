import unittest
from unittest.mock import patch, MagicMock, Mock
from data.nlp_processing import NLPProcessor

class TestNLPProcessor(unittest.TestCase):

    @patch('nltk.tokenize.word_tokenize', return_value=['this', 'is', 'a', 'sample', 'text'])
    @patch('nltk.tokenize.sent_tokenize', return_value=['This is a sample text.'])
    @patch('nltk.tag.pos_tag', return_value=[('this', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('sample', 'JJ'), ('text', 'NN')])
    @patch('nltk.stem.WordNetLemmatizer.lemmatize')
    @patch('nltk.corpus.stopwords.words', return_value=['is', 'a'])
    def test_process(self, mock_stopwords, mock_lemmatize, mock_pos_tag, mock_sent_tokenize, mock_word_tokenize):
        # Create NLPProcessor instance
        processor = NLPProcessor()

        # Set lemmatization mock to return input word
        mock_lemmatize.side_effect = lambda word, pos: word

        # Call the function to be tested
        article_body = {'content': "This is a sample text."}
        result = processor.process(article_body)
        
        # Verify the result
        expected_result = {'content': 'this sample text'}
        self.assertEqual(result, expected_result)

        # Assert that the mock objects were called with the correct arguments
        mock_sent_tokenize.assert_called_once_with(article_body['content'])
        mock_word_tokenize.assert_called_with(mock_sent_tokenize.return_value[0])
        mock_pos_tag.assert_called_with(mock_word_tokenize.return_value)
        mock_lemmatize.assert_has_calls([Mock.call(word, pos=processor.get_wordnet_pos(pos)) for word, pos in mock_pos_tag.return_value])


