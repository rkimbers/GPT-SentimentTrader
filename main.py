from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_article, fetch_articles
from data.process_articles import process_article  
from models.trading_strategy import prepare_buy_orders, prepare_sell_orders
from dotenv import load_dotenv
from models.finance_utils import translate_symbols

import os

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    # Step 1: Fetch and process articles

    # Fetch the URLs of the last 10 earnings articles
    urls = fetch_articles()
    
    # Initialize an empty dictionary to store the processed articles
    # Fetch and process each article
    sentiment_scores = {}
    for url in urls:
        article_html = fetch_article(url)
        processed_article = process_article(article_html)  # Updated this line
        if processed_article is not None:  # Added this line to avoid appending None
            # Analyze sentiment of each article and update sentiment_scores dictionary
            scores = analyze_sentiment(processed_article)
            for k, v in scores.items():
                if k in sentiment_scores:
                    sentiment_scores[k].append(v)
                else:
                    sentiment_scores[k] = [v]
    
    # Translate sentiment_scores keys from company names to symbols
    sentiment_scores = translate_symbols(sentiment_scores)

    # Step 2: Decide trades based on sentiment scores
    buy_orders = prepare_buy_orders(sentiment_scores)
    sell_orders = prepare_sell_orders(sentiment_scores)

    # Print the orders
    #print(buy_orders)
    #print(sell_orders)

    # Step 3: Execute trades
    for order in buy_orders + sell_orders:
        print(f"Submitting order: {order}")
        submit_order(order)


if __name__ == "__main__":
    main()
