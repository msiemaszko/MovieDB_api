#!/usr/bin/env bash
set -ex

poetry run python ./scripts/wait_redis_postgres.py
poetry run python -m src.utilities.populate_database
poetry run python -m data_loader.get_posters
poetry run uvicorn src.main.app:app --reload --host 0.0.0.0 --port 5000
