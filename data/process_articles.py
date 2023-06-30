from bs4 import BeautifulSoup
from .fetch_articles import fetch_article, create_webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os


def process_article(source, url):
    
    email = os.getenv("EMAIL")
    
    """
    Processes a single raw HTML article.

    Parameters:
    source: A string representing the source of the article.
    url: A string representing the URL of the article.

    Returns:
    A dictionary representing the processed article. The dictionary has a 'content' key.
    """
    print(f"Starting process_article function for {source}...")

    # Define the div class for each source
    div_classes = {
        "yahoo_finance": "caas-content",
        "reuters": "article-body__content__17Yit",
        "investing_com": "WYSIWYG articlePage",
        "bloomberg": "body-content",  
        "market_watch": "article__content",
        #"business_insider": "news-content"
    }

    if source == 'bloomberg':
        try:
            # Use Selenium for Bloomberg articles
            with create_webdriver() as driver:
                driver.get(url)

                # Fill out the email field and click the submit button
                # Replace 'input[type="email"]' and 'button[type="submit"]' with the actual selectors
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))).send_keys(email)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

                # Wait for the page to load
                time.sleep(3)  # Adjust this value based on your internet speed

                # Extract the article content
                content_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, div_classes[source])))
                content = content_div.text

        except NoSuchElementException:
            print(f"Failed to fetch or process article from Bloomberg at {url}. Please check the selectors for email field and submit button.")
            return None
        except Exception as e:
            print(f"An error occurred while processing the article from Bloomberg at {url}. Error message: {e}")
            return None    
    else:
        # Get the raw HTML content of the article using fetch_article function
        raw_article = fetch_article(url)

        # Check if the raw_article is None before proceeding
        if raw_article is None:
            print(f"Failed to fetch article from {url}")
            return None

        # Parse the raw HTML content with BeautifulSoup
        soup = BeautifulSoup(raw_article, 'html.parser')

        # Extract the article content
        content_div = soup.find('div', {'class': div_classes[source]})
        if content_div is None:
            print(f"Warning: Could not find content div in article from {source}.")
            return None
        content = content_div.text.strip()

    # Return the processed article
    return {'content': content}
