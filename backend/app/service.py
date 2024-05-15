from sqlmodel import Session, select, SQLModel
from typing import Type, TypeVar, Generic, List
from .model import LLMBackend, Prompt
from .schema import LLMBackendUpsert, PromptUpsert
from pydantic import BaseModel

def list_llmbackends(session: Session):
    with session:
        statement = select(LLMBackend)
        llms = session.exec(statement)
        return list(llms)
    

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

def delete_llmbackend(session: Session, id: int):
    with session:
        backend = session.get(LLMBackend, id)
        if backend:
            session.delete(backend)
        session.commit()

def list_prompts(session: Session):
    with session:
        statement = select(Prompt)
        prompts = session.exec(statement)
        return list(prompts)

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


def delete_prompt(session: Session, id: int):
    with session:
        prompt = session.get(Prompt, id)
        if prompt:
            session.delete(prompt)
        session.commit()


T = TypeVar('T', bound=SQLModel)

class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    def list(self, session: Session):
        with session:
            statement = select(self.model)
            results = statement.exec()
            return list(results)
        
    def upsert(self, session: Session, object: BaseModel):
        with session:
            if hasattr(object, 'id') and object.id is not None:
                existing = session.get(self.model, object.id)
                if existing:
                    for k, v in object.items():
                        setattr(existing, k, v)
                    session.add(existing)
            else:
                newinstance = self.model(**object.model_dump())
                session.add(newinstance)
            session.commit()

    def delete(self, session: Session, id: int):
        with session:
            object = session.get(self.model, id)
            if object:
                session.delete(object)
            session.commit()

class LLMBackendService(CRUDBase[LLMBackend]):
    pass

class PromptService(CRUDBase[Prompt]):
    pass




        
    