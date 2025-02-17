from sqlmodel import SQLModel, Field, TEXT, create_engine, Session, Enum
from sqlalchemy import Column, event
from sqlalchemy.event import listen
from datetime import datetime
from typing import Optional
from enum import Enum as oEnum


class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)


class Prompt(Base, table=True):
    template: str = Field(sa_column=Column(TEXT))

class ModelVendor(oEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"

class LLMBackend(Base, table=True):
    name: str = Field()
    description: str = Field()
    url: str = Field()
    secret: str = Field()
    model_vendor: ModelVendor = Field(sa_column=Column(Enum(ModelVendor)))

def update_time(mapper, connection, target):
    target.updated = datetime.now()

listen(Prompt, 'before_update', update_time)
listen(LLMBackend, 'before_update', update_time)

def get_db():
    from .config import DATABASE
    engine = create_engine(DATABASE)
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()