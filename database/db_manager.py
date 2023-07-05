import os
import sqlite3

# Check if the code is running inside a Docker container
in_docker = os.environ.get('IN_DOCKER_CONTAINER')

if in_docker == "True":
    DB_NAME = '/app/articles/articles.db'
else:
    DB_NAME = 'articles.db'

def connect_db():
    # Check if the code is running inside a Docker container
    in_docker = os.environ.get('IN_DOCKER_CONTAINER')

    if in_docker == "True":
        #DB_NAME = '/app/articles/articles.db'
        print("You are containerized!")
    else:
        #print("Local machine")
        DB_NAME = 'articles.db'
    
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = connect_db()
    if conn is None:
        return
    try:
        c = conn.cursor()
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
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def check_url_in_database(url):
    conn = connect_db()
    if conn is None:
        return False
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE url=?", (url,))
        result = c.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Error querying database: {e}")
        return False
    finally:
        conn.close()

def save_url_to_database(url, source, symbol, sentiment_score):
    if check_url_in_database(url):
        print(f"URL {url} already exists in the database. Skipping...")
        return
    conn = connect_db()
    if conn is None:
        return
    try:
        c = conn.cursor()
        c.execute("INSERT INTO articles (url, source, symbol, sentiment_score) VALUES (?, ?, ?, ?)",
                  (url, source, symbol, sentiment_score))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicated URL {url}. Skipping...")
    except sqlite3.Error as e:
        print(f"Error saving URL to database: {e}")
    finally:
        conn.close()

def fetch_sentiment_scores_from_database():
    conn = connect_db()
    if conn is None:
        return {}
    sentiment_scores = {}
    try:
        c = conn.cursor()
        c.execute("SELECT symbol, sentiment_score FROM articles;")
        records = c.fetchall()
        for record in records:
            company = record[0]
            score = record[1]
            if company in sentiment_scores:
                sentiment_scores[company].append(score)
            else:
                sentiment_scores[company] = [score]
    except sqlite3.Error as e:
        print(f"Error fetching sentiment scores from database: {e}")
    finally:
        conn.close()
    return sentiment_scores

def delete_all_records():
    conn = connect_db()
    if conn is None:
        return
    try:
        c = conn.cursor()
        c.execute("DELETE FROM articles;")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting all records from database: {e}")
    finally:
        print("Deleted all contents from table articles")
        conn.close()

def get_all_records():
    conn = connect_db()
    if conn is None:
        return []
    records = []
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM articles;")
        records = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error getting all records from database: {e}")
    finally:
        conn.close()
    return records
