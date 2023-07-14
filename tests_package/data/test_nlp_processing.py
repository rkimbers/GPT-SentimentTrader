import unittest
from unittest.mock import patch, MagicMock, Mock
from data.nlp_processing import NLPProcessor

class TestNLPProcessor(unittest.TestCase):

    @patch('nlp_processing.sent_tokenize', return_value=['This is a sample text.'])
    @patch('nlp_processing.word_tokenize', return_value=['This', 'is', 'a', 'sample', 'text'])
    def test_tokenize_sentences(self, mock_word_tokenize, mock_sent_tokenize):
        content = 'This is a sample text.'
        expected_result = [['This', 'is', 'a', 'sample', 'text']]
        
        processor = NLPProcessor()
        result = processor.tokenize_sentences(content)
        
        self.assertEqual(result, expected_result)

    def test_remove_punctuations_and_non_alphabets(self):
        sentences = [['This', 'is', 'a', 'sample', 'text!']]
        expected_result = [['this', 'is', 'a', 'sample', 'text']]
        
        processor = NLPProcessor()
        result = processor.remove_punctuations_and_non_alphabets(sentences)
        
        self.assertEqual(result, expected_result)

    @patch('nlp_processing.stopwords.words', return_value=['is', 'a'])
    def test_remove_stopwords(self, mock_stopwords):
        sentences = [['this', 'is', 'a', 'sample', 'text']]
        expected_result = [['this', 'sample', 'text']]
        
        processor = NLPProcessor()
        result = processor.remove_stopwords(sentences)
        
        self.assertEqual(result, expected_result)

    @patch('nlp_processing.pos_tag', return_value=[('this', 'NN'), ('sample', 'NN'), ('text', 'NN')])
    def test_pos_tagging(self, mock_pos_tag):
        sentences = [['this', 'sample', 'text']]
        expected_result = [[('this', 'NN'), ('sample', 'NN'), ('text', 'NN')]]
        
        processor = NLPProcessor()
        result = processor.pos_tagging(sentences)
        
        self.assertEqual(result, expected_result)

    @patch('nlp_processing.WordNetLemmatizer')
    def test_lemmatize(self, mock_lemmatizer):
        sentences = [[('this', 'NN'), ('sample', 'NN'), ('text', 'NN')]]
        expected_result = [['this', 'sample', 'text']]
        mock_lemmatizer_instance = mock_lemmatizer.return_value
        mock_lemmatizer_instance.lemmatize.side_effect = ['this', 'sample', 'text']
        
        processor = NLPProcessor()
        result = processor.lemmatize(sentences)
        
        self.assertEqual(result, expected_result)

    # Continue with the rest of the tests.
    # You may also want to test the `process` function as a whole. 


