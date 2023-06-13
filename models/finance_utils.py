# finance_utils.py
import requests
import os

from typing import List, Dict

def translate_symbols(positions: List[Dict]) -> List[Dict]:
    translated_positions = []
    for position in positions:
        # Get ticker symbol for company name
        ticker_symbol = get_symbol(position['symbol'])

        # If a valid ticker symbol is returned, add it to the new position list
        if ticker_symbol:
            translated_positions.append({
                'symbol': ticker_symbol,
                'qty': position['qty']
            })
            
    return translated_positions

def get_symbol(company_name):

    # Your Alpha Vantage API Key
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    # The API endpoint
    BASE_URL = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH"

    # The search parameters
    params = {
        "keywords": company_name,
        "apikey": API_KEY
    }

    # Send a GET request to the API
    response = requests.get(BASE_URL, params=params)

    # Convert the response to JSON
    data = response.json()

    # If there are no matches, return None
    if not data.get('bestMatches'):
        return None

    # The response includes a list of matches. Loop over them to find the first match where the region is "United States".
    for match in data['bestMatches']:
        if match['4. region'] == "United States":
            # This match is in the United States.
            return match['1. symbol']

    # If no match for the United States is found, return None
    return None


# Gets share price given a ticker symbol
def get_share_price(ticker):
    
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"

    # Send the GET request and get the response
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()
    # Ensure the response contains the key "Time Series (5min)"
    if "Time Series (5min)" in data:
        # Get the most recent timestamp
        recent_timestamp = max(data["Time Series (5min)"].keys())

        # Get the closing price at the most recent timestamp
        recent_price = data["Time Series (5min)"][recent_timestamp]["4. close"]

        return float(recent_price)
    else:
        print(f"Unable to get price for ticker {ticker}.")
        return None
    

def prepare_trades(sentiment_scores):
    trades_preparation = []
    for company, sentiment_score in sentiment_scores.items():
        symbol = get_symbol(company)
        print(f"{company} symbol: {symbol}")  # Debugging line
        if symbol is not None:
            share_price = get_share_price(symbol)
            print(f"{company} share price: {share_price}")  # Debugging line
            trades_preparation.append({
                'symbol': symbol,
                'sentiment_score': sentiment_score,
                'share_price': share_price,
            })
    return trades_preparation


def calculate_total_sentiment(trades_preparation):
    return sum([trade['sentiment_score'] for trade in trades_preparation])
