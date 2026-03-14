import sqlite3
from datetime import datetime

def save_to_db(countryA, countryB, avg_score):
    conn = sqlite3.connect('worldview_reddit.db')
    cursor = conn.cursor() 

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_a TEXT,
            country_b TEXT,
            score REAL,
            date_created DATETIME
        )
    ''')

    cursor.execute('''
        INSERT INTO sentiment_results (country_a, country_b, score, date_created)
        VALUES (?, ?, ?, ?)
    ''', (countryA, countryB, avg_score, datetime.now()))

    conn.commit()
    conn.close()
