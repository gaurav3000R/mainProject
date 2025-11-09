"""State schemas for LangGraph agents."""
from typing import List, Optional, Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    Base state for agent workflows.
    
    Attributes:
        messages: List of messages with automatic message appending
        current_step: Current step in the workflow
        metadata: Additional metadata
    """
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: Optional[str]
    metadata: Optional[dict]


class ChatbotState(TypedDict):
    """State for simple chatbot agents."""
    messages: Annotated[List[BaseMessage], add_messages]


class ResearchState(TypedDict):
    """
    State for research agents.
    
    Attributes:
        messages: Conversation messages
        query: Research query
        search_results: Results from web search
        summary: Summarized research findings
        sources: List of source URLs
    """
    messages: Annotated[List[BaseMessage], add_messages]
    query: str
    search_results: Optional[List[dict]]
    summary: Optional[str]
    sources: Optional[List[str]]


class WriterState(TypedDict):
    """
    State for content writing agents.
    
    Attributes:
        messages: Conversation messages
        topic: Writing topic
        outline: Content outline
        draft: Draft content
        final_content: Final polished content
        content_type: Type of content (blog, article, etc.)
    """
    messages: Annotated[List[BaseMessage], add_messages]
    topic: str
    outline: Optional[str]
    draft: Optional[str]
    final_content: Optional[str]
    content_type: str


class MultiAgentState(TypedDict):
    """
    State for multi-agent collaboration.
    
    Attributes:
        messages: Shared messages
        current_agent: Currently active agent
        next_agent: Next agent to execute
        task: Task description
        result: Final result
        agent_outputs: Outputs from individual agents
    """
    messages: Annotated[List[BaseMessage], add_messages]
    current_agent: Optional[str]
    next_agent: Optional[str]
    task: str
    result: Optional[str]
    agent_outputs: Optional[dict]
