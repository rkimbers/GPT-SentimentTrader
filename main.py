from my_openai.sentiment_analysis import analyze_sentiment
from my_alpaca.trading import submit_order
from data.fetch_articles import fetch_article, fetch_articles
from data.process_articles import process_article  
#from models.trading_strategy import decide_trades
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def main():
    # Step 1: Fetch and process articles

    # Fetch the URLs of the top 5 earnings articles
    urls = fetch_articles()
    
    # Initialize an empty list to store the processed articles
    # Fetch and process each article
    processed_articles = []
    for url in urls:
        article_html = fetch_article(url)
        processed_article = process_article(article_html)  # Updated this line
        if processed_article is not None:  # Add this line to avoid appending None
            processed_articles.append(processed_article)

    # Step 2: Analyze sentiment of articles
    sentiment_scores = []
    for article in processed_articles:
        score = analyze_sentiment(article)
        if score is not None:  # Add this line to avoid appending None
            sentiment_scores.append(score)

    print(sentiment_scores)
    # Step 3: Decide trades based on sentiment scores
    #trades_to_execute = decide_trades(sentiment_scores)

    #print(trades_to_execute)
    # Step 4: Execute trades
    #for trade, score in trades_to_execute.items():
    #    submit_order({trade: score})

if __name__ == "__main__":
    main()
