from functools import wraps
from fastapi import FastAPI, Depends
from .db import get_session, Session
from . import crud
from . import model


app = FastAPI()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def exception_wrapper(fn):
    # necessary!
    @wraps(fn)
    def f(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(e)
            return str(e)
    return f