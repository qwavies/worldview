import sqlite3
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(content: str) -> float:
    if not content:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(content)['compound']

def save_to_reddit_db(countryA: str, countryB: str, data: list[str]):
    conn = sqlite3.connect('databases/worldview_reddit.db')
    cursor = conn.cursor() 

    # create database if it doesnt exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_a TEXT,
            country_b TEXT,
            score REAL,
            date_created DATETIME
        )
    ''')

    # iterate through all posts, get sentiment analysis and put in database
    for post in data:
        sentiment_score = analyse(post)

        cursor.execute('''
            INSERT INTO sentiment_results (country_a, country_b, score, date_created)
            VALUES (?, ?, ?, ?)
        ''', (countryA, countryB, sentiment_score, datetime.now()))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    from src.reddit_scraper.reddit_scraper import reddit_scraper

    save_to_reddit_db(*reddit_scraper("Australia", "USA"))
