from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .model import ModelVendor

class MetaBase(BaseModel):
    id: int
    created: datetime
    updated: datetime

class Prompt(MetaBase):
    template: str

class PromptUpsert(BaseModel):
    id: Optional[int] = None
    template: str

class LLMBackend(MetaBase):
    name: str
    description: str
    url: str
    secret: str
    model_vendor: ModelVendor

    class Config:
        from_attributes = True

class LLMBackendUpsert(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    url: str
    secret: str
    model_vendor: ModelVendor


    class Config:
        from_attributes = True

class GenRequest(BaseModel):
    llm_id: int
    prompt_id: int
    content: str
    model: Optional[str] = ""


class Prompt(BaseModel):
    version: str
    intro: str
    intro2: str
    mainPrompt: str
    encore: str
    pick: str
    improve: str

class Evaluation(BaseModel):
    validity: int
    explaination: str

class EvaluationFailed(BaseModel):
    message: str
    explaination: str