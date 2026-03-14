from pydantic import BaseModel

class CountryABQuery(BaseModel):
    countryA: str
    countryB: str
