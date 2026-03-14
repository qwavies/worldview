import sqlite3

DB_NAME = 'worldview_tweet.db'

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_country TEXT,
            target_country TEXT,
            username TEXT,
            tweet_text TEXT,
            created_at TEXT,
            retweets INTEGER,
            likes INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("Database setup complete.")

def insert_tweets_batch(tweet_batch_data):
    """Inserts a list of multiple tweets into the database in one fast transaction."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.executemany('''
        INSERT INTO tweets (source_country, target_country, username, tweet_text, created_at, retweets, likes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tweet_batch_data)
    
    conn.commit()
    conn.close()