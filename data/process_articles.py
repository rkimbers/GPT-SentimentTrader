import os
import time
import datetime
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
#from .fetch_articles import create_webdriver
from fetch_articles import create_webdriver
from fetch_articles import *


def process_article(source, url, retries=3):
    logging.info(f"[{datetime.datetime.now()}] Starting process_article function for {source}...")

    div_classes = {
        "yahoo_finance": "caas-content",
        "reuters": "article-body__content__17Yit",
        "investing_com": "WYSIWYG articlePage",
        "bloomberg": "body-content",
        "market_watch": "article__content",
        "business_insider": "content-lock-content",
    }

    for i in range(retries):
        try:
            html = fetch_article(url)
            if html is not None:
                soup = BeautifulSoup(html, 'html.parser')
                content_div = soup.find('div', class_=div_classes[source])
                if content_div is not None:
                    content = content_div.text
                    article = {'content': content}  # Store the content in a dictionary
                    return article
                else:
                    logging.error(f"[{datetime.datetime.now()}] No content found for {url} in {source}")
                    return None
            else:
                logging.error(f"[{datetime.datetime.now()}] Failed to fetch HTML for {url}")
                return None
        except WebDriverException as e:
            logging.error(f"[{datetime.datetime.now()}] WebDriverException occurred on attempt {i+1} of {retries}: {e}")
            if i < retries - 1:  # i is zero indexed
                time.sleep(1)  # You can adjust this delay
                continue
            else:
                raise
        except Exception as e:
            logging.error(f"[{datetime.datetime.now()}] Unexpected error: {e}")
            raise


# Take mercy on me. I know this naming is terrible, I am too shy to fix it.
def fetch_article(url, retries=3):
    # Validate URL
    if not is_valid_url(url):
        logging.error(f"[{datetime.datetime.now()}] Invalid URL: {url}")
        return None

    for i in range(retries):
        try:
            with create_webdriver() as driver:
                driver.get(url)
                # Wait for the page to load completely
                time.sleep(5)
                # Return the raw HTML content of the page
                html = driver.page_source

            return html
        except (Exception, TimeoutException) as e:
            logging.error(f"[{datetime.datetime.now()}] Error occurred on attempt {i+1} of {retries}: {e}")
            time.sleep(1)  # You can adjust this delay

    logging.error(f"[{datetime.datetime.now()}] Failed to fetch article from {url} after {retries} attempts")
    return None


def bloomberg_bypass(url):
    with create_webdriver() as driver:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        time.sleep(3)  # Adjust this value based on your internet speed
        content_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, div_classes[source])))
        content = content_div.text
        return content


if __name__ == '__main__':
    urls = business_insider_fetch_articles()
    print(process_article("business_insider",urls))