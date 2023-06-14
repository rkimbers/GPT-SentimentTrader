# GPT-SentimentTrader

GPT-SentimentTrader is a Python-based trading bot that employs sentiment analysis techniques using OpenAI's GPT model on news articles to guide trading decisions. This bot was built with the intent to explore the potential of leveraging AI for automated trading.

## Project Overview

The bot operates through a sequence of actions that include fetching articles from the internet, performing sentiment analysis using the GPT model, implementing a trading strategy based on the sentiment scores, and executing trades via the Alpaca Markets API.

The project is structured in the following way:

```
/my_trading_bot
    /my_openai
        - __init__.py
        - sentiment_analysis.py
    /my_alpaca
        - __init__.py
        - trading.py
    /data
        - __init__.py
        - fetch_articles.py
        - process_articles.py
    /models
        - __init__.py
        - trading_strategy.py
        - finance_utils.py
        - account_utils.py
    - main.py
    - requirements.txt 
```
    
    
## Modules
Each directory contains modules that fulfill specific functions within the bot:

| Directory | Description |
|-----------|-------------|
| [my_openai](/my_openai)    | This directory contains the `sentiment_analysis.py` module, which interacts with OpenAI's GPT-3.5 API to analyze the sentiment of news articles. |
| [my_alpaca](/my_alpaca)    | The `trading.py` module in this directory manages all interactions with the Alpaca API. It is responsible for executing trading decisions made by the bot. |
| [data](/data)        | This directory houses two modules. `fetch_articles.py` fetches articles from the internet, and `process_articles.py` preprocesses these articles to prepare them for sentiment analysis. |
| [models](/models)    | This directory includes the `trading_strategy.py` module which implements the bot's trading strategy. Other dependency modules are housed here to act as support for preparing trades. |
| [main.py](/main.py)  | The main script that ties all the modules together to enable the bot's functionality. |
| [requirements.txt](/requirements.txt) | The file containing the list of dependencies and libraries required for the project. |

## Setup & Installation

To set up and run GPT-BasedTradingBot on your local machine, follow these steps:

1. Clone the repository to your local machine: `git clone https://github.com/rkimbers/GPT-SentimentTrader.git`
2. Navigate to the project directory: `cd GPT-SentimentTrader`
3. Install the required Python packages: `pip install -r requirements.txt`
4. Update the required API keys in `main.py`, `alpaca/trading.py`, and `openai/sentiment_analysis.py`.

## Usage

Run the bot by executing the main script: `python main.py` The bot will fetch news articles, analyze their sentiment, determine trading actions, and execute trades.

## Dependencies

GPT-SentimentTrader leverages a number of Python packages:

- OpenAI's GPT for sentiment analysis
- Alpaca's API for executing trades
- Alpha Vantage's API for finance utilities. I use the '75 requests/min' tier currently
- BeautifulSoup and Requests for fetching and parsing web articles


## Contributions 
Contributions to GPT-SentimentTrader are welcome! If you'd like to contribute, please fork the repository and make changes as you'd like. 

Pull requests are warmly welcomed.

If you have any questions or need further clarification about the bot, feel free to open an issue to discuss what you would like to change or add.

## License

The GPT-SentimentTrader application is licensed under the [MIT License](/LICENSE).
