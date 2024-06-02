from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


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
        if "model" not in kwargs or kwargs["model"] == "":
            model = "gpt-4o"
        else:
            model = kwargs["model"]

        llm = ChatOpenAI(temperature=0.8, openai_api_base=kwargs["url"], openai_api_key=kwargs["key"], model=model)
        return llm
        

class AnthropicProxy(ModelProxy):
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
        
        if "model" not in kwargs or kwargs["model"] == "":
            model = "claude-3-opus-20240229"
        else:
            model = kwargs["model"]

        llm = ChatAnthropic(anthropic_api_url=kwargs["url"], anthropic_api_key=kwargs["key"], model=model)
        return llm