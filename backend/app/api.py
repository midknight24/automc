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
    srv = service.LLMBackendService()
    return srv.list(db)


@llmbackendRouter.post("/")
def upsert_llmbackend(llm: LLMBackendUpsert, db: Session = Depends(get_db)):
    srv = service.LLMBackendService()
    srv.upsert(db, llm.model_dump())


promptRouter = APIRouter(
    prefix="/prompts",
    tags=["prompts"]
)

@promptRouter.get("/")
def get_prompt(db: Session = Depends(get_db)):
    srv = service.PromptService()
    return srv.list(db)


@promptRouter.post("/")
def upsert_prompt(prompt: PromptUpsert, db: Session = Depends(get_db)):
    srv = service.PromptService()
    srv.upsert(db, prompt.model_dump())