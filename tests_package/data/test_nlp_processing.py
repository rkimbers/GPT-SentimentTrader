import unittest
from unittest.mock import patch
from data.nlp_processing import NLPProcessor

class TestNLPProcessor(unittest.TestCase):

    def setUp(self):
        self.nlp_processor = NLPProcessor()

    @patch('nltk.stem.WordNetLemmatizer.lemmatize')
    def test_lemmatize(self, mock_lemmatize):
        mock_lemmatize.return_value = 'test'
        result = self.nlp_processor.lemmatize([['testing']])
        self.assertEqual(result, [['test']])

    @patch('nltk.pos_tag')
    def test_pos_tagging(self, mock_pos_tag):
        mock_pos_tag.return_value = [('test', 'NN')]
        result = self.nlp_processor.pos_tagging([['test']])
        self.assertEqual(result, [[('test', 'NN')]])

    @patch('nltk.corpus.stopwords.words')
    def test_remove_stopwords(self, mock_stopwords):
        mock_stopwords.return_value = ['this', 'is']
        result = self.nlp_processor.remove_stopwords([['this', 'is', 'a', 'test']])
        self.assertEqual(result, [['test']])

    @patch('nltk.sent_tokenize')
    def test_tokenize_sentences(self, mock_sent_tokenize):
        mock_sent_tokenize.return_value = ['this is a test']
        result = self.nlp_processor.tokenize_sentences('this is a test')
        self.assertEqual(result, [['this', 'is', 'a', 'test']])

    def test_remove_punctuations_and_non_alphabets(self):
        result = self.nlp_processor.remove_punctuations_and_non_alphabets([['this', 'is', 'a', 'sample', '!123']])
        self.assertEqual(result, [['this', 'is', 'a', 'sample']])
