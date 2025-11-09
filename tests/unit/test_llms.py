"""Unit tests for LLM module."""
import pytest
from src.llms.base import LLMFactory
from src.core.exceptions import ConfigurationException


def test_llm_factory_groq(monkeypatch):
    """Test LLM factory creates Groq LLM."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    
    llm = LLMFactory.create(provider="groq")
    assert llm is not None
    assert llm.model_name is not None


def test_llm_factory_invalid_provider():
    """Test LLM factory raises error for invalid provider."""
    with pytest.raises(ConfigurationException):
        LLMFactory.create(provider="invalid")
