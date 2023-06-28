# models

This directory acts as the wrapper for the articles.db file located in the root directory. It contains various methods to read and write from the SQLite3 database that stores the article URL, source, symbol, and score. In our case, symbol refers to the company. The company is translated into a ticker symbol in other functionality within the application.

## Files

### db_manager.py

This module contains various functions that aid the interation with the database.

#### `connect_db()`
Instantiates/authenticates database. 

#### `create_table()`
Creates a table within the database named articles. The table has the following attributes: id INTEGER PRIMARY KEY, url TEXT UNIQUE, source TEXT, symbol TEXT, sentiment_score REAL. 

#### `check_url_in_database()`
Checks if URL already exists in the database. This function is very important in elimitating potential duplicates which can skew true sentiment scores.

#### `save_url_in_database()`
Calls the `check_url_in_database()` function and proceeds to add an index in the table articles with the following parameters: url, source, symbol, sentiment_score (if the url isn't already existent in the database).

#### `get_all_tables()`
Returns all tables in the database. Not the table's content. Returns a tuple.

#### `get_all_tables_strings()`
Returns all tables in the database. Not the table's content. Returns a string.

#### `create_table_if_not_exists()`
Identical to the `create_table()` function.

#### `get_all_records()`
Returns all records from the articles table. 

#### `fetch_sentiment_scores_from_database()`
Grabs every company and sentiment score from the database. If the same company has multiple scores, it adds the multiple scores to a list. This function returns a list of dictionaries, where the key is the company name and the value is a list of sentiment scores.

## Usage
Import the necessary functions from each file as needed. For example, to use the `fetch_sentiment_scores_from_database()` function in your code, you would use:

```python
from database.db_manager import fetch_sentiment_scores_from_database

