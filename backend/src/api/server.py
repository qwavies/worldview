from fastapi import FastAPI, HTTPException
import random
from src.api.pydantic_models import CountryABQuery
from fastapi.middleware.cors import CORSMiddleware
import time

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
    # TODO: query from DBs and return
    def rand():
        return round(random.uniform(-1, 1), 3)

    time.sleep(10)

    return {
        "news": {"a": rand(), "b": rand()},
        "reddit": {"a": rand(), "b": rand()},
        "twitter": {"a": rand(), "b": rand()},
    }
