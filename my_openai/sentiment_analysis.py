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

        # Prepare the system message
        system_message = "This is a news article sentiment analysis model. It identifies companies and associated sentiment from news articles. Please format your response in this way: Company (Sentiment). The sentiment can only be positive, neutral, or negative"

        # Prepare the user message (the article content)
        user_message = content
        
        #Suggestion prompt due to AI's inherent uncertainty
        suggestion_prompt = "For example: 'Nvidia (Positive)'"


        # Define the messages for the chat
        # Define the messages for the chat
        messages = [
        {"role": "system", "content": system_message},
        {"role": "system", "content": suggestion_prompt},
        {"role": "user", "content": user_message},
        ]


        # Send the chat messages to the GPT API and get the response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Using the gpt-3.5-turbo model
        messages=messages,
        max_tokens=1000,  # Same as DaVinci
        )

        # The model's response will be in the message content of the last choice
        model_response = response.choices[0].message.content.strip()
        
        print(model_response)
        
        #DaVinci version
        #response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)

        # Process the response
        try:
            responses = model_response.split(",")  # Separate different ticker sentiment pairs

            for response in responses:
                response = response.strip()  # Remove leading/trailing whitespace

                if "(" in response:
                    # Handle format "CompanyName (Sentiment)"
                    symbol, sentiment = response.split("(")
                    sentiment = sentiment.rstrip(')').strip()  # Remove the closing parenthesis and strip whitespace
                    symbol = symbol.strip()
                    ticker = get_symbol(symbol)

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