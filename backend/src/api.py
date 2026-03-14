from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str|None = None
    is_done: bool = False

@app.get("/testapi")
def test_api():
    return {"hello": "world"}

