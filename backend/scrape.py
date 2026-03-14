from src.reddit_scraper.reddit_scraper import reddit_scraper
from src.reddit_scraper.reddit_to_db import save_to_reddit_db

save_to_reddit_db(*reddit_scraper("Australia", "USA"))
