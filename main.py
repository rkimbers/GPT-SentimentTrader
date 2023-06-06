#main.py

from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_articles
from data.fetch_articles import article_input
from data.process_articles import process_articles
from models.trading_strategy import decide_trades
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    # Step 1: Fetch and process articles

    # Gather URLs
    urls = article_input()
    articles = []
    # Fetch the articles for each URL
    for url in urls:
        fetched_article = fetch_articles(url)
        articles.append(fetched_article)

    processed_articles = process_articles(articles)

    # Step 2: Analyze sentiment of articles
    trades_to_execute = analyze_sentiment(processed_articles)

    # Step 3: Decide trades based on sentiment scores
    #trades_to_execute = decide_trades(sentiment_scores)

    # Step 4: Execute trades
    #trades_to_execute = {'NVDA': 1}
    for trade, score in trades_to_execute.items():
        submit_order({trade: score})

if __name__ == "__main__":
    main()




