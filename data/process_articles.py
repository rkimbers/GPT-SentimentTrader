from bs4 import BeautifulSoup
from bs4.element import Comment
import re

# Function to filter out invisible HTML elements
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def process_articles(raw_articles):
    processed_articles = []
    
    for raw_article in raw_articles:
        soup = BeautifulSoup(raw_article, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)

        # Join all the visible text fragments together
        full_article_text = " ".join(t.strip() for t in visible_texts)

        # Optional: Remove extra whitespaces and newlines
        full_article_text = re.sub(r'\s+', ' ', full_article_text)

        processed_articles.append(full_article_text)

    return processed_articles
