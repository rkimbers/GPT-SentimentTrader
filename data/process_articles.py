import os
import time
import datetime
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .fetch_articles import fetch_article, create_webdriver


def process_article(source, url, retries=3):
    email = os.getenv("EMAIL")
    logging.info(f"[{datetime.datetime.now()}] Starting process_article function for {source}...")

    div_classes = {
        "yahoo_finance": "caas-content",
        "reuters": "article-body__content__17Yit",
        "investing_com": "WYSIWYG articlePage",
        "bloomberg": "body-content",
        "market_watch": "article__content",
    }

    for i in range(retries):
        try:
            if source == 'bloomberg':
                with create_webdriver() as driver:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))).send_keys(email)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
                    time.sleep(3)  # Adjust this value based on your internet speed
                    content_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, div_classes[source])))
                    content = content_div.text
            else:
                raw_article = fetch_article(url)
                if raw_article is None:
                    logging.error(f"[{datetime.datetime.now()}] Failed to fetch article from {url}")
                    return None
                soup = BeautifulSoup(raw_article, 'html.parser')
                content_div = soup.find('div', {'class': div_classes[source]})
                if content_div is None:
                    logging.warning(f"[{datetime.datetime.now()}] Warning: Could not find content div in article from {source}.")
                    return None
                content = content_div.text.strip()

            return {'content': content}

        except Exception as e:
            logging.error(f"[{datetime.datetime.now()}] An error occurred on attempt {i+1} of {retries} while processing the article from {source} at {url}. Error message: {e}")
            time.sleep(1)  # You can adjust this delay

    logging.error(f"[{datetime.datetime.now()}] Failed to process article from {source} at {url} after {retries} attempts")
    return None
