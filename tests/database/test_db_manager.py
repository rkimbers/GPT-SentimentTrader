import pytest
import sqlite3
import json
from unittest.mock import patch
from database.db_manager import *

def test_create_table():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = None
        create_table()
        assert mock_connect.called

def test_save_url_to_database():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = None
        save_url_to_database('https://example.com', 'test_source', {'score': 0.8})
        assert mock_connect.called

def test_check_url_in_database_true():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = ('1', 'https://example.com', 'test_source', json.dumps({'score': 0.8}))
        assert check_url_in_database('https://example.com') == True

def test_check_url_in_database_false():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = None
        assert check_url_in_database('https://example.com') == False

def test_get_all_records():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchall.return_value = [('1', 'https://example.com', 'test_source', json.dumps({'score': 0.8}))]
        assert get_all_records() == [('1', 'https://example.com', 'test_source', {'score': 0.8})]

def test_get_all_scores():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchall.return_value = [(json.dumps({'score': 0.8}),)]
        assert get_all_scores() == [{'score': 0.8}]

def test_fetch_all_from_database():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchall.return_value = [('1', 'https://example.com', 'test_source', json.dumps({'score': 0.8}))]
        assert fetch_all_from_database() == [('1', 'https://example.com', 'test_source', {'score': 0.8})]

def test_delete_all_records():
    with patch('database.db_manager.sqlite3.connect') as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.fetchall.return_value = None
        delete_all_records()
        assert mock_connect.called
