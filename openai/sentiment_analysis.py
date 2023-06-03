# sentiment_analysis.py
import os
from openai import OpenAI

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the OpenAI API key to authenticate
OpenAI.api_key = openai_api_key

def analyze_sentiment(processed_articles):
    """
    Function to analyze the sentiment of a list of articles using OpenAI's GPT API.

    Parameters:
    processed_articles: A list of dictionaries. Each dictionary represents an article and has a 'content' key and a 'symbol' key.

    Returns:
    A dictionary with stock symbols as keys and sentiment scores as values.
    """
    scores = {}

    for article in processed_articles:
        # Extract the article content and symbol
        content = article['content']
        symbol = article['symbol']

        # Prepare the prompt for the GPT API
        prompt = f"This is a sentiment analysis request. Please evaluate the sentiment of the following text: \"{content}\""

        # Send the prompt to the GPT API and get the response
        response = OpenAI.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=3)

        # Extract the sentiment from the response
        sentiment = response['choices'][0]['text'].strip().lower()

        # Calculate a sentiment score
        if sentiment == 'positive':
            score = 1
        elif sentiment == 'negative':
            score = -1
        else:
            score = 0

        # If the symbol is already in the scores dictionary, add the new score to the existing score
        # Otherwise, add a new entry to the scores dictionary
        if symbol in scores:
            scores[symbol] += score
        else:
            scores[symbol] = score

    # Return the scores dictionary
    return scores