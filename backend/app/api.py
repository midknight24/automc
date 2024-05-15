from fastapi import APIRouter, Depends
from sqlmodel import Session
from .model import get_db
from .schema import LLMBackendUpsert, PromptUpsert
from . import service

llmbackendRouter = APIRouter(
    prefix="/backends",
    tags=["llmbackends"]
)

@llmbackendRouter.get("/")
def get_llmbackend(db: Session = Depends(get_db)):
    service = service.LLMBackendService()
    return service.list_llmbackends(db)


@llmbackendRouter.post("/")
def upsert_llmbackend(llm: LLMBackendUpsert, db: Session = Depends(get_db)):
    service.upsert_llmbackend(db, llm)


promptRouter = APIRouter(
    prefix="/prompts",
    tags=["prompts"]
)

@promptRouter.get("/")
def get_prompt(db: Session = Depends(get_db)):
    return service.list_prompts(db)


@promptRouter.post("/")
def upsert_prompt(prompt: PromptUpsert, db: Session = Depends(get_db)):
    service.upsert_prompt(db, prompt)