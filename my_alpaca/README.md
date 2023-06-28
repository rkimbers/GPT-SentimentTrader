# my_alpaca

This directory contains modules that interact with the Alpaca trading platform. These modules allow the application to execute trades based on sentiment analysis performed on financial news articles.

## Files 

### __init__.py
This file is necessary to make Python treat the `my_alpaca` directory as a package (i.e., a directory that can contain other modules).

### trading.py
This module contains the `submit_order()` function, which handles trade execution. 

#### `submit_order()`
This function is responsible for submitting trade orders to the Alpaca trading platform. It takes a `trade` object as its argument, is a dictionary containing a stock symbol, order side, and quantiy. This function uses the Alpaca API key and "secret" key to authenticate with the Alpaca trading platform. Once authenticated, the function constructs a `MarketOrderRequest` object with the necessary details for the trade, and submits the order using the `TradingClient.submit_order()` method. After the trade is executed, the function *previously* prints the details of the executed order. The function also returns the `market_order` object.

## Usage
Import the necessary functions from each file as needed. For example, to use the `submit_order()` function in your code, you would use:

```python
from my_alpaca.trading import submit_order


