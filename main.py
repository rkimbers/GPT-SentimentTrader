from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_article, fetch_articles
from data.process_articles import process_article  
from models.trading_strategy import prepare_buy_orders, prepare_sell_orders, prepare_immediate_order
from dotenv import load_dotenv
from models.finance_utils import translate_symbols
from database.db_manager import connect_db, create_table, check_url_in_database, save_url_to_database
from my_twilio.messaging import send_order_text, send_immediate_order_text
from database.db_manager import fetch_sentiment_scores_from_database, get_all_records
from pprint import pprint

import threading
import schedule 
import queue
import os
import time

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def main():
    
    prompt_user()
    
    # Schedule fetch_and_analyze_articles to run every 10 minutes
    schedule.every(10).minutes.do(fetch_and_analyze_articles)

    # Schedule the task to be performed every Monday at market open (9:30 AM ET)
    schedule.every().monday.at("09:30").do(perform_trades)

    while True:
        # Run pending tasks
        schedule.run_pending()
        # Sleep for a while before checking for pending tasks again
        time.sleep(60)
        
        
def fetch_and_analyze_articles():
    # Fetch the URLs of the last 10 earnings articles from multiple sources
    urls_dict = fetch_articles()

    # Initialize an empty dictionary to store the processed articles
    sentiment_scores = {}

    for source, urls in urls_dict.items():
        for url in urls:
            # Check if this URL has been processed before
            if check_url_in_database(url):  
                print(f"The URL from '{source}' is already in the database.")
                continue

            processed_article = process_article(source, url)  
            if processed_article is not None:  
                # Analyze sentiment of each article and update sentiment_scores dictionary
                scores = analyze_sentiment(processed_article)
                for k, v in scores.items():
                    if k in sentiment_scores:
                        sentiment_scores[k].extend(v)
                    else:
                        sentiment_scores[k] = v

                    # Prepare and submit an immediate order
                    for score in v:
                        if abs(score) == 10:
                            side = "buy" if score > 0 else "sell"
                            order = prepare_immediate_order(k, score, side)
                            if order is not None:
                                print(f"Submitting immediate order: {order}")
                                result = submit_order(order)
                                if result:
                                    send_immediate_order_text(order)

            # Save the URL to database
            for company, score in scores.items():
                save_url_to_database(url, source, company, score[0])


def perform_trades():
    # Fetch the sentiment scores from the database
    sentiment_scores = fetch_sentiment_scores_from_database() 

    # Prepare buy and sell orders based on the sentiment scores
    buy_orders = prepare_buy_orders(sentiment_scores)
    sell_orders = prepare_sell_orders(sentiment_scores)

    # Execute trades
    successful_buy_orders = []
    successful_sell_orders = []
    
    for order in buy_orders + sell_orders:
        if order is not None:
            print(f"Submitting order: {order}")
            result = submit_order(order)
            if result:
                if order['side'] == 'buy':
                    successful_buy_orders.append(order)
                else:
                    successful_sell_orders.append(order)

    # Send the successful orders as sms
    if successful_buy_orders:
        send_order_text(successful_buy_orders)

    if successful_sell_orders:
        send_order_text(successful_sell_orders)


#prompt user to view database tables
def prompt_user():
    # Queue to share data between threads
    q = queue.Queue()

    # This function will run in a new thread
    def get_user_input():
        user_input = input("Would you like to view all current tables in the database? (Yes/No): ")
        q.put(user_input)

    # Start a thread that will run the get_user_input function
    thread = threading.Thread(target=get_user_input)
    thread.start()

    # Wait for 10 seconds or until the user enters their input
    thread.join(timeout=10)

    # Check if thread is still active
    if thread.is_alive():
        print("\nNo response. Continuing...")
        # Here we assume 'no' as default action if user does nothing
        user_input = "no"
    else:
        # If the thread has finished, get_user_input() has put something in the queue
        user_input = q.get()

    if user_input.lower() == "yes":
        # Fetch all records from the database and pretty print them
        records = get_all_records()
        print("\nContents of the 'articles' table:")
        pprint(records)
        print("End of database. Confinuting...")
    elif user_input.lower() == "no":
        print("Continuing without displaying tables.")
    else:
        print("Invalid input. Continuing with default action.")
        
if __name__ == "__main__":
    main()
