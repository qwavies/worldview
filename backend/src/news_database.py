import sqlite3
from datetime import date

def news_to_db(country_a, country_b, news_text, sentiment_score, date_created):
    conn = sqlite3.connect('news_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXIST NEWS(
                   id PRIMARY KEY AUTOINCREMENT NOT NULL,
                   source_country TEXT NOT NULL,
                   target_country TEXT NOT NULL,
                   news_text TEXT NOT NULL,
                   sentiment_score REAL NOT NULL,
                   date_created DATE NOT NULL
                   )
    ''')

    cursor.execute('''
    INSERT INTO NEWS(source_country, target_country, news_text, sentiment_score, date_created
                   ) VALUES (?, ?, ?, ?, ?)''', (country_a, country_b, news_text, sentiment_score, date_created))

    conn.commit()
    conn.close()