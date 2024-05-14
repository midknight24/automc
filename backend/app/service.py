from sqlmodel import Session, select
from .model import LLMBackend, Prompt
from .schema import LLMBackendUpsert, PromptUpsert


def upsert_llmbackend(session: Session, upsert: LLMBackendUpsert):
    with session:
        if upsert.id is not None:
            existing = session.get(LLMBackend, upsert.id)
            if existing:
                existing.name = upsert.name
                existing.description = upsert.description
                existing.url = upsert.url
                existing.secret = upsert.secret
                session.add(existing)
        else:
            llm = LLMBackend(
                name=upsert.name,
                description=upsert.description,
                url=upsert.url,
                secret=upsert.secret
            )
            session.add(llm)
        session.commit()


def upsert_prompt(session: Session, upsert: PromptUpsert):
    with session:
        if upsert.id is not None:
            existing = session.get(Prompt, upsert.id)
            if existing:
                existing.template = upsert.template
                session.add(existing)
        else:
            prompt = Prompt(
                template=upsert.template
            )
            session.add(prompt)
        session.commit()

def list_llmbackends(session: Session):
    with session:
        statement = select(LLMBackend)
        llms = session.exec(statement)
        return list(llms)
    
def list_prompts(session: Session):
    with session:
        statement = select(Prompt)
        prompts = session.exec(statement)
        return list(prompts)


        
    