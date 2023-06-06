# fetch_articles.py

from bs4 import BeautifulSoup
import requests

def fetch_articles(url):
    """
    Fetches the raw HTML of an article from a given URL.

    Parameters:
    url: A string representing the URL from which to fetch the article.

    Returns:
    A string representing the raw HTML of the article.
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
        return None

    # Return the raw HTML content of the article
    return r.text


def article_input():
    urls = []
    while True:
        url = input("Enter an article URL (or 'done' when finished): ")
        if url.lower() == 'done':
            break
        else:
            urls.append(url)
    return urls

if __name__ == '__main__':
    # Ask the user for the URLs of the website they want to analyze
    urls = article_input()

    # Fetch the articles from the given URLs
    articles = fetch_articles(urls)

    # Print the fetched articles
    #for article in articles:
        #print(f"Content: {article['content']}")
