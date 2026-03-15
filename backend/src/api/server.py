from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/testapi")
def test_api():
    return {"hello": "world"}


@app.get("/sentiment")
def get_sentiment(countryA: str, countryB: str):
    # TODO: replace with real DB queries
    def rand():
        return round(random.uniform(-1, 1), 3)

    return {
        "news": {"a": rand(), "b": rand()},
        "reddit": {"a": rand(), "b": rand()},
        "twitter": {"a": rand(), "b": rand()},
    }


# from fastapi import FastAPI, HTTPException
# from src.api.pydantic_models import CountryABQuery
#
# app = FastAPI()
#
# @app.get("/testapi")
# def test_api():
#     return {"hello": "world"}
#
# @app.get("/sentiment")
# def get_countryab_sentiment(countryAB: CountryABQuery):
#     # TODO: query from DBs and return
#     return {"hello": "world"}
