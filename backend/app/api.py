from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .model import get_db
from .schema import LLMBackendUpsert, PromptUpsert, GenRequest
from . import service

llmbackendRouter = APIRouter(
    prefix="/backends",
    tags=["llmbackends"]
)

@llmbackendRouter.get("/")
def get_llmbackend(db: Session = Depends(get_db)):
    srv = service.LLMBackendService(db)
    return srv.list()


@llmbackendRouter.post("/")
def upsert_llmbackend(llm: LLMBackendUpsert, db: Session = Depends(get_db)):
    srv = service.LLMBackendService(db)
    srv.upsert(llm.model_dump())

@llmbackendRouter.delete("/{id}")
def delete_llmbackend(id: int, db: Session = Depends(get_db)):
    srv = service.LLMBackendService(db)
    srv.delete(id)


promptRouter = APIRouter(
    prefix="/prompts",
    tags=["prompts"]
)

@promptRouter.get("/")
def get_prompt(db: Session = Depends(get_db)):
    srv = service.PromptService(db)
    return srv.list()


@promptRouter.post("/")
def upsert_prompt(prompt: PromptUpsert, db: Session = Depends(get_db)):
    srv = service.PromptService(db)
    srv.upsert(prompt.model_dump())

@promptRouter.delete("/")
def delete_prompt(id: int, db: Session = Depends(get_db)):
    srv = service.PromptService(db)
    srv.delete(id)

automcRouter = APIRouter(
    prefix="/multichoices",
    tags=["multichoices"]
)

@automcRouter.post("/generate")
def generate(gen_req: GenRequest, db: Session = Depends(get_db)):
    llm_srv = service.LLMBackendService(db)
    prompt_srv = service.PromptService(db)
    llm = llm_srv.get(gen_req.llm_id)
    if not llm:
        raise HTTPException(status_code=404, detail="llm not found")
    prompt = prompt_srv.get(gen_req.prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="prompt not found")
    
    srv = service.MultiChoiceService(llm, prompt)
    return srv.invoke(gen_req.content)