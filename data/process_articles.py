from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re

# Function to filter out invisible HTML elements
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def process_articles(articles):
    processed_articles = []

    for url in articles:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'caas-body'
        article_body = soup.find('div', {'class': 'caas-body'})

        if article_body is not None:
            # Get all paragraph tags within the div
            paragraphs = article_body.find_all('p')

            article_content = ''

            # Extract the text from each paragraph tag and append it to the article content
            for para in paragraphs:
                article_content += para.text

            # Use a regular expression to remove any unwanted characters (e.g., newlines)
            article_content = re.sub('\n', '', article_content)

            # Append the processed article to the list
            processed_articles.append(article_content)
        else:
            print(f"Could not find the body of the article at {url}.")
            
    return processed_articles
