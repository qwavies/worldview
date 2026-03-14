from fastapi import FastAPI, HTTPException
from src.pydantic_models import CountryABQuery
from src.RedditScrapper import RedditScrapper

app = FastAPI()

@app.get("/testapi")
def test_api():
    return {"hello": "world"}

@app.get("/sentiment")
def get_countryab_sentiment(countryAB: CountryABQuery):
    a_to_b = RedditScrapper(countryAB.countryA, countryAB.countryB)
    b_to_a = RedditScrapper(countryAB.countryB, countryAB.countryA)
    return {"a_to_b":a_to_b, "b_to_a":b_to_a}
