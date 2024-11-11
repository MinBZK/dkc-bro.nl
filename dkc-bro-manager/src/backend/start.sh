#! /usr/bin/env bash

# Let the DB start
python3 -m app.create_database

# Run migrations
alembic -c alembic/alembic.ini upgrade head

# Start the backend server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000