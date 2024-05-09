from sqlmodel import SQLModel, Field, TEXT
from sqlalchemy import Column
from datetime import datetime
from typing import Optional

class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)


class Prompt(Base, table=True):
    template: str = Field(sa_column=Column(TEXT))

class LLMBackend(Base, table=True):
    name: str = Field()
    description: str = Field()
    url: str = Field()
    secret: str = Field()