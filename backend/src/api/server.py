from fastapi import FastAPI, HTTPException
from src.api.pydantic_models import CountryABQuery

app = FastAPI()

@app.get("/testapi")
def test_api():
    return {"hello": "world"}

@app.get("/sentiment")
def get_countryab_sentiment(countryAB: CountryABQuery):
    # TODO: query from DBs and return
    return {"hello": "world"}
