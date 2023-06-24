from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_article, fetch_articles
from data.process_articles import process_article  
from models.trading_strategy import prepare_buy_orders, prepare_sell_orders, prepare_immediate_order
from dotenv import load_dotenv
from models.finance_utils import translate_symbols
from database.db_manager import connect_db, create_table_if_not_exists, check_url_in_database, save_url_to_database
from my_twilio.messaging import send_order_text
import os

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    try:
        # Create the table if it doesn't already exist
        create_table_if_not_exists()

        # Fetch the URLs of the last 10 earnings articles from multiple sources
        urls_dict = fetch_articles()

        # Initialize an empty dictionary to store the processed articles
        sentiment_scores = {}

        for source, urls in urls_dict.items():
            for url in urls:
                # Check if this URL has been processed before
                if check_url_in_database(url): 
                    print(f"URL: {url} already processed. Skipping...")
                    continue

                processed_article = process_article(source, url)  
                if processed_article is not None:  
                    # Analyze sentiment of each article and update sentiment_scores dictionary
                    scores = analyze_sentiment(processed_article)
                    for k, v in scores.items():
                        if k in sentiment_scores:
                            sentiment_scores[k].append(v)
                        else:
                            sentiment_scores[k] = [v]

                        # Check if the sentiment score is extreme
                        if abs(v) == 10:
                            # Prepare and submit an immediate order
                            order = prepare_immediate_order(k, v) 
                            print(f"Submitting immediate order: {order}")
                            result = submit_order(order)
                            if result:
                                send_order_text(order)

                # Save the URL to database
                save_url_to_database(url)

        # Translate sentiment_scores keys from company names to symbols
        sentiment_scores = translate_symbols(sentiment_scores)

        # Prepare buy and sell orders based on the sentiment scores
        buy_orders = prepare_buy_orders(sentiment_scores)
        sell_orders = prepare_sell_orders(sentiment_scores)

        # Execute trades
        for order in buy_orders + sell_orders:
            print(f"Submitting order: {order}")
            result = submit_order(order)
            if result:
                send_order_text(order)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close database connection
        connect_db().close()

if __name__ == "__main__":
    main()
