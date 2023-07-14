# data

This directory contains the necessary modules for fetching and processing financial news articles to be used in the sentiment analysis.

## Files

### __init__.py
This file is necessary to make Python treat the `data` directory as a package (i.e., a directory that can contain other modules).

### fetch_articles.py
This module contains the `fetch_articles()` function for collecting financial news articles. 

#### `is_valid_url()`
This function is very simple. It takes the `url` string as a parameter and returns a boolean as to wether or not it's a valid URL.

#### `fetch_articles()`
When `fetch_articles()` is called, it calls the various fetch article functions. It instantiates an articles dictionary, with the key being the news source itself. Each iteration of fetch_articles for the news sources operates in their own unique ways. All of these functions scrape from a topic URL for a href, and append the href to the base url. return the 10 most recent URLs from each of the sources. 

#### `yf_fetch_articles()`
This function used to carry the topic URL `https://finance.yahoo.com/market-news` but yahoo finance updated the site to `https://finance.yahoo.com/most-active`. This function currently works as intended

#### `reuters_fetch_articles()`
This function works as intended.

#### `investing_com_fetch_articles()`
This function works as intended.

#### `bloomberg_fetch_articles()`
This function works as intended. I am unable to parse the URLs, though.

#### `market_watch_fetch_articles()`
This function works as intended.

#### `business_insider_fetch_articles()`
This function is currently broken. I spent a short while trying to fix it, but cannot seem to make it work as is.

### process_articles.py
This module contains the `process_articles()` function that is used for preprocessing and cleaning the articles before they are inputted to the sentiment analysis.

#### `process_article()`
`process_article()` takes the article's `soruce` and `url` as a parameter and retrieves the relevant body content of the article itself. This function makes a request and to the URL using the `fetch_article()` function, expecting the raw HTML as a response. It then uses BeautifulSoup4 to parse the html by div/class. Each class is different for each news site, and must be hardcoded in which is prone to breaking if any news outlet updaties their webpage structure. This function has support for various news sources, with yahoo finance, reuters, marketwatch, and investing.com working as intended. As I am writing this README, I am working on a bloomberg bypass, as bloomberg is a paid site. The function returns a dictionary of the article's relevant body content, with the key being `content` in the format, `{'content': content}`. I understand this is confusing and will fix it in the future.

#### `fetch_article()`
This function is used as support for the `process_article()` function in the `process_articles` module. It takes the `url` string as a parameter and returns the raw HTML content of the webpage.

### nlp_processing.py

The `nlp_processing.py` file contains the implementation of the `NLPProcessor` class, which provides methods for performing natural language processing (NLP) tasks on text data.

#### `NLPProcessor` Class

The `NLPProcessor` class encapsulates the following methods:

- `__init__()`: Initializes the `NLPProcessor` object. It sets up the stop words list and initializes the WordNet lemmatizer.

- `get_wordnet_pos(tag)`: Takes a part-of-speech tag as input and returns the corresponding WordNet POS tag.

- `tokenize_sentences(content)`: Tokenizes the input content into sentences using NLTK's `sent_tokenize()` and then tokenizes each sentence into words using `word_tokenize()`. Returns a list of tokenized sentences.

- `remove_punctuations_and_non_alphabets(sentences)`: Removes punctuations and non-alphabetic characters from the tokenized sentences. Returns a list of sentences with only alphabetic words.

- `remove_stopwords(sentences)`: Removes stop words from the tokenized sentences using NLTK's predefined stop word list. Returns a list of sentences without stop words.

- `pos_tagging(sentences)`: Performs part-of-speech tagging on the tokenized sentences using NLTK's `pos_tag()`. Returns a list of sentences with each word tagged with its part-of-speech.

- `lemmatize(sentences)`: Lemmatizes the tokenized sentences using NLTK's WordNet lemmatizer. It determines the WordNet POS tag for each word and lemmatizes accordingly. Returns a list of lemmatized sentences.

- `process(processed_article)`: Performs the complete NLP processing pipeline on a processed article dictionary. It tokenizes sentences, removes punctuations and non-alphabetic characters, removes stop words, performs part-of-speech tagging, and lemmatizes the sentences. The processed content is then returned as a modified article dictionary.

Please refer to the `nlp_processing.py` file for the complete implementation.

## Usage
Import the necessary functions from each file as needed. For example, to use the `process_article()` function in your code, you would use:

```python
from data.process_articles.py import process_article