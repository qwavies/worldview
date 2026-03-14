import asyncio
import os
from src.reddit_scraper.reddit_scraper import reddit_scraper
from src.reddit_scraper.reddit_to_db import save_to_reddit_db
from src.twitter_scraper.twitter_scraper import main
from src.news_scraper.news_scrapper import news_scrapper
from src.news_scraper.news_database import news_to_db

"""
TODO:
    -[ ] create databases folder if it doesnt exist
    -[x] reddit 
    -[x] twitter
    -[x] news
""" 

# create databases dir if it doesnt already exist
os.makedirs('databases', exist_ok=True)

save_to_reddit_db(*reddit_scraper("Australia", "USA"))
print("finished reddit scrape")

asyncio.run(main("Australia", "USA")) # should already populate db
print("finished twitter scrape")

news_to_db(*news_scrapper("Australia", "China"))
print("FINISHED EVERY DATABASE YAYYYYY")
