"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from src.core.config import settings


@pytest.fixture
def test_settings():
    """Test settings fixture."""
    settings.environment = "test"
    settings.debug = True
    return settings


@pytest.fixture
def client():
    """Test client fixture."""
    from main import app
    return TestClient(app)


@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    class MockLLM:
        def invoke(self, messages):
            class MockResponse:
                content = "Mock response"
            return MockResponse()
        
        def get_client(self):
            return self
    
    return MockLLM()
