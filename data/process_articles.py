from bs4 import BeautifulSoup

def process_article(raw_article):
    """
    Processes a single raw HTML article.

    Parameters:
    raw_article: A string representing the raw HTML of an article.

    Returns:
    A dictionary representing the processed article. The dictionary has a 'content' key.
    """
    print("Starting process_article function...")

    # Parse the raw HTML content with BeautifulSoup
    soup = BeautifulSoup(raw_article, 'html.parser')

    # Extract the article content
    content_div = soup.find('div', {'class': 'caas-content'})
    if content_div is None:
        print(f"Warning: Could not find content div in article.")
        return None
    content = content_div.text.strip()

    # Return the processed article
    return {'content': content}