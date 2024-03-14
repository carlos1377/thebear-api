#!/bin/sh

set -e

alembic upgrade head

echo "Migrations complete, starting server ✅"
