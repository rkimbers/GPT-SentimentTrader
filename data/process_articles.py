from bs4 import BeautifulSoup
from .fetch_articles import fetch_article
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        "bloomberg": "body-content",  # Update this to the correct class for Bloomberg
        "market_watch": "article__content",
        #"business_insider": "news-content"
    }

    if source == 'bloomberg':
        try:
            # Use Selenium for Bloomberg articles
            driver_path = "/usr/local/bin/chromedriver"
            driver = webdriver.Chrome(driver_path)
            driver.get(url)

            # Fill out the email field and click the submit button
            # Replace 'emailFieldId' and 'submitButtonId' with the actual ids
            email_field = driver.find_element_by_id('input[type="email"]')
            email_field.send_keys(email)
            submit_button = driver.find_element_by_id('button[type="submit"]')
            submit_button.click()

            # Wait for the page to load
            time.sleep(3)  # Adjust this value based on your internet speed

            # Extract the article content
            content_div = driver.find_element_by_class_name(div_classes[source])
            content = content_div.text

            driver.quit()
        except NoSuchElementException:
            print(f"Failed to fetch or process article from Bloomberg at {url}. Please check the ids for email field and submit button.")
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
