#main.py

from openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_articles
from data.process_articles import process_articles
from models.trading_strategy import decide_trades
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access the API keys
GPT_API_KEY = os.getenv("GPT_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")



def main():
    # Step 1: Fetch and process articles
    raw_articles = fetch_articles()
    processed_articles = process_articles(raw_articles)

    # Step 2: Analyze sentiment of articles
    sentiment_scores = analyze_sentiment(processed_articles)

    # Step 3: Decide trades based on sentiment scores
    trades_to_execute = decide_trades(sentiment_scores)

    # Step 4: Execute trades
    for trade in trades_to_execute:
        submit_order(trade)

if __name__ == "__main__":
    main()
