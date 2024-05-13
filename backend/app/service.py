from sqlmodel import Session, select
from .model import LLMBackend, Prompt
from .schema import LLMBackendUpsert, PromptUpsert


def upsert_llmbackend(session: Session, llm: LLMBackendUpsert):
    with session:
        if llm.id:
            existing = session.get(LLMBackend, llm.id)
            if existing:
                existing.name = llm.name
                existing.description = llm.description
                existing.url = llm.url
                existing.secret = llm.secret
            llm = existing
        if llm:
            session.add(llm)
        session.commit()


def upsert_prompt(session: Session, prompt: PromptUpsert):
    with session:
        if prompt.id:
            existing = session.get(Prompt, prompt.id)
            if existing:
                existing.template = prompt.template
            prompt = existing
        if prompt:
            session.add(prompt)
        session.commit()

def list_llmbackend(session: Session):
    with session:
        llms = select(LLMBackend)
        return list(llms)
    
def list_prompts(session: Session):
    with session:
        prompts = select(Prompt)
        return list(prompts)


        
    