"""
Deployable graph definitions for LangGraph Studio/CLI.
These are the entry points that LangGraph Studio will use.
"""
import os

# CRITICAL: Set LangSmith environment variables FIRST, before any LangChain imports
# This ensures tracing is enabled from the start
from dotenv import load_dotenv
load_dotenv()  # Load .env file

# Set environment variables explicitly for LangSmith tracing
# Convert string 'true'/'false' to proper values
tracing_enabled = os.getenv('LANGCHAIN_TRACING_V2', '').lower() in ('true', '1', 'yes')
if tracing_enabled:
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    api_key = os.getenv('LANGCHAIN_API_KEY', '')
    if api_key:
        os.environ['LANGCHAIN_API_KEY'] = api_key
        os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT', 'agentic-ai-platform')
        os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
        print(f"✅ LangSmith tracing enabled for project: {os.environ['LANGCHAIN_PROJECT']}")

from langgraph.graph import StateGraph
from src.llms.base import LLMFactory
from src.agents.graphs.base import (
    ChatbotGraphBuilder,
    ChatbotWithToolsGraphBuilder,
    ResearchGraphBuilder,
    WriterGraphBuilder
)
from src.agents.graphs.news import NewsSummarizationGraph
from src.agents.graphs.redmine import AdaptiveRedmineChatbot
from src.core.config import settings


def get_default_llm():
    """Get default LLM from settings."""
    return LLMFactory.create(
        provider=settings.default_llm_provider,
        model_name=settings.default_model,
        temperature=settings.default_temperature
    )


# Export individual graphs for LangGraph Studio
def chatbot_graph() -> StateGraph:
    """Simple chatbot graph."""
    llm = get_default_llm()
    builder = ChatbotGraphBuilder(llm)
    return builder.build()


def chatbot_with_tools_graph() -> StateGraph:
    """Chatbot with tool integration."""
    llm = get_default_llm()
    builder = ChatbotWithToolsGraphBuilder(llm, tool_names=["web_search"])
    return builder.build()


def research_graph() -> StateGraph:
    """Research agent graph."""
    llm = get_default_llm()
    builder = ResearchGraphBuilder(llm)
    return builder.build()


def writer_graph() -> StateGraph:
    """Content writer graph."""
    llm = get_default_llm()
    builder = WriterGraphBuilder(llm)
    return builder.build()


def news_graph() -> StateGraph:
    """News summarization graph."""
    llm = get_default_llm()
    news_workflow = NewsSummarizationGraph(llm)
    return news_workflow.graph


def redmine_graph() -> StateGraph:
    """Redmine chatbot graph with adaptive RAG."""
    llm = get_default_llm()
    redmine_chatbot = AdaptiveRedmineChatbot(llm)
    return redmine_chatbot.graph


# For direct access
__all__ = [
    "chatbot_graph",
    "chatbot_with_tools_graph", 
    "research_graph",
    "writer_graph",
    "news_graph",
    "redmine_graph"
]
