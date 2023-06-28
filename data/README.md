# data

This directory contains the necessary modules for fetching and processing financial news articles to be used in the sentiment analysis.

## Files

### __init__.py
This file is necessary to make Python treat the `data` directory as a package (i.e., a directory that can contain other modules).

### fetch_articles.py
This module contains the `fetch_articles()` function for collecting financial news articles. 

#### `is_valid_url()`
This function is very simple. It takes the `url` string as a parameter and returns a boolean as to wether or not it's a valid URL.

#### `fetch_article()`
This function is used as support for the `process_article()` function in the `process_articles` module. It takes the `url` string as a parameter and returns the raw HTML content of the webpage.

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

## Usage
Import the necessary functions from each file as needed. For example, to use the `process_article()` function in your code, you would use:

```python
from data.process_articles.py import process_article