#!/bin/sh

alembic upgrade heads

echo "Migrations complete, starting server ✅"

echo "Starting server 🚀"
uvicorn main:app --host 0.0.0.0 --reload
