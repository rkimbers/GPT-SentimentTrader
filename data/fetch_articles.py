# file: data/fetch_articles.py

import requests
from bs4 import BeautifulSoup

def fetch_articles():
    # This is a simplistic way to fetch articles. 
    # You may want to fetch articles from different sources and handle pagination, filtering, etc.
    
    url = input("Input article URL here")  # allows user to input single article
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')  # the tag might be different based on the news source
    
    return articles
