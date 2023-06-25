from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

import requests
import re
import time

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Chromedriver path
webdriver_service = Service('/usr/local/bin/chromedriver')

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_article(url):
    # Validate URL
    if not is_valid_url(url):
        print(f"Invalid URL: {url}")
        return None

    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Choose Chrome Browser
        webdriver_service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        driver.get(url)

        # Wait for the page to load completely
        time.sleep(5)

        # Return the raw HTML content of the page
        html = driver.page_source

        driver.quit()
        return html

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def fetch_articles():
    article_urls_dict = {
        "yahoo_finance": yf_fetch_articles(),
        "reuters": reuters_fetch_articles(),
        "investing_com": investing_com_fetch_articles(),
        "bloomberg": bloomberg_fetch_articles(),
        "market_watch": market_watch_fetch_articles(),
        #"business_insider": business_insider_fetch_articles()
    }
    return article_urls_dict

def yf_fetch_articles():
    base_url = "https://finance.yahoo.com"
    topic_url = "https://finance.yahoo.com/most-active"

    response = requests.get(topic_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith("/news"):
            article_links.append(base_url + href)
    return article_links[:10]  # Return only the first 10 article URLs


def reuters_fetch_articles():
    reuters_base_url = "https://www.reuters.com"
    reuters_topic_url = "https://www.reuters.com/business"

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
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36")

    bloomberg_base_url = "https://www.bloomberg.com"
    bloomberg_topic_url = "https://www.bloomberg.com/markets"

    driver = webdriver.Chrome(options=options)
    driver.get(bloomberg_topic_url)

    elements = driver.find_elements("css selector", "a[href*='/news/articles/']")
    article_links = [element.get_attribute('href') for element in elements if element.get_attribute('href')]

    return article_links[:10]  # Return only the first 10 article URLs


def market_watch_fetch_articles():
    market_watch_base_url = "https://www.marketwatch.com"
    market_watch_topic_url = "https://www.marketwatch.com/markets"

    driver.get(market_watch_topic_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    article_links = []
    for article_div in soup.find_all('div', class_='article__content'):
        headline = article_div.find('h3', class_='article__headline')
        link = headline.find('a')
        href = link.get('href')
        if href:
            article_links.append(href)
    return article_links[:10]  # Return only the first 10 article URLs


def business_insider_fetch_articles():
    business_insider_base_url = "https://markets.businessinsider.com"
    business_insider_topic_url = "https://markets.businessinsider.com/news/stocks"
    
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver.get(business_insider_topic_url)
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for at least one article link to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.top-story__link, a.instrument-stories__link")))

    articles = driver.find_elements("css selector", "a.top-story__link, a.instrument-stories__link")
    article_links = [article.get_attribute("href") for article in articles if article.get_attribute("href") and "/news/stocks/" in article.get_attribute("href")]
    
    return article_links[:10]  # Return only the first 10 article URLs





if __name__ == '__main__':
   
    # Fetch the articles from the given URLs
    print(yf_fetch_articles()) #working
    print(reuters_fetch_articles()) #working
    print(investing_com_fetch_articles()) #working
    print(bloomberg_fetch_articles()) #working
    print(market_watch_fetch_articles()) #working
    #print(business_insider_fetch_articles())
   
    driver.quit()