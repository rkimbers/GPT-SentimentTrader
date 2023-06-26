import os
import openai
import re

from openai.error import RateLimitError
from collections import defaultdict

def analyze_sentiment(article):
    # Use the OpenAI API key to authenticate
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Extract the article content
    content = article['content']

    # Calculate the number of tokens in the content (approximate)
    num_tokens = len(content) // 4  # one token ~= 4 characters

    # Skip articles that are too long
    if num_tokens > 4096:  # gpt-3.5-turbo has a maximum limit of 4096 tokens
        print(f"Skipping article with {num_tokens} tokens.")
        return {}

    # Prepare the system message
    system_message = """This is a news article sentiment analysis model. It identifies companies and associated sentiment from news articles. 
    Please format your response in this way: Nvidia: 6. 
    The sentiment score can only be an integer between -10 and 10, where -10 means extremely negative sentiment and 10 means extremely positive sentiment. 
    Numbers around zero mean mixed sentiment. DO NOT return a description."""

    # Suggestion prompt due to AI's inherent uncertainty
    suggestion_prompt = "Nvidia: 6"

    # Prepare the user message (the article content)
    user_message = content

    # Define the messages for the chat
    messages = [
        {"role": "system", "content": system_message},
        {"role": "system", "content": suggestion_prompt},
        {"role": "user", "content": user_message},
    ]
    
    # Send the chat messages to the GPT API and get the response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using the gpt-3.5-turbo model
            messages=messages,
            max_tokens=1000,  # Same as DaVinci
        )
    except RateLimitError:
        print("Hit rate limit, please try again later.")
        return {}  # Return an empty dictionary to signify failure

    # The model's response will be in the message content of the last choice
    model_response = response.choices[0].message.content.strip()

    print(model_response)

    # Process the response
    scores = defaultdict(list)
    try:
        responses = re.split(",|\\.", model_response)  # Separate different company-score pairs by comma or period

        for response in responses:
            response = response.strip()  # Remove leading/trailing whitespace

            if ":" in response:
                # Handle format "CompanyName: sentiment score"
                parts = response.split(":")
                company = parts[0].strip()

                # We extract only the score which is the first integer after the ":".
                # This time, handle potential trailing period
                sentiment_score = int(re.findall(r"-?\d+", parts[1].strip())[0])  # handle numbers with a trailing period

                # Add the sentiment score to the list of scores for the company
                scores[company].append(sentiment_score)

    except ValueError:
        print(f"Could not process the model's response: {model_response}")
        
    # Calculate the average sentiment score for each company

    return scores
