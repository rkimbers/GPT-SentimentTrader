# file: nlp_processing.py
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import string

class NLPProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def process(self, processed_article):
        try:
            content = processed_article.get('content', '')

            # Tokenize sentences and words
            sentences = sent_tokenize(content)
            tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

            # Remove punctuation and non-alphabetic tokens and convert to lower case
            tokenized_sentences = [[word.lower() for word in sentence if word.isalpha()] for sentence in tokenized_sentences]

            # Remove stopwords
            tokenized_sentences = [[word for word in sentence if word not in self.stop_words] for sentence in tokenized_sentences]

            # Part of speech tagging
            pos_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]

            # Lemmatization
            lemmatized_sentences = [[self.lemmatizer.lemmatize(word[0], pos=self.get_wordnet_pos(word[1])) for word in sentence] for sentence in pos_sentences]

            processed_content = ' '.join([' '.join(sentence) for sentence in lemmatized_sentences])

            processed_article['content'] = processed_content

            return processed_article

        except Exception as e:
            logging.error(f"Exception occurred during NLP processing: {e}")
            return processed_article
