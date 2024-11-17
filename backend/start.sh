#!/bin/bash

set -e

# alembic revision --autogenerate -m "new migration"

alembic upgrade head

python -m app.main