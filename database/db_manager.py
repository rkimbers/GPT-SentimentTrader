import os
import sqlite3
import logging
import json

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
                scores TEXT
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


def save_url_to_database(url, source, scores):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Convert the scores dictionary to a JSON string
        scores_json = json.dumps(scores)

        cursor.execute(
            f"INSERT INTO articles (url, source, scores) VALUES (?, ?, ?)",
            (url, source, scores_json),
        )


def fetch_all_from_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")

        # Fetch all rows from the query
        rows = cursor.fetchall()

        # Create a list of tuples, converting the JSON string back to a Python dictionary
        result = [
            (row[0], row[1], row[2], json.loads(row[3]))
            for row in rows
        ]

    return result


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
        c.execute("SELECT scores FROM articles;")
        rows = c.fetchall()
        scores = [json.loads(row[0]) for row in rows]
    except sqlite3.Error as e:
        logging.error(f"Error getting all records from database: {e}")
        raise
    finally:
        conn.close()
    return scores
