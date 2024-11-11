#! /usr/bin/env sh

# Let the DB start
# python3 -m app.database.create_database

# Start the backend server

echo 'Starting DKC-BRO Processor'
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

