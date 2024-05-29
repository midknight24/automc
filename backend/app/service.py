from sqlmodel import Session, select, SQLModel
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from .model import LLMBackend, Prompt, ModelVendor
from .schema import Prompt as PromptSchema
import langchain
import yaml

class CRUDBase():
    session: Session
    model: SQLModel

    def __init__(self, session):
        if not hasattr(self, 'model'):
            raise TypeError(f'model class attribute missing')
        self.session = session
    
    def get(self, id):
        with self.session:
            existing = self.session.get(self.model, id)
            return existing
            


    def list(self):
        with self.session:
            statement = select(self.model)
            results = self.session.exec(statement)
            return list(results)
        
    def upsert(self, object: dict):
        with self.session:
            if 'id' in object and object['id'] is not None:
                existing = self.session.get(self.model, object['id'])
                if existing:
                    for k, v in object.items():
                        setattr(existing, k, v)
                    self.session.add(existing)
            else:
                newinstance = self.model(**object)
                # newinstance = self.model(**object.model_dump())
                self.session.add(newinstance)
            self.session.commit()

    def delete(self, id: int):
        with self.session:
            object = self.session.get(self.model, id)
            if object:
                self.session.delete(object)
            self.session.commit()

class LLMBackendService(CRUDBase):
    model = LLMBackend

class PromptService(CRUDBase):
    model = Prompt

class Answer(BaseModel):
    choice: str = Field(description="正确选项的编号")
    why: str = Field(description="正确选项是问题答案的解释")

class MultiChoice(BaseModel):
    question: str = Field(description="选择题的题干")
    choices: str = Field(description="选择题的选项，包含英文编号和选项描述")
    answers: Answer = Field(description="选择题的答案")


class MultiChoiceService():
    def __init__(self, llm: LLMBackend, prompt: Prompt):
        self.llm = llm
        self.prompt = prompt
        

    def invoke(self, content: str, model: str):
        if "{content}" not in self.prompt.template:
            raise TypeError("'{content}' must be in prompt template")
        prompt = ChatPromptTemplate.from_template(template=self.prompt.template)
        llm = None
        if self.llm.model_vendor == ModelVendor.OPENAI:
            from .vendor import OpenAIProxy
            llm = OpenAIProxy().chat_model(url=self.llm.url, key=self.llm.secret, model=model)
        elif self.llm.model_vendor == ModelVendor.ANTHROPIC:
            from .vendor import AnthropicProxy
            llm = AnthropicProxy().chat_model(url=self.llm.url, key=self.llm.secret, model=model)
        if not llm:
            raise TypeError("unsupported llm vendor")
        
        parser = JsonOutputParser(pydantic_object=MultiChoice)
        langchain.debug = True
        try:
            chain = prompt | llm | parser
            ret = chain.invoke({'content': content})
        except Exception as e:
            print(e)
            raise e
        return ret

    def load_prompt(self, path="prompt.yaml"):
        with open(path, encoding="utf-8") as file:
            out = yaml.safe_load(file)
        return PromptSchema(**out)