# my_alpaca

This directory contains modules that interact with the Alpaca trading platform. These modules allow the application to execute trades based on sentiment analysis performed on financial news articles.

## Files 

### __init__.py
This file is necessary to make Python treat the `my_alpaca` directory as a package (i.e., a directory that can contain other modules).

### trading.py
This module contains the `submit_order()` function, which handles trade execution. 

#### `submit_order()`
This function is responsible for submitting trade orders to the Alpaca trading platform. It takes a `trade` object as its argument, which should be a dictionary containing a stock symbol and a sentiment score. The sentiment score is used to determine the type of trade to execute: a score of 1 results in a "buy" order, while any other score results in a "hold" decision. 

This function uses the Alpaca API key and secret key to authenticate with the Alpaca trading platform. These keys should be stored as environment variables. 

Once authenticated, the function constructs a `MarketOrderRequest` object with the necessary details for the trade, and submits the order using the `TradingClient.submit_order()` method. 

After the trade is executed, the function prints the details of the executed order and returns the `market_order` object.

---

Remember to update your Alpaca API key and secret key in the `trading.py` file with your own values. You can obtain these keys by creating an account on the Alpaca platform. Always store these keys in a secure manner, and never publish them in a public repository.
