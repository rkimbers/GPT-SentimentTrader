import sqlite3

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
