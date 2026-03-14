#!/bin/bash

cd ./backend/
uv sync

# start venv
source .venv/bin/activate

# start backend server
uv run uvicorn src.api:app --reload


