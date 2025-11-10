"""
Deployable graph definitions for LangGraph Studio/CLI.
These are the entry points that LangGraph Studio will use.
"""
from langgraph.graph import StateGraph
from src.llms.base import LLMFactory
from src.agents.graphs.base import (
    ChatbotGraphBuilder,
    ChatbotWithToolsGraphBuilder,
    ResearchGraphBuilder,
    WriterGraphBuilder
)
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


# For direct access
__all__ = [
    "chatbot_graph",
    "chatbot_with_tools_graph", 
    "research_graph",
    "writer_graph"
]
