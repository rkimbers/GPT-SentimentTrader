# file: main.py
from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_articles
from data.process_articles import process_article  
from models.trading_strategy import prepare_buy_orders, prepare_sell_orders, prepare_immediate_order
from database.db_manager import create_table, check_url_in_database, save_url_to_database
from my_twilio.messaging import send_order_text, send_immediate_order_text
from database.db_manager import fetch_sentiment_scores_from_database, get_all_records, delete_all_records
from my_twilio.messaging import send_market_open_message
from dotenv import load_dotenv
from tabulate import tabulate
from pprint import pprint
import threading
import schedule 
import queue
import os
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('debug.log'),
                        logging.StreamHandler()
                    ])

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    create_table()
    
    print_all_records()
    
    #delete_all_records()
        
    #fetch_and_analyze_articles()

    schedule.every(10).minutes.do(fetch_and_analyze_articles)
    schedule.every().monday.at("09:30").do(perform_trades)
    schedule.every().monday.at("10:00").do(delete_all_records)

    while True:
        schedule.run_pending()
        time.sleep(60)


def fetch_and_analyze_articles():
    logging.info("Starting fetch_and_analyze_articles()")
    try:
        urls_dict = fetch_articles()
        sentiment_scores = {}
        for source, urls in urls_dict.items():
            for url in urls:
                if check_url_in_database(url):
                    logging.info(f"The URL from '{source}' is already in the database.")
                    continue
                processed_article = process_article(source, url)
                scores = {}
                if isinstance(processed_article, dict) and 'content' in processed_article:
                    scores = analyze_sentiment(processed_article)
                    for k, v in scores.items():
                        if k in sentiment_scores:
                            sentiment_scores[k].extend(v)
                        else:
                            sentiment_scores[k] = v
                        for score in v:
                            if score == 10:
                                side = "buy"
                                order = prepare_immediate_order(k, score, side)
                                if order is not None:
                                    logging.info(f"Submitting immediate order: {order}")
                                    result = submit_order(order)
                                    if result:
                                        try:
                                            send_immediate_order_text(order)
                                        except Exception as e:
                                            logging.error(f"Failed to send immediate order text: {e}")
                else:
                    logging.error("Processed article is not in the expected format.")
                for company, score_list in scores.items():
                    try:
                        if company in sentiment_scores:
                            sentiment_scores[company].extend(score_list)
                        else:
                            sentiment_scores[company] = score_list                         
                        for score in score_list:
                            if score == 10:
                                side = "buy"
                                order = prepare_immediate_order(company, score, side)
                                if order is not None:
                                    logging.info(f"Submitting immediate order: {order}")
                                    result = submit_order(order)
                                    if result:
                                        try:
                                            send_immediate_order_text(order)
                                        except Exception as e:
                                            logging.error(f"Failed to send immediate order text: {e}")                                     
                        save_url_to_database(url, source, company, score_list[0])                      
                    except Exception as e:
                        logging.error(f"Failed to save URL to database: {e}")
    except Exception as e:
        logging.error(f"Exception occurred in fetch_and_analyze_articles: {e}")
        raise


def perform_trades():
    successful_buy_orders = []
    successful_sell_orders = []
    try:
        sentiment_scores = fetch_sentiment_scores_from_database()
        buy_orders = prepare_buy_orders(sentiment_scores)
        sell_orders = prepare_sell_orders(sentiment_scores)
        buy_orders = [order for order in buy_orders if order['qty'] > 0]
        sell_orders = [order for order in sell_orders if order['qty'] > 0]
        for order in buy_orders + sell_orders:
            logging.info(f"Submitting order: {order}")
            result = submit_order(order)
            if result:
                if order['side'] == 'buy':
                    successful_buy_orders.append(order)
                else:
                    successful_sell_orders.append(order)
        try:
            if successful_buy_orders:
                send_order_text(successful_buy_orders)
        except Exception as e:
            logging.error(f"Exception occurred when sending buy orders text: {e}")
        try:
            if successful_sell_orders:
                send_order_text(successful_sell_orders)
        except Exception as e:
            logging.error(f"Exception occurred when sending sell orders text: {e}")
    except Exception as e:
        logging.error(f"Exception occurred in perform_trades: {e}")
        raise
    finally:
        if successful_buy_orders or successful_sell_orders:
            send_market_open_message("trades_executed")
        else:
            send_market_open_message("no_trades")


def print_all_records():
    records = get_all_records()
    logging.info("\nContents of the 'articles' table at startup:")
    logging.info(print_table(records))
    logging.info("End of database content at startup.\n")


def print_table(records):
    if not records:
        print("No records found.")
        return

    headers = ["ID", "URL", "Source", "Symbol", "Sentiment Score"]
    table = tabulate(records, headers=headers, tablefmt="fancy_grid")
    print(table)


def prompt_user():
    q = queue.Queue()
    def get_user_input():
        user_input = input("Would you like to view all current tables in the database? (Yes/No): ")
        q.put(user_input)
    thread = threading.Thread(target=get_user_input)
    thread.start()
    thread.join(timeout=10)
    if thread.is_alive():
        logging.info("\nNo response. Continuing...")
        user_input = "no"
    else:
        user_input = q.get()
    if user_input.lower() == "yes":
        records = get_all_records()
        logging.info("\nContents of the 'articles' table:")
        logging.info(pprint(records))
        logging.info("End of database. Continuing...")
    elif user_input.lower() == "no":
        logging.info("Continuing without displaying tables.")
    else:
        logging.error("Invalid input. Continuing with default action.")
        
if __name__ == "__main__":
    main()
