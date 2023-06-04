# sentiment_analysis.py
import os
import openai
from .finance_utils import get_symbol


def analyze_sentiment(articles):

    """
    Function to analyze the sentiment of a list of articles using OpenAI's GPT API.

    Parameters:
    articles: A list of dictionaries. Each dictionary represents an article and has a 'content' key.

    Returns:
    A dictionary with stock symbols as keys and sentiment scores as values.
    """

    # Use the OpenAI API key to authenticate
    openai.api_key = os.getenv("OPENAI_API_KEY")    
    
    scores = {}

    for article in articles:
        # Extract the article content
        content = article['content']

        # Prepare the prompt for the GPT API
        prompt = f"The following news article was found: \n\n\"{content}\"\n\n\
        Please identify any mentioned stock tickers and the sentiment (positive, negative, neutral) associated with each ticker. Format your response as follows: TickerName (sentiment)"

        # Send the prompt to the GPT API and get the response
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)

        # The model's response will be in the form 'Symbol: sentiment'
        model_response = response.choices[0].text.strip()

    # Process the response
        try:
            if "(" in model_response:
                # Handle format "CompanyName (Sentiment)"
                symbol, sentiment = model_response.split("(")
                sentiment = sentiment.rstrip(')').strip()  # Remove the closing parenthesis and strip whitespace
                symbol = symbol.strip()
                ticker = get_symbol(symbol)

            else:
                # Handle format "Ticker: CompanyName  Sentiment: SentimentValue"
                components = model_response.split("  ")
                
                if len(components) != 2:
                    print(f"Could not process the model's response: {model_response}")
                    continue

                symbol = components[0].split(":")[1].strip() 
                sentiment = components[1].split(":")[1].strip()
                ticker = get_symbol(symbol)

        # Your code to append the ticker and sentiment to the scores dictionary goes here


            # Calculate a sentiment score
            if sentiment.lower() == 'positive':
                score = 1
            elif sentiment.lower() == 'negative':
                score = -1
            else:
                score = 0

            # If the symbol(ticker) is already in the scores dictionary, add the new score to the existing score
            # Otherwise, add a new entry to the scores dictionary
            if ticker in scores:
                scores[ticker] += score
            else:
                scores[ticker] = score

        except ValueError:
            print(f"Could not process the model's response: {model_response}")

    # Return the scores dictionary
    print(scores)
    return scores