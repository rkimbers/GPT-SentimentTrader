# GPT-SentimentTrader

GPT-SentimentTrader is a Python-based trading bot that employs sentiment analysis techniques using OpenAI's GPT models on news articles to guide trading decisions. This bot was built with the intent to leverage various APIs to compare AI trading to major index preformance. More info about the project's goals are below.

## Project Overview

The bot operates through a sequence of actions that include fetching articles from the internet, performing sentiment analysis using the GPT model, implementing a trading strategy based on the sentiment scores, and executing trades via the Alpaca Markets API.

The project is structured in the following way:

```
/GPT-SentimentTrader
    /my_openai
        - __init__.py
        - sentiment_analysis.py
    /my_alpaca
        - __init__.py
        - trading.py
    /my_twilio
        - __init__.py
        - messaging.py
    /data
        - __init__.py
        - nlp_processing.py
        - fetch_articles.py
        - process_articles.py
    /models
        - __init__.py
        - trading_strategy.py
        - finance_utils.py
        - account_utils.py
    /database
        - __init__.py
        - db_manager.py
    /tests_package
        - __init__.py
        /data
            - __init__.py
            - test_fetch_articles.py
            - test_process_articles.py
        /database
            - __init__.py
            - test_db_manager.py
        /models
            - __init__.py
            - test_trading_strategy.py
            - test_finance_utils.py
            - test_account_utils.py
        /my_alpaca
            - __init__.py
            - test_trading.py
        /my_openai
            - __init__.py
            - test_sentiment_analysis.py
        /my_twilio
            - __init__.py
            - test_messaging.py
    - main.py
    - requirements.txt 
    - Dockerfile
    - LICENSE
```

## GitHub Workflow

The project employs a continuous integration (CI) workflow using GitHub Actions for deployment to Amazon Elastic Container Service (ECS). 

The workflow performs the following steps:

1. Checkout the code from the repository
2. Configure AWS credentials
3. Cache Python dependencies to speed up workflow runs
4. Log in to Amazon Elastic Container Registry (ECR)
5. Setup Python environment
6. Install Python dependencies from `requirements.txt`
7. Build a Docker image and push it to ECR
8. Deploy the Docker image to an EC2 instance

The workflow is triggered on every push to the `main` branch. 

To make use of this workflow, AWS access credentials, secrets for accessing the EC2 instance, ECR repository, and Alpaca API keys need to be stored in the GitHub repository's secrets.
    
## Modules
Each directory contains modules that fulfill specific functions within the bot:

| Directory | Description |
|-----------|-------------|
| [my_openai](/my_openai)               | This directory contains the `sentiment_analysis.py` module, which interacts with OpenAI's GPT-3.5 API to analyze the sentiment of news articles. |
| [my_alpaca](/my_alpaca)               | The `trading.py` module in this directory manages all interactions with the Alpaca API. It is responsible for executing trading decisions made by the bot. |
| [my_twilio](/my_twilio)               | The `messaging.py` module in this directory interacts with the twilio API, providing trade notifications via SMS. |
| [data](/data)                         | This directory houses two modules. `fetch_articles.py` fetches articles from the internet, and `process_articles.py` preprocesses these articles to prepare them for sentiment analysis. |
| [database](/database)                 | This directory houses the SQLite3 database manager, `db_manager.py` which acts as a wrapper for the articles.db file found in the root directory. Its purpose is to store data before trades are executed  |
| [models](/models)                     | This directory includes the `trading_strategy.py`, `finance_utils.py`, and the `account_utils.py` modules which house the bot's trading strategy, and provide utility getter functions for other areas of the applicaion. |
| [main.py](/main.py)                   | The main script that ties all the modules together to enable the bot's functionality. |
| [requirements.txt](/requirements.txt) | The file containing the list of dependencies and libraries required for the project. |
| [Dockerfile](/Dockerfile)             | The Dockerfile containing instructions to build this application to a container. |
| [License](/LICENSE)                   | Self explanitory. More details about GPT-SentimentTrader's license below. |

## Setup & Installation

To set up and run GPT-SentimentTrader, follow these steps:

1. Fork the repository to your GitHub account: Click on the 'Fork' button at the top of the repository page.
2. Clone the forked repository to your local machine: `git clone https://github.com/<your-username>/GPT-SentimentTrader.git`
3. Navigate to the project directory: `cd GPT-SentimentTrader`
4. Add the necessary secrets to your repository. The required secrets are:
    - `AWS_ACCESS_KEY_ID`: Your AWS access key ID
    - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
    - `AWS_REGION`: The AWS region where your resources are located
    - `AWS_ACCOUNT_ID`: Your AWS account ID
    - `AWS_ECR_REPOSITORY`: The name of your ECR repository
    - `HOST`: The public IP address or DNS name of your EC2 instance
    - `USERNAME`: The username to connect to your EC2 instance
    - `SSH_PRIVATE_KEY`: The private key to connect to your EC2 instance
    - `APCA_API_KEY_ID`: Your Alpaca API key ID
    - `ALPACA_SECRET_KEY`: Your Alpaca secret key
5. Make changes to the codebase as required, commit the changes and push to the main branch: `git add .` -> `git commit -m "<your-commit-message>"` -> `git push origin main`

GitHub Actions will then automatically build a Docker image of the application, push it to the specified Amazon ECR repository, and then deploy the image to your EC2 instance.

## Usage

Run the bot by executing the main script: `python main.py` The bot will scrape news articles and analyze their sentiment every 10 minutes. The bot will then take the calculated sentiment and execute trades every Monday at market open. The bot also has support for immediate orders, which are placed in succession to the sentiment analysis, if needed.

## Dependencies

GPT-SentimentTrader implements an array of Python packages:

- OpenAI's GPT for sentiment analysis
- Alpaca's API for executing trades
- Alpha Vantage's API for finance utilities. I use the '75 requests/min' tier currently
- BeautifulSoup and Requests for fetching and parsing web articles
- Selenium for scraping dynamic content, such as artilce URLs
- Twilio's API for SMS interactions.

## Contributions 

Contributions to GPT-SentimentTrader are welcome! If you'd like to contribute, please fork the repository and make changes as you'd like. 

Pull requests are warmly welcomed as well.

If you have any questions or need further clarification about the bot, feel free to open an issue to propose what you would like to change or add.

## License

The GPT-SentimentTrader application is licensed under the (GPL) [GNU License](/LICENSE).

## Goals

This project was created with the intent to learn the interaction with OpenAI's API and see just how powerful it can be. I also want to learn more about the SDLC and how to ship software. One thing I've never truly done before is properly and "professionally" document my code with README's and comments. I want to give that a shot this time around. Before I started this project, I realized it has been way too long for me to keep waiting to mess around with GPT models. This project throws me into the crossroads of 2 of my biggest interests, computer science and finance. Now, it's time to figure out how to implement math. 

This project was NOT created with the expectation of being profitable. If you fork this repository and run this application on your own, please carry the same expectation. I am only responsible for financial gain. I am not responsible for financial loss.

🤘

