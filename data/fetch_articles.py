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
    try:
        # Make a request to the website
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Error occurred:", err)
        return []

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Initialize an empty list to hold the articles
    articles = []

    # This is a placeholder for the actual code that you would need to write to fetch and parse the articles from the website
    article_elements = soup.find_all('div', class_='article')

    for article_element in article_elements:
        # Extract the article content and symbol
        content = article_element.find('p').text
        symbol = article_element.find('span', class_='symbol').text

        # Add the article to the list of articles
        articles.append({
            'content': content,
            'symbol': symbol,
        })

    return articles


if __name__ == '__main__':
    # Ask the user for the URL of the website they want to analyze
    url = input("Please enter the URL of the website you want to analyze: ")

    # Fetch the articles from the given URL
    articles = fetch_articles(url)

    # Print the fetched articles
    for article in articles:
        print(f"Symbol: {article['symbol']}")
        print(f"Content: {article['content']}")
