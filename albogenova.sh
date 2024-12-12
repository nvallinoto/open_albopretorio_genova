#!/bin/bash

ARCHIVE_DAYS=14

cd "$(dirname "$0")"

# activate python venv
source .venv/bin/activate

# run
python download_and_search.py

# end
deactivate

# archive
find pub -maxdepth 1 -name "*.html" -type f -mtime +$ARCHIVE_DAYS -print0 | xargs -0 -I {} mv {} pub/archive/
