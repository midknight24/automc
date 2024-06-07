from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
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

class PatchPrompt(BaseModel):
    name: str
    patch_prompt: str

class TypeSpecs(BaseModel):
    specs: List[PatchPrompt]


class Prompt(BaseModel):
    version: str
    intro: str
    intro2: str
    mainPrompt: str
    encore: str
    pick_and_improve: str
    type_spces: TypeSpecs


class TextType(str, Enum):
    definition = "definition and introduction"
    procedure = "mechanism and procedure"
    detail = "technical detail"
    algorithm = "algorithm and datastructure"
    comparison = "technical comparison"
    others = "others"


class Evaluation(BaseModel):
    validity: int
    explaination: str
    text_type: TextType

class EvaluationFailed(BaseModel):
    message: str
    explaination: str