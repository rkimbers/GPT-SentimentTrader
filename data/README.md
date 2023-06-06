# data

This directory contains the necessary modules for fetching and processing financial news articles to be used in the sentiment analysis.

## Files

### __init__.py
This file is necessary to make Python treat the `data` directory as a package (i.e., a directory that can contain other modules).

### fetch_articles.py
This module contains the `fetch_articles()` function for collecting financial news articles. 

#### `fetch_articles()`
This function takes a URL as input and fetches the relevant financial news articles from the web. 

### process_articles.py
This module contains the `process_articles()` function that is used for preprocessing and cleaning the articles before they are input to the sentiment analysis.

#### `process_articles()`
This function takes a list of articles as input, processes them to remove any unwanted characters or words, and returns a list of cleaned articles.

---

Note: The functions provided in this directory are designed to work together. The output of `fetch_articles()` should be the input to `process_articles()`. The final output of `process_articles()` can then be used as an input to the sentiment analysis.
