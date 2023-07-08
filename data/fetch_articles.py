import os
import re
import time
import requests
import datetime
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from process_articles import bloomberg_bypass
#from .process_articles import bloomberg_bypass, fetch_article


@contextmanager
def create_webdriver(retries=5):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")

    # Chromedriver path
    webdriver_service = Service('/usr/local/bin/chromedriver')
    
    driver = None
    try:
        for i in range(retries):
            try:
                driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
                break
            except (WebDriverException, TimeoutException) as e:
                logging.error(f"[{datetime.datetime.now()}] WebDriverException occurred on attempt {i+1} of {retries}: {e}")
                if i < retries - 1:  # i is zero indexed
                    time.sleep(10)  # You can adjust this delay
                else:
                    raise
        yield driver
    except Exception as e:  # Catch exceptions that happened while the driver was being used.
        logging.error(f"[{datetime.datetime.now()}] Unexpected error: {e}")
        raise
    finally:
        if driver:
            driver.quit()


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_articles():
    article_urls_dict = {
        "yahoo_finance": yf_fetch_articles(),
        "reuters": reuters_fetch_articles(),
        "investing_com": investing_com_fetch_articles(),
        #"bloomberg": bloomberg_fetch_articles(),
        "market_watch": market_watch_fetch_articles(),
        "business_insider": business_insider_fetch_articles()
    }
    return article_urls_dict

def yf_fetch_articles():
    base_url = "https://finance.yahoo.com"
    topic_url = "https://finance.yahoo.com/most-active"

    try:
        response = requests.get(topic_url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
    except (requests.RequestException, Exception) as e:
        logging.error(f"Failed to fetch articles from Yahoo Finance: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith("/news"):
            article_links.append(base_url + href)
    logging.info(f"Successfully fetched articles from Yahoo Finance")
    return article_links[:10]  # Return only the first 10 article URLs


def reuters_fetch_articles():
    reuters_base_url = "https://www.reuters.com"
    reuters_topic_url = "https://www.reuters.com/business"
    
    with create_webdriver() as driver:
        driver.get(reuters_topic_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        article_links = []
        for link in soup.find_all('a', {'data-testid': 'Heading'}):
            class_list = link.get('class')
            if 'text__text__1FZLe' in class_list and 'text__dark-grey__3Ml43' in class_list and 'text__medium__1kbOh' in class_list:
                href = link.get('href')
                if href and href.startswith('/'):  # href could be a relative URL
                    article_links.append(reuters_base_url + href)
                    
    return article_links[:10]  # Return only the first 10 article URLs


def investing_com_fetch_articles():
    investing_com_base_url = "https://www.investing.com"
    investing_com_topic_url = "https://www.investing.com/news/stock-market-news"
    
    with create_webdriver() as driver:
        driver.get(investing_com_topic_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        article_links = []
        for article in soup.find_all('article', class_='js-article-item articleItem'):
            link = article.find('a')
            href = link.get('href')
            if href:
                article_links.append(investing_com_base_url + href)
                
    return article_links[:10]  # Return only the first 10 article URLs


def bloomberg_fetch_articles():
    bloomberg_base_url = "https://www.bloomberg.com"
    bloomberg_topic_url = "https://www.bloomberg.com/industries"

    with create_webdriver() as driver:
        # Pass the URL to the bypass function
        page_source = bloomberg_bypass(driver, bloomberg_topic_url)
        
    soup = BeautifulSoup(page_source, 'html.parser')
    elements = soup.find_all("a", href=re.compile("/news/articles/"))
    article_links = [bloomberg_base_url + element['href'] if element['href'].startswith('/') else element['href'] for element in elements]

    return article_links[-10:]  # Return only the last 10 article URLs.


def market_watch_fetch_articles():
    market_watch_base_url = "https://www.marketwatch.com"
    market_watch_topic_url = "https://www.marketwatch.com/markets"

    with create_webdriver() as driver:
        driver.get(market_watch_topic_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        article_links = []
        for article_div in soup.find_all('div', class_='article__content'):
            headline = article_div.find('h3', class_='article__headline')
            link = headline.find('a')
            href = link.get('href')
            if href and href.startswith('http'):  # make sure it's a valid URL
                article_links.append(href)

    return article_links[:10]  # Return only the first 10 article URLs


def business_insider_fetch_articles():
    business_insider_base_url = "https://markets.businessinsider.com"
    business_insider_topic_url = "https://markets.businessinsider.com/stocks"

    with create_webdriver() as driver:
        try:
            driver.get(business_insider_topic_url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for at least one article link to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.popular-articles__link")))

            articles = driver.find_elements(By.CSS_SELECTOR, "a.popular-articles__link")
            article_links = [article.get_attribute("href") for article in articles if article.get_attribute("href") and "/news/stocks/" in article.get_attribute("href")]
        except Exception as e:
            logging.error(f"Failed to fetch articles from Business Insider: {e}")
            return []

    return article_links[:10]  # Return only the first 10 article URLs
