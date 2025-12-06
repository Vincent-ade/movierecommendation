# database.py
import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genres TEXT,
            tmdb_id INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            rating REAL,
            timestamp INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def import_movies():
    """Import movies from CSV to database"""
    conn = sqlite3.connect('movies.db')
    movies = pd.read_csv('movies.csv')
    movies.to_sql('movies', conn, if_exists='replace', index=False)
    conn.close()

# Initialize database
create_database()
import_movies()