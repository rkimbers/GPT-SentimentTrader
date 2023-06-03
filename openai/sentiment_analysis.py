# sentiment_analysis.py
import os
import openai

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the OpenAI API key to authenticate
openai.api_key = openai_api_key

def analyze_sentiment(articles):
    """
    Function to analyze the sentiment of a list of articles using OpenAI's GPT API.

    Parameters:
    articles: A list of dictionaries. Each dictionary represents an article and has a 'content' key.

    Returns:
    A dictionary with stock symbols as keys and sentiment scores as values.
    """
    scores = {}

    for article in articles:
        # Extract the article content
        content = article['content']

        # Prepare the prompt for the GPT API
        prompt = f"The following news article was found: \n\n\"{content}\"\n\n\
        Please identify any mentioned stock tickers and the sentiment (positive, negative, neutral) associated with each ticker."

        # Send the prompt to the GPT API and get the response
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)

        # The model's response will be in the form 'Symbol: sentiment'
        model_response = response.choices[0].text.strip()

        # Process the response
        try:
            symbol, sentiment = model_response.split(":")
            symbol = symbol.strip()
            sentiment = sentiment.strip().lower()

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

        except ValueError:
            print(f"Could not process the model's response: {model_response}")

    # Return the scores dictionary
    return scores