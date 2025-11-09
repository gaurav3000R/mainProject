"""Base LLM interface and factory."""
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.core.config import settings
from src.core.exceptions import LLMException, ConfigurationException
from src.utils.logger import app_logger


class BaseLLM(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, model_name: Optional[str] = None, temperature: Optional[float] = None):
        self.model_name = model_name or settings.default_model
        self.temperature = temperature or settings.default_temperature
        self._client: Optional[BaseChatModel] = None
    
    @abstractmethod
    def get_client(self) -> BaseChatModel:
        """Get the LLM client instance."""
        pass
    
    def invoke(self, messages: List[Any], **kwargs) -> Any:
        """Invoke the LLM with messages."""
        try:
            client = self.get_client()
            return client.invoke(messages, **kwargs)
        except Exception as e:
            app_logger.error(f"LLM invocation failed: {str(e)}")
            raise LLMException(f"LLM invocation failed: {str(e)}")
    
    async def ainvoke(self, messages: List[Any], **kwargs) -> Any:
        """Async invoke the LLM with messages."""
        try:
            client = self.get_client()
            return await client.ainvoke(messages, **kwargs)
        except Exception as e:
            app_logger.error(f"LLM async invocation failed: {str(e)}")
            raise LLMException(f"LLM async invocation failed: {str(e)}")
    
    def stream(self, messages: List[Any], **kwargs):
        """Stream responses from the LLM."""
        try:
            client = self.get_client()
            return client.stream(messages, **kwargs)
        except Exception as e:
            app_logger.error(f"LLM streaming failed: {str(e)}")
            raise LLMException(f"LLM streaming failed: {str(e)}")


class GroqLLM(BaseLLM):
    """Groq LLM implementation."""
    
    def __init__(self, model_name: Optional[str] = None, temperature: Optional[float] = None):
        super().__init__(model_name, temperature)
        if not settings.groq_api_key:
            raise ConfigurationException("GROQ_API_KEY not configured")
    
    def get_client(self) -> ChatGroq:
        """Get Groq client."""
        if self._client is None:
            self._client = ChatGroq(
                api_key=settings.groq_api_key,
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=settings.default_max_tokens
            )
            app_logger.info(f"Initialized Groq LLM with model: {self.model_name}")
        return self._client


class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation."""
    
    def __init__(self, model_name: Optional[str] = None, temperature: Optional[float] = None):
        super().__init__(model_name or "gpt-4", temperature)
        if not settings.openai_api_key:
            raise ConfigurationException("OPENAI_API_KEY not configured")
    
    def get_client(self) -> ChatOpenAI:
        """Get OpenAI client."""
        if self._client is None:
            self._client = ChatOpenAI(
                api_key=settings.openai_api_key,
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=settings.default_max_tokens
            )
            app_logger.info(f"Initialized OpenAI LLM with model: {self.model_name}")
        return self._client


class LLMFactory:
    """Factory for creating LLM instances."""
    
    _providers = {
        "groq": GroqLLM,
        "openai": OpenAILLM
    }
    
    @classmethod
    def create(
        cls,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> BaseLLM:
        """Create LLM instance based on provider."""
        provider = provider or settings.default_llm_provider
        
        if provider not in cls._providers:
            raise ConfigurationException(
                f"Unknown LLM provider: {provider}. Available: {list(cls._providers.keys())}"
            )
        
        llm_class = cls._providers[provider]
        return llm_class(model_name=model_name, temperature=temperature)
    
    @classmethod
    def register_provider(cls, name: str, llm_class: type):
        """Register a new LLM provider."""
        cls._providers[name] = llm_class
        app_logger.info(f"Registered LLM provider: {name}")
