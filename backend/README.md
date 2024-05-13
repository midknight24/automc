# automc backend

fastapi backend

run command: python -m app.main

# db migration guide
```
# generate migration
alembic revision --autogenerate -m "revision message here"

# make migration
alembic upgrade head

# undo migration
alembic downgrade base
```