#!/bin/sh
sleep 10
alembic upgrade heads

echo "Migrations complete, starting server ✅"

echo "Starting server 🚀 \n"
uvicorn main:app --host 0.0.0.0 --reload
