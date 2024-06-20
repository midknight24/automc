from sqlmodel import Session, select, SQLModel
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import langchain
import yaml
import os
from .model import LLMBackend, Prompt, ModelVendor
from .schema import PlayWright as PromptSchema, Evaluation, EvaluationFailed, TextTypeMap
from .config import VALID_QUIZ_SCORE
from .utils import async_wrapper
import asyncio
from asyncio import Task

langchain.debug = True

def load_prompt(path="prompt.yaml"):
    import os
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, path)
    with open(prompt_path, encoding="utf-8") as file:
        out = yaml.safe_load(file)
    return PromptSchema(**out)


    
def load_playwright(path):
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, path)
    with open(prompt_path, encoding="utf-8") as file:
        out = yaml.safe_load(file)
    return PromptSchema(**out)

def load_oneshot(path):
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, path)
    with open(prompt_path, encoding="utf-8") as file:
        return file.read()

playwright = load_playwright(path="prompt.yaml")
oneshot_promot = load_oneshot(path="prompt-oneshot.yaml")

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

    store = {}

    def _get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]


    def __init__(self, llm: LLMBackend):
        self.llm = llm
        
    def load_llm(self, model):
        llm = None
        if self.llm.model_vendor == ModelVendor.OPENAI:
            from .vendor import OpenAIProxy
            llm = OpenAIProxy().chat_model(url=self.llm.url, key=self.llm.secret, model=model)
        elif self.llm.model_vendor == ModelVendor.ANTHROPIC:
            from .vendor import AnthropicProxy
            llm = AnthropicProxy().chat_model(url=self.llm.url, key=self.llm.secret, model=model)
        if not llm:
            raise TypeError("unsupported llm vendor")
        return llm
    
    def log_history(self, path, key):
        with open(path, "w", encoding="utf-8") as file:
            file.write(str(self.store[key]))

    async def invoke_oneshot(self, content: str, model: str | None):
        prompt = ChatPromptTemplate.from_template(template=oneshot_promot)
        llm = self.load_llm(model)
        parser = JsonOutputParser(pydantic_object=MultiChoice)
        try:
            chain = prompt | llm | parser
            ret = chain.invoke({'content': content})
        except Exception as e:
            print(e)
            raise e
        return ret


    async def invoke(self, content: str, model: str | None, pick_best=True, oneshot=False):

        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        llm = self.load_llm(model)
        runnable = prompt | llm
        
        results = {}
        if oneshot:
            oneshot_task = asyncio.create_task(self.invoke_oneshot(content, model))

        # create history based chain
        with_message_history = RunnableWithMessageHistory(
            runnable,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        # enter question input evaluation
        parser = JsonOutputParser(pydantic_object=Evaluation)
        chain = with_message_history | parser
        intro = ChatPromptTemplate.from_template(template=playwright.intro)

        rendered = intro.invoke({"content": content}).to_messages()
        out = chain.invoke(
            {"input": rendered},
            config={"configurable": {"session_id": "tmp"}}
        )
        evalution = Evaluation(**out)

        if evalution.validity < VALID_QUIZ_SCORE:
            print(evalution)
            return EvaluationFailed(
                message="哦！看起来您的输入不太适合转变成选择题。。",
                explaination=evalution.explaination
            )


        # ask for more background on input topic
        with_message_history.invoke(
            {"input": playwright.intro2},
            config={"configurable": {"session_id": "tmp"}}
        )

        # enter main prompt
        parser = JsonOutputParser(pydantic_object=MultiChoice)
        tmp_chain = with_message_history | parser
        ret1 = tmp_chain.invoke(
            {"input": playwright.mainPrompt},
            config={"configurable": {"session_id": "tmp"}}   
        )

        results["full"] = ret1
        

        # ask for type specific generation
        ret2 = tmp_chain.invoke(
            {
                "input": playwright.encore + '\n' + 
                getattr(playwright.type_specs, TextTypeMap[evalution.text_type]).patch_prompt
            },
            config={"configurable": {"session_id": "tmp"}}
        )

        results["encore"] = ret2


        if pick_best:
            # ask to choose and improve final output
            final = with_message_history | parser
            ret_best = final.invoke(
                {"input": playwright.pick_and_improve},
                config={"configurable": {"session_id": "tmp"}}
            )
            results["best"] = ret_best

        if oneshot:
            results["oneshot"] = await oneshot_task

        self.log_history("history.txt", "tmp")

        # cleanup history
        del self.store["tmp"]

        return results

    
