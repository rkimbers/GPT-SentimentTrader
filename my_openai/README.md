# my_openai

The `my_openai` directory contains modules related to sentiment analysis using the OpenAI API. The main components are `__init__.py` and `sentiment_analysis.py`

## Files

### __init__.py

This is an initialization file that makes Python treat the directories as containing packages.

### sentiment_analysis.py

This file contains the `analyze_sentiment()` function that connects to OpenAI's API and returns sentiment analysis scores for given input articles. 

#### `analyze_sentiment()`
The function uses OpenAI's GPT-3.5 model to analyze the sentiment. The function requires a list of preprocessed articles as raw text. It then sends this text to OpenAI's API for sentiment analysis. After receiving the response, the function processes it to compute a sentiment score for each ticker symbol. The output is a dictionary where keys are the ticker symbols - company names, truly and values are the sentiment scores.

## Usage

Import the necessary functions from each file as needed. For example, to use the `analyze_sentiment()` function in your code, you would use:

```python
from my_openai.sentiment_analysis import analyze_sentiment
