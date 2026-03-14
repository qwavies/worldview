from fastapi import FastAPI, HTTPException
from src.pydantic_models import CountryABQuery

app = FastAPI()

@app.get("/testapi")
def test_api():
    return {"hello": "world"}

@app.get("/sentiment")
def get_countryab_sentiment(countryAB: CountryABQuery):
    return {"a_to_b":0.2, "b_to_a":0.5}
