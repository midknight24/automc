from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetaBase(BaseModel):
    id: int
    created: datetime
    updated: datetime

class Prompt(MetaBase):
    id: int = None
    template: str

class PromptUpsert(BaseModel):
    id: Optional[int] = None
    template: str

class LLMBackend(MetaBase):
    name: str
    description: str
    url: str
    secret: str

    class Config:
        from_attributes = True

class LLMBackendUpsert(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    url: str
    secret: str


    class Config:
        from_attributes = True

