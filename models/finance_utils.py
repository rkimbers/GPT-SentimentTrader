# finance_utils.py
import requests
import os

def get_symbol(company_name):
    """
    Function to get the ticker symbol of a company using the Alpha Vantage API.

    Parameters:
    company_name: The name of the company

    Returns:
    The ticker symbol of the company, or None if no match is found.
    """

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
