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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from .fetch_articles import create_webdriver, is_valid_url #running main
#from fetch_articles import create_webdriver
#from fetch_articles import * #testing file
import http.cookiejar
import requests
from bs4 import BeautifulSoup


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
            if source == 'bloomberg':
                with create_webdriver() as driver:
                    # Pass the URL to the bypass function
                    page_source = bloomberg_bypass(driver, url)
                
                soup = BeautifulSoup(page_source, 'html.parser')
                content_div = soup.find('div', class_=div_classes[source])
                if content_div is not None:
                    content = content_div.text
                    article = {'content': content}  # Store the content in a dictionary
                    return article
                else:
                    logging.error(f"[{datetime.datetime.now()}] No content found for {url} in {source}")
                    return None
            else:
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


def bloomberg_bypass(driver, url):
    driver.get(url)
    
    # Check if the page is a CAPTCHA page
    if "Bloomberg - Are you a robot?" in driver.title:
        # Bypass the CAPTCHA
        solve_captcha(driver)
        
        # Wait for the page to load after solving CAPTCHA
        WebDriverWait(driver, 10).until(EC.title_contains("Bloomberg"))

    page_source = driver.page_source
    return page_source

def solve_captcha(driver):
    # Introduce a loop to wait until the iframe appears
    iframe_titles = [None]
    counter = 0
    while None in iframe_titles and counter < 30:
        time.sleep(2)
        counter += 1

        # Execute JavaScript to get iframe titles
        iframe_titles = driver.execute_script("""
            let iframes = Array.from(document.getElementsByTagName('iframe'));
            let titles = iframes.map(iframe => iframe.getAttribute('title'));
            return titles;
        """)

        print(iframe_titles)  # Print the iframe titles

    # Iterate over the iframe titles
    for title in iframe_titles:
        if title is not None and "Human verification challenge" in title:
            iframe = driver.find_element(By.XPATH, f'//iframe[@title="{title}"]')
            driver.switch_to.frame(iframe)
            break
    else:
        print("CAPTCHA iframe not found.")
        return

    # Switch to the CAPTCHA iframe
    driver.switch_to.frame(iframe)

    # Find and interact with the CAPTCHA element
    captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'px-captcha')))

    # Perform the click and hold action
    action = ActionChains(driver)
    action.click_and_hold(captcha_element).perform()

    # Wait for the required duration
    time.sleep(30)

    # Release the click
    action.release().perform()

    # Switch back to the default content
    driver.switch_to.default_content()


def get_captcha_token(driver):
    captcha_frame = driver.find_element(By.CSS_SELECTOR, 'div[data-analytics-area="body"] > iframe')
    captcha_iframe = captcha_frame.get_attribute("src")
    token = captcha_iframe.split("token=")[1].split("&")[0]
    return token


if __name__ == '__main__':
    urls = bloomberg_fetch_articles()
    #print(urls)
    #urls = urls[0]
    #print(urls)
    #print(process_article("bloomberg",urls))