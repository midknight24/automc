from sqlmodel import Session, select, SQLModel
from typing import Type, TypeVar, Generic, List
from .model import LLMBackend, Prompt
from .schema import LLMBackendUpsert, PromptUpsert
from pydantic import BaseModel

T = TypeVar('T', bound=SQLModel)

class CRUDBase(Generic[T]):
    model: SQLModel

    def __init__(self):
        if not hasattr(self, 'model'):
            raise TypeError(f'model class attribute missing')
    
    def list(self, session: Session):
        with session:
            statement = select(self.model)
            results = session.exec(statement)
            return list(results)
        
    def upsert(self, session: Session, object: dict):
        with session:
            if 'id' in object and object['id'] is not None:
                existing = session.get(self.model, object['id'])
                if existing:
                    for k, v in object.items():
                        setattr(existing, k, v)
                    session.add(existing)
            else:
                newinstance = self.model(**object)
                # newinstance = self.model(**object.model_dump())
                session.add(newinstance)
            session.commit()

    def delete(self, session: Session, id: int):
        with session:
            object = session.get(self.model, id)
            if object:
                session.delete(object)
            session.commit()

class LLMBackendService(CRUDBase):
    model = LLMBackend

class PromptService(CRUDBase):
    model = Prompt




        
    