from bs4 import BeautifulSoup
from .fetch_articles import fetch_article  # Add this import

def process_article(source, url):
    """
    Processes a single raw HTML article.

    Parameters:
    source: A string representing the source of the article.
    url: A string representing the URL of the article.

    Returns:
    A dictionary representing the processed article. The dictionary has a 'content' key.
    """
    print(f"Starting process_article function for {source}...")

    # Get the raw HTML content of the article using fetch_article function
    raw_article = fetch_article(url)

    # Check if the raw_article is None before proceeding
    if raw_article is None:
        print(f"Failed to fetch article from {url}")
        return None


    # Parse the raw HTML content with BeautifulSoup
    soup = BeautifulSoup(raw_article, 'html.parser')

    # Define the div class for each source
    div_classes = {
        "yahoo_finance": "caas-content",
        "reuters": "article-body__content__17Yit",
        "investing_com": "WYSIWYG articlePage",
        "bloomberg": "body-copy-v2 fence-body",
        "market_watch": "article__content",
        #"business_insider": "news-content"
    }

    # Extract the article content
    content_div = soup.find('div', {'class': div_classes[source]})
    if content_div is None:
        print(f"Warning: Could not find content div in article from {source}.")
        return None
    content = content_div.text.strip()

    # Return the processed article
    return {'content': content}
