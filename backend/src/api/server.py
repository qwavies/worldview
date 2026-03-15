from fastapi import FastAPI, HTTPException
import random
from src.api.pydantic_models import CountryABQuery
from fastapi.middleware.cors import CORSMiddleware

from src.reddit_scraper.reddit_scraper import reddit_scraper
from src.news_scraper.news_scrapper import news_scrapper

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(content: str) -> float:
    if not content:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(content)['compound']

def analyse_list(content: list[str]) -> list[float]:
    return [analyse(s) for s in content]

def filter_zeros(numbers: list[float]) -> list[float]:
    return [n for n in numbers if n != 0]

def average_sentiment(content: list[float]) -> float:
    return sum(content) / len(content) if content else 0.0

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    )

@app.get("/testapi")
def test_api():
    return {"hello": "world"}

@app.post("/sentiment")
def get_countryab_sentiment(countryAB: CountryABQuery):
    countryA: str = countryAB.countryA
    countryB: str = countryAB.countryB

    try:
        _, _, a_to_b_reddit = reddit_scraper(countryA, countryB)
        _, _, b_to_a_reddit = reddit_scraper(countryB, countryA)
        a_to_b_reddit_sentiments: list[float] = filter_zeros(analyse_list(a_to_b_reddit))
        b_to_a_reddit_sentiments: list[float] = filter_zeros(analyse_list(b_to_a_reddit))
        a_to_b_reddit_sentiment: float = average_sentiment(a_to_b_reddit_sentiments)
        b_to_a_reddit_sentiment: float = average_sentiment(b_to_a_reddit_sentiments)
    except:
        a_to_b_reddit_sentiment: float = 0
        b_to_a_reddit_sentiment: float = 0

    try:
        _, _, a_to_b_news = news_scrapper(countryA, countryB)
        _, _, b_to_a_news = news_scrapper(countryB, countryA)
        a_to_b_news_sentiments: list[float] = filter_zeros(analyse_list(a_to_b_news))
        b_to_a_news_sentiments: list[float] = filter_zeros(analyse_list(b_to_a_news))
        a_to_b_news_sentiment: float = average_sentiment(a_to_b_news_sentiments)
        b_to_a_news_sentiment: float = average_sentiment(b_to_a_news_sentiments)
    except:
        a_to_b_news_sentiment: float = 0
        b_to_a_news_sentiment: float = 0


    return {
        "news": {"a": a_to_b_news_sentiment, "b": b_to_a_news_sentiment},
        "reddit": {"a": a_to_b_reddit_sentiment, "b": b_to_a_reddit_sentiment},
    }
