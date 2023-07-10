# finance_utils.py
import requests
import os
import logging
from typing import List, Dict

failed_tickers = set()

def compile_and_average_scores(score_lists):
    if isinstance(score_lists, float):
        return score_lists
    elif isinstance(score_lists[0], list):
        flat_list = [score for sublist in score_lists for score in sublist]
    else:
        flat_list = score_lists
    return sum(flat_list) / len(flat_list)


def translate_symbols(scores_dict):
    translated_scores = {}
    for company in scores_dict.keys():
        ticker_symbol = get_symbol(company)
        if ticker_symbol is None:
            raise Exception(f"Could not translate company name {company} to symbol")
        translated_scores[ticker_symbol] = scores_dict[company]
    return translated_scores


def get_symbol(company_name):
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    BASE_URL = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH"
    params = {
        "keywords": company_name,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Request to Alpha Vantage API failed: {response.content}") 
    data = response.json()
    if 'bestMatches' not in data:
        logging.error(f"Alpha Vantage API response does not contain 'bestMatches': {data}")
        return None
    for match in data['bestMatches']:
        if match['4. region'] == "United States":
            return match['1. symbol']
    if data['bestMatches']:
        # If no match was found in the US, return the first match regardless of region
        return data['bestMatches'][0]['1. symbol']
    # If no match was found at all
    logging.info(f"No matching symbol found for company name: {company_name}")
    return None


def get_share_price(ticker):
    if ticker in failed_tickers:
        return None  # skip unsupported tickers
    try:
        ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f"Non-200 response for ticker {ticker}: {response.content}")
            failed_tickers.add(ticker)  # add this
            return None  # change from raising an exception to returning None
        data = response.json()
        if "Time Series (5min)" in data:
            recent_timestamp = max(data["Time Series (5min)"].keys())
            recent_price = data["Time Series (5min)"][recent_timestamp]["4. close"]
            return float(recent_price)
        else:
            logging.error(f"No price data found for ticker {ticker}: {data}")
            failed_tickers.add(ticker)  # add this
            return None  # change from raising an exception to returning None
    except Exception as e:
        logging.error(f"Error getting price data for {ticker}: {str(e)}")
        failed_tickers.add(ticker)
        return None


def prepare_trades(sentiment_scores):
    trades_preparation = []
    for company, sentiment_scores_list in sentiment_scores.items():
        symbol = get_symbol(company)
        if symbol is None:
            logging.error(f"Unable to find symbol for company {company}")
            continue  # continue to the next company if we cannot find the symbol
        share_price = get_share_price(symbol)
        if share_price is None:
            logging.error(f"Unable to get price for ticker {symbol} ({company})")
            failed_tickers.add(symbol)
            continue  # continue to the next company if we cannot get the share price
        avg_sentiment_score = compile_and_average_scores(sentiment_scores_list)
        trades_preparation.append({
            'symbol': symbol,
            'sentiment_score': avg_sentiment_score,
            'share_price': share_price,
        })
    return trades_preparation


def calculate_total_sentiment(trades_preparation):
    total_sentiment = sum([trade['sentiment_score'] for trade in trades_preparation])
    if total_sentiment is None:
        raise Exception("Error occurred while calculating total sentiment")
    return total_sentiment
