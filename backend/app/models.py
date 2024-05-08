from sqlmodel import SQLModel,  Field
from datetime import datetime
from typing import Optional

class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)


class Prompt(Base, table=True):
    pass
