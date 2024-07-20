#!/bin/bash

# Start Redis server
redis-server &

# Start Celery worker
celery -A celery_app worker --loglevel=info &

# Run the main application
python main.py