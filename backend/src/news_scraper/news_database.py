import sqlite3
from datetime import datetime

def news_to_db(country_a, country_b, news_text, sentiment_score):
    conn = sqlite3.connect('news_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NEWS(
                   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   source_country TEXT NOT NULL,
                   target_country TEXT NOT NULL,
                   news TEXT NOT NULL,
                   sentiment_score REAL NOT NULL,
                   date_created DATE NOT NULL
                   )
    ''')

    for news in news_text:
        cursor.execute('''
        INSERT INTO NEWS(source_country, target_country, news, sentiment_score, date_created
                    ) VALUES (?, ?, ?, ?, ?)''', (country_a, country_b, news, sentiment_score, datetime.now()))

    conn.commit()
    conn.close()
