# models

This directory hosts the algorithmic trading models used for determining the execution of trades. The models ingest sentiment data derived from financial news articles and determine the most optimal trading decisions based on the given sentiment.

## Files

### __init__.py
This file is necessary to make Python treat the `models` directory as a package (i.e., a directory that can contain other modules).

### trading_strategy.py
This module contains the function `decide_trades()`, which decides whether to buy or hold a stock based on sentiment analysis.

#### `decide_trades()`
This function determines the trading strategy based on the sentiment scores. The sentiment scores should be a dictionary where the keys are stock symbols and the values are the sentiment scores. A score of 1 implies a buy decision while any other score results in a hold decision.

---

Note: These models can be updated or replaced depending on the trading strategies that you want to implement. Always ensure that the input to the models (in this case, the sentiment scores) is correctly formatted and valid.
