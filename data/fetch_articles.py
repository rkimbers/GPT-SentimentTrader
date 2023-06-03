# fetch_articles.py

from bs4 import BeautifulSoup
import requests

def fetch_articles(url):
    
    """
    Fetch articles from a given URL.

    Parameters:
    url: A string representing the URL from which to fetch articles.

    Returns:
    A list of dictionaries. Each dictionary represents an article and has a 'content' key and a 'symbol' key.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }

    try:
        # Make a request to the website
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        if r.status_code == 404:
            print(f"Error 404: Page not found at {url}")
        else:
            print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Error occurred:", err)
        return []



    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Initialize an empty list to hold the articles
    articles = []

    # Fetch the article content using the appropriate class for Yahoo Finance
    article_element = soup.find('div', {'class':'caas-body'})

    if article_element:
        # Extract the article content
        content = article_element.text
        # Add the article to the list of articles
        articles.append({'content': content})

    return articles


if __name__ == '__main__':
    # Ask the user for the URL of the website they want to analyze
    url = input("Please enter the URL of the website you want to analyze: ")

    # Fetch the articles from the given URL
    articles = fetch_articles(url)

    # Print the fetched articles
    for article in articles:
        print(f"Content: {article['content']}")
