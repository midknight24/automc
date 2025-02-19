from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek


class ModelProxy(ABC):
    @abstractmethod
    def chat_model(self, **kwargs):
        pass
    
class OpenAIProxy(ModelProxy):
    model = "gpt-4o-2024-11-20"
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
            self.model = "gpt-4o-2024-11-20"
        else:
            self.model = kwargs["model"]

        llm = ChatOpenAI(temperature=0.8, openai_api_base=kwargs["url"], openai_api_key=kwargs["key"], model=self.model)
        return llm
        

class AnthropicProxy(ModelProxy):
    model = "claude-3-5-sonnet-20240620"
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
            self.model = "claude-3-5-sonnet-20240620"
        else:
            self.model = kwargs["model"]

        llm = ChatAnthropic(anthropic_api_url=kwargs["url"], anthropic_api_key=kwargs["key"], model=self.model)
        return llm
    

class DeepseekProxy(ModelProxy):
    model = "deepseek-reasoner"
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
            self.model = "deepseek-reasoner"
        else:
            self.model = kwargs["model"]

        llm = ChatDeepSeek(api_base=kwargs["url"], api_key=kwargs["key"], model=self.model)
        return llm