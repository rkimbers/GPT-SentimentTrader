# file: models/trading_strategy.py

def decide_trades(sentiment_scores):
    """
    Decide on the trades to make based on sentiment scores.

    This function currently uses a very simple strategy: it buys one share of a stock if its sentiment score is positive,
    and sells one share if its sentiment score is negative.

    In a real-world application, you'd likely want to use a more sophisticated strategy.

    :param sentiment_scores: A dictionary where the keys are stock symbols and the values are sentiment scores.
    :return: A list of trades to execute. Each trade is represented as a dictionary with keys "symbol", "qty" and "side".
    """

    trades = []
    for symbol, score in sentiment_scores.items():
        if score > 0:
            trades.append({"symbol": symbol, "qty": 1, "side": "buy"})
        elif score < 0:
            trades.append({"symbol": symbol, "qty": 1, "side": "sell"})

    return trades
