#!/bin/bash

cd "$(dirname "$0")"

# activate python venv
source .venv/bin/activate

# run
python download_and_search.py

