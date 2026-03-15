import sqlite3
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(content: str) -> float:
    if not content:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(content)['compound']

def news_to_db(country_a: str, country_b: str, news_text: list[str]):
    conn = sqlite3.connect('databases/news_database.db')
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
        news_sentiment = analyse(news)
        cursor.execute('''
        INSERT INTO NEWS(source_country, target_country, news, sentiment_score, date_created
                    ) VALUES (?, ?, ?, ?, ?)''', (country_a, country_b, news, news_sentiment, datetime.now()))

    conn.commit()
    conn.close()
