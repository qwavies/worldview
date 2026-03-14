import asyncio
import sys
import time
from datetime import datetime
from random import randint
from configparser import ConfigParser
from geopy.geocoders import Nominatim
from twikit import Client, TooManyRequests, NotFound
from src.twitter_scraper.twitter_database import setup_database, insert_tweets_batch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(content: str) -> float:
    if not content:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(content)['compound']

MINIMUM_TWEETS = 50

def check_configuration(filepath='config.ini'):
    """
    
    Verifies that the configuration file exists.
    
    """
    config = ConfigParser()
    if not config.read(filepath):
        print(f"ERROR: Could not read {filepath}. Please ensure it exists.")
        sys.exit()

def authenticate_client(cookies_path='cookies.json'):
    """
    
    Initialises the Twikit client and loads session cookies.
    
    """
    client = Client(language='en-UK')
    print(f'{datetime.now()} - Loading cookies...')
    try:
        client.load_cookies(cookies_path)
        print("SUCCESS: Cookies loaded!")
        return client
    except Exception as e:
        print(f"ERROR: Could not load {cookies_path}. Details: {e}")
        sys.exit()

def get_country_geocode(country_name, default_radius="1000km"):
    """
    
    Fetches coordinates for a country using OpenStreetMap.
    
    """
    geolocator = Nominatim(user_agent="worldview_sentiment_scraper")
    
    print(f"Locating {country_name} on the map...")
    location = geolocator.geocode(country_name)
    time.sleep(1) 
    
    if location:
        return f"{location.latitude},{location.longitude},{default_radius}"
    else:
        print(f"Could not find coordinates for {country_name}")
        return None

async def get_tweets(client, tweets, query):
    """
    
    Fetches the next page of tweets, handling pagination and pauses.
    
    """
    if tweets is None:
        print(f'{datetime.now()} - Searching for: {query}')
        tweets = await client.search_tweet(query, product='Top')
    else:
        wait_time = randint(1, 5)
        print(f'{datetime.now()} - Pausing for {wait_time}s to mimic human browsing...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()

    return tweets


async def process_country_pair(client, source, target):
    """
    
    Handles the extraction loop for a single geographic relationship.
    
    """
    dynamic_geocode = get_country_geocode(source, default_radius="1000km")
    
    if not dynamic_geocode:
        print(f"Skipping task {source} -> {target} due to missing coordinates.")
        return

    current_query = f'{target} geocode:{dynamic_geocode} lang:en since:2026-02-01 until:2026-03-01'
    
    print(f"\n{'='*50}")
    print(f"STARTING EXTRACTION: {source} -> {target}")
    print(f"Using coordinates: {dynamic_geocode}")
    print(f"{'='*50}")
    
    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(client, tweets, current_query)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue
        except NotFound:
            print("ERROR 404: X killed the session. grab fresh cookies from your browser.")
            sys.exit() 
        except Exception as e:
            print(f"Unexpected Error during {source}->{target}: {e}")
            break

        if not tweets:
            print(f'{datetime.now()} - No more tweets found for this specific topic.')
            break

        current_batch = []
        for tweet in tweets:
            tweet_analysis = analyse(tweet.text) # sentiment analysis

            tweet_count += 1
            tweet_data = (
                source, 
                target, 
                tweet.user.name, 
                tweet.text, 
                tweet.created_at, 
                tweet.retweet_count, 
                tweet.favorite_count,
                tweet_analysis
            )
            current_batch.append(tweet_data)

        insert_tweets_batch(current_batch)

        print(f'{datetime.now()} - Collected {tweet_count}/{MINIMUM_TWEETS} tweets...')

    print(f"DONE extraction for {source} -> {target}.\n")


async def main(countryA: str, countryB: str):
    search_tasks = [
    {'source': countryA, 'target': countryB},
]

    check_configuration()
    print(f'{datetime.now()} - Setting up database...')
    setup_database()

    client = authenticate_client()

    for task in search_tasks:
        await process_country_pair(client, task['source'], task['target'])
        print("Taking an 8-second break before the next country...")
        await asyncio.sleep(8)

    print("ALL TASKS DONE")

# if __name__ == "__main__":
#     asyncio.run(main())
