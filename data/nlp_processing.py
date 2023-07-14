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

    def tokenize_sentences(self, content):
        return [word_tokenize(sentence) for sentence in sent_tokenize(content)]

    def remove_punctuations_and_non_alphabets(self, sentences):
        return [[word.lower() for word in sentence if word.isalpha()] for sentence in sentences]

    def remove_stopwords(self, sentences):
        return [[word for word in sentence if word not in self.stop_words] for sentence in sentences]

    def pos_tagging(self, sentences):
        return [pos_tag(sentence) for sentence in sentences]

    def lemmatize(self, sentences):
        return [[self.lemmatizer.lemmatize(word[0], pos=self.get_wordnet_pos(word[1])) for word in sentence] for sentence in sentences]

    def process(self, processed_article):
        try:
            content = processed_article.get('content', '')

            sentences = self.tokenize_sentences(content)
            alpha_sentences = self.remove_punctuations_and_non_alphabets(sentences)
            sentences_without_stopwords = self.remove_stopwords(alpha_sentences)
            pos_sentences = self.pos_tagging(sentences_without_stopwords)
            lemmatized_sentences = self.lemmatize(pos_sentences)

            processed_content = ' '.join([' '.join(sentence) for sentence in lemmatized_sentences])

            processed_article['content'] = processed_content

            return processed_article

        except Exception as e:
            logging.error(f"Exception occurred during NLP processing: {e}")
            return processed_article
