from newsapi import NewsApiClient
from newspaper import Article
import pycountry
from dotenv import load_dotenv
import os

def news_scrapper(countryA, countryB):
    def get_country_code(name):
        try:
            results = pycountry.countries.search_fuzzy(name)
            return results[0].alpha_2.lower() 
        except Exception:
            return None
    load_dotenv()
    API = os.getenv('news_api')
    newsapi = NewsApiClient(api_key=API)
    
    countryA = "USA"
    countryAcode = get_country_code(countryA)
    countryB = "CHINA"
    articles = newsapi.get_top_headlines(
        q=countryB,       # Country B
        country=countryAcode,    # Country A
        language='en'
    )
    data = []
    for article in articles['articles']:
        url = article['url']
        title = article['title']
        
        try:
            #Get the full text content
            scraper = Article(url)
            scraper.download()
            scraper.parse()
            full_text = scraper.text
            data.append(full_text)
        
        except Exception as e:
            print(f"Skipping {title[:30]}... (Error: {e})")
        
    return data
            
