from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_article, fetch_articles
from data.process_articles import process_article  
from models.trading_strategy import prepare_buy_orders, prepare_sell_orders, prepare_immediate_order
from dotenv import load_dotenv
from models.finance_utils import translate_symbols
from database.db_manager import connect_db, create_table, check_url_in_database, save_url_to_database
from my_twilio.messaging import send_order_text, send_immediate_order_text
from database.db_manager import get_all_tables, get_all_records
from pprint import pprint

import threading
import os

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    
    prompt_user()
    
    # Fetch the URLs of the last 10 earnings articles from multiple sources
    urls_dict = fetch_articles()
    
    # Initialize an empty dictionary to store the processed articles
    sentiment_scores = {}

    for source, urls in urls_dict.items():
        for url in urls:
            # Check if this URL has been processed before
            if check_url_in_database(url):  # You will need to implement this function
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

                    # Check if any sentiment score is extreme
                    if abs(score) == 10:
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

    # Translate sentiment_scores keys from company names to symbols
    sentiment_scores = translate_symbols(sentiment_scores)

    # Average the sentiment scores
    for company in sentiment_scores:
        sentiment_scores[company] = sum(sentiment_scores[company]) / len(sentiment_scores[company])

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

    # Send the successful orders as messages
    if successful_buy_orders:
        send_order_text(successful_buy_orders)

    if successful_sell_orders:
        send_order_text(successful_sell_orders)


#prompt user to view database tables
def prompt_user():
    # Prompt the user to check if they want to view the tables
    user_input = input("Would you like to view all current tables in the database? (Yes/No): ")

    # Start a 10-second timer
    timer = threading.Timer(10.0, lambda: print("\nNo response. Continuing..."))
    timer.start()

    if user_input.lower() == "yes":
        # Cancel the timer
        timer.cancel()

        # Fetch all records from the database and pretty print them
        records = get_all_records()
        print("\nContents of the 'articles' table:")
        pprint(records)
    elif user_input.lower() == "no":
        # Cancel the timer
        timer.cancel()

        print("Continuing without displaying tables.")
    else:
        print("Invalid input. Please answer with 'Yes' or 'No'.")


if __name__ == "__main__":
    main()
