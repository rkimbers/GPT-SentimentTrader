# models

This directory hosts the algorithmic trading models used for determining the execution of trades. The models ingest sentiment data derived from financial news articles and determine the most optimal trading decisions based on the given sentiment.

## Files

### __init__.py

This file is necessary to make Python treat the `models` directory as a package (i.e., a directory that can contain other modules). Currently not in use.

### trading_strategy.py
This module contains the support for preparing buy, sell, and immediate orders. It relies heavily on the `finance_utils.py` and `account_utils.py` modules and their underlying functions

#### `prepare_buy_orders()`
This function accepts the sentiment score list of dictionaries as an input. It will translate the company names to ticker symbols using the `translate_symbols()` function. It asseses a order cap based on 10% of the portfolio value - more specifically the non-marginable buying power. It gathers the portfolio value by calling the `account_value()` function. It also determines the amount of shares to buy given the individual ticker's sentiment score's portion of the total sentiment. It then uses that same percentage to figure out the shares to purchase. This is done by multiplying the percentage by the order cap, then dividing that number by the share price (calling `get_share_price()`).

#### `prepare_sell_orders()`
This function contains most of the same logic as `prepare_buy_orders()`. The difference is that it calculates the quantity in a unique way. It determines how much of a position to sell by dividing the sentiment score by 10, and taking the absolute value. A sentiment score of -2 becomes 0.2 (20%), and -9 becomes 0.9 (90%). It takes that percentage as the percentage of the current position to sell, rounded to the nearest whole number

#### `prepare_immediate_order()` 
`prepare_immedate_order()` is designated to execute whenever a sentiment score of 10 is gathered from a single article. It is allocated 1% of the non-marginable buying power. It acts in the same way as `prepare_buy_orders()` for the most part. Currently, this function does not have support for sell orders. I am still contimplating if that is a good idea.

### finance_utils.py
This module contains getter functions that interact with Alpha Vantage's API, and functions that act as "supporters" for the bulky logic in my `trading_strategy.py` module. 

#### `compile_and_average_scores()`
This function takes a list of scores which have been represented as the value in the sentiment_scores list of dictionaries. It returns all indicies of the list of scores, averaged.

#### `translate_symbols()`
This function takes a list of company names, and translates them one by one by calling `get_symbol()` for each index. It returns a list of companies.

#### `get_symbol()`
This function utilizes the Alpha Vantage API and builds an API endpoint by appending the company to a base url. It searches by company name, expecting a JSON response of a bunch of ticker symbols. It then returns the first response that is within the United States, as many times the first exchange returned would be on a foreign exchange.

#### `get_share_price()`
This function also utilizes the Alpha Vantage API and builds an endpoint in the same way as `get_symbol()`. It searches by ticker symbol and expects a JSON response containing a bunch of price data. It extracts the most relevant data, the key "Time Series (5min)". It returns that value as a float

#### `prepare_trades()`
This function is a bit redundant. It is still in use, but will be removed soon. It translates the symbol and the share price, which is already done in `prepare_buy_orders()`

#### `calculate_total_sentiment()`
This function is also redundant, and soon to be removed. It adds up the total sentiment from the values in the sentiment_scores dictionary. 


### account_utils.py
This module contains the interactions with the user's Alpaca Markets account.

#### `account_value()`
This function makes a call to Alpha Vantage's API and returns the user's non-marginable buying power.

#### `portfolio_positions()`
`portfolio_positions()` is a very self-explanitory function. It makes a call to the `get_all_positions()` Alpaca API endpoint. Returns a list of positions


## Usage
Import the necessary functions from each file as needed. For example, to use the `prepare_buy_orders()` function in your code, you would use:

```python
from models.trading_strategy.py import prepare_buy_orders