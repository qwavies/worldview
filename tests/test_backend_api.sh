#!/bin/bash

# query http://127.0.0.1:8000/sentiment
curl -X POST "https://worldview-production.up.railway.app/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"countryA": "US", "countryB": "GB"}'
