from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re

# Function to filter out invisible HTML elements
#def tag_visible(element):
#    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#        return False
#    if isinstance(element, Comment):
#        return False
#    return True

def process_articles(raw_articles):
    """
    Processes a list of raw HTML articles.

    Parameters:
    raw_articles: A list of strings. Each string represents the raw HTML of an article.

    Returns:
    A list of dictionaries representing the processed articles. Each dictionary has a 'content' key.
    """
    print("Starting process_articles function...")
    
    processed_articles = []

    for raw_article in raw_articles:
        # Parse the raw HTML content with BeautifulSoup
        soup = BeautifulSoup(raw_article, 'html.parser')

        # Extract the article content
        content = soup.find('div', {'class': 'caas-body'}).text.strip()

        # Add the article to the list of processed articles
        processed_articles.append({'content': content})

    #print("Processed articles:", processed_articles)
    return processed_articles