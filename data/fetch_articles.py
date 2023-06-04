# fetch_articles.py

from bs4 import BeautifulSoup
import requests

def fetch_articles(url):
    
    """
    Fetches the raw HTML of articles from a given URL.

    Parameters:
    url: A string representing the URL from which to fetch articles.

    Returns:
    A list of strings. Each string represents the raw HTML of an article.
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

    # Return the raw HTML content of each article
    return [r.text]

def article_input():
    try:
        url = input("Please enter the URL of the website you want to analyze: ")
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        exit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit()
    
    return url

if __name__ == '__main__':
    # Ask the user for the URL of the website they want to analyze
    url = input("Please enter the URL of the website you want to analyze: ")

    # Fetch the articles from the given URL
    articles = fetch_articles(url)

    # Print the fetched articles
    #for article in articles:
        #print(f"Content: {article['content']}")
