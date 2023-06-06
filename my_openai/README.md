# my_openai

The `my_openai` directory contains modules related to sentiment analysis using the OpenAI API. The main components are `__init__.py`, `sentiment_analysis.py`, and `finance_utils.py`.

## __init__.py

This is an initialization file that makes Python treat the directories as containing packages.

## sentiment_analysis.py

This file contains the `analyze_sentiment()` function that connects to OpenAI's API and returns sentiment analysis scores for given input articles. The function requires a dictionary of preprocessed articles where keys are ticker symbols and values are concatenated article texts. The output is a dictionary where keys are the ticker symbols and values are the sentiment scores.

The function uses OpenAI's GPT-3.5 model to analyze the sentiment. Before making the API call, the function preprocesses the text, removes extraneous information, and concatenates it. It then sends this text to OpenAI's API for sentiment analysis. After receiving the response, the function processes it to compute a sentiment score for each ticker symbol.

## finance_utils.py

This file contains utility functions for the finance-related tasks in the project. The function `get_symbol()` is used to convert a given company name to ticker symbol.

## Usage

Import the necessary functions from each file as needed. For example, to use the `analyze_sentiment()` function in your code, you would use:

```python
from my_openai.sentiment_analysis import analyze_sentiment
