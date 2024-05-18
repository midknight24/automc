from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

class ModelProxy(ABC):
    @abstractmethod
    def chat_model(self, **kwargs):
        pass
    
class OpenAIProxy(ModelProxy):
    def chat_model(self, **kwargs):
        """
        chat_model returns the ChatOpenAI class instance
        must have params:
        - url: openai model (proxy) address
        - key: secret key for api
        """
        if "url" not in kwargs:
            raise TypeError("url param missing")
        if "key" not in kwargs:
            raise TypeError("key param missing")
        llm = ChatOpenAI(base_url=kwargs["url"], api_key=kwargs["key"])
        return llm
        