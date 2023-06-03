from openai.sentiment_analysis import analyze_sentiment
from alpaca.trading import submit_order
from data.fetch_articles import fetch_articles
from data.process_articles import process_articles
from models.trading_strategy import decide_trades

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
