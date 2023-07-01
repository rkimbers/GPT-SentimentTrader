import os
import sqlite3

# Check if the code is running inside a Docker container
in_docker = os.environ.get('IN_DOCKER_CONTAINER')

if in_docker == "True":
    DB_NAME = '/app/data/articles.db'
else:
    DB_NAME = 'articles.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            source TEXT,
            symbol TEXT,
            sentiment_score REAL
        )
    ''')

    conn.commit()
    conn.close()

def check_url_in_database(url):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT * FROM articles WHERE url=?", (url,))

    result = c.fetchone()

    conn.close()

    return result is not None

def save_url_to_database(url, source, symbol, sentiment_score):
    if check_url_in_database(url):
        print(f"URL {url} already exists in the database. Skipping...")
        return

    conn = connect_db()
    c = conn.cursor()

    c.execute("INSERT INTO articles (url, source, symbol, sentiment_score) VALUES (?, ?, ?, ?)", 
              (url, source, symbol, sentiment_score))

    conn.commit()
    conn.close()
    
    print(f"New entry succssfully added: url - {url}, source - {source}, symbol - {symbol}, sentiment_score - {sentiment_score}")

def create_table_if_not_exists():
    conn = connect_db()
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            source TEXT,
            symbol TEXT,
            sentiment_score REAL
        )
    ''')

    conn.commit()
    conn.close()
    
def get_all_tables():
    conn = connect_db()
    c = conn.cursor()

    # Execute a query to get all tables in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch all results
    tables = c.fetchall()

    conn.close()

    return tables

def get_all_tables_strings():
    conn = connect_db()
    c = conn.cursor()

    # Execute a query to get all tables in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch all results and extract table names from the tuples
    tables = [table[0] for table in c.fetchall()]

    conn.close()

    return tables

def get_all_records():
    conn = connect_db()
    c = conn.cursor()

    # Execute a query to get all records from the 'articles' table
    c.execute("SELECT * FROM articles;")

    # Fetch all results
    records = c.fetchall()

    conn.close()

    return records

def fetch_sentiment_scores_from_database():
    # Connect to the database
    conn = connect_db()
    c = conn.cursor()

    # Execute a query to get all records from the 'articles' table
    c.execute("SELECT symbol, sentiment_score FROM articles;")

    # Fetch all results
    records = c.fetchall()

    # Close the connection to the database
    conn.close()

    # Initialize an empty dictionary to store the sentiment scores
    sentiment_scores = {}

    # Go through each record
    for record in records:
        # Extract the company and sentiment score
        company = record[0]
        score = record[1]

        # If the company is already in the dictionary, add the score to its list of scores
        if company in sentiment_scores:
            sentiment_scores[company].append(score)
        # If the company is not in the dictionary, add a new entry with a list containing the score
        else:
            sentiment_scores[company] = [score]

    return sentiment_scores

def delete_all_records():
    conn = connect_db()
    c = conn.cursor()

    # Execute a query to delete all records from the 'articles' table
    c.execute("DELETE FROM articles;")

    conn.commit()
    conn.close()
