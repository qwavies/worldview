import asyncio
from src.reddit_scraper.reddit_scraper import reddit_scraper
from src.reddit_scraper.reddit_to_db import save_to_reddit_db
from src.twitter_scraper.twitter_scraper import main

"""
TODO:
    -[ ] create databases folder if it doesnt exist
    -[x] reddit 
    -[x] twitter
    -[ ] news
""" 



# save_to_reddit_db(*reddit_scraper("Australia", "USA"))
# print("finished reddit scrape")

asyncio.run(main("Australia", "USA")) # should already populate db
print("finished twitter scrape")
