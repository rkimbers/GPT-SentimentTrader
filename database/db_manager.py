import os
import sqlite3
import logging


# Check if the code is running inside a Docker container
in_docker = os.environ.get('IN_DOCKER_CONTAINER')

if in_docker == "True":
    DB_NAME = '/app/articles/articles.db'
else:
    DB_NAME = 'articles.db'

def connect_db():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        raise


def create_table():
    conn = connect_db()
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                source TEXT,
                symbol TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_scores (
                id INTEGER PRIMARY KEY,
                article_id INTEGER,
                sentiment_score REAL,
                FOREIGN KEY(article_id) REFERENCES articles(id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")
        raise
    finally:
        conn.close()


def check_url_in_database(url):
    conn = connect_db()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE url=?", (url,))
        result = c.fetchone()
        return result is not None
    except sqlite3.Error as e:
        logging.error(f"Error querying database: {e}")
        raise
    finally:
        conn.close()


def save_url_to_database(url, source, symbol, sentiment_scores):
    if check_url_in_database(url):
        logging.info(f"URL {url} already exists in the database. Skipping...")
        return
    conn = connect_db()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO articles (url, source, symbol) VALUES (?, ?, ?)",
                  (url, source, symbol))
        article_id = c.lastrowid  # Get the id of the article we just inserted
        for score in sentiment_scores:
            c.execute("INSERT INTO sentiment_scores (article_id, sentiment_score) VALUES (?, ?)",
                      (article_id, score))
        conn.commit()
    except sqlite3.IntegrityError:
        logging.info(f"Duplicated URL {url}. Skipping...")
    except sqlite3.Error as e:
        logging.error(f"Error saving URL to database: {e}")
        raise
    finally:
        conn.close()


def fetch_sentiment_scores_from_database():
    conn = connect_db()
    sentiment_scores = {}
    try:
        c = conn.cursor()
        c.execute("""SELECT articles.symbol, sentiment_scores.sentiment_score 
                     FROM articles JOIN sentiment_scores 
                     ON articles.id = sentiment_scores.article_id;""")
        records = c.fetchall()
        for record in records:
            company = record[0]
            score = record[1]
            if company in sentiment_scores:
                sentiment_scores[company].append(score)
            else:
                sentiment_scores[company] = [score]
    except sqlite3.Error as e:
        logging.error(f"Error fetching sentiment scores from database: {e}")
        raise
    finally:
        conn.close()
    return sentiment_scores


def delete_all_records():
    conn = connect_db()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM articles;")
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error deleting all records from database: {e}")
        raise
    finally:
        logging.info("Deleted all contents from table articles")
        conn.close()

def get_all_records():
    conn = connect_db()
    records = []
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM articles;")
        records = c.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Error getting all records from database: {e}")
        raise
    finally:
        conn.close()
    return records


def get_all_scores():
    conn = connect_db()
    scores = []
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM sentiment_scores;")
        scores = c.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Error getting all records from database: {e}")
        raise
    finally:
        conn.close()
    return scores