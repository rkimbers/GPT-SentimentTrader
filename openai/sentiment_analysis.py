# sentiment_analysis.py
import os
from openai import OpenAI

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the OpenAI API key to authenticate
OpenAI.api_key = openai_api_key

def analyze_sentiment(processed_articles):
    """
    Analyze the sentiment of a list of processed articles.

    :param processed_articles: A list of strings, where each string is a processed article.
    :return: A dictionary where the keys are article indices and the values are sentiment scores.
    """
    sentiment_scores = {}

    for i, article in enumerate(processed_articles):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=article,
            temperature=0.7,
            max_tokens=150
        )
        
        # Assume the returned text is a sentiment score.
        # In reality, you'd want to extract or calculate the sentiment score from the returned text.
        sentiment_scores[i] = response.choices[0].text.strip()

    return sentiment_scores
