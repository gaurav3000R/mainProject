"""State definition for Redmine chatbot."""

from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RedmineChatState(TypedDict):
    """State for Redmine chatbot workflow."""
    
    # Messages history
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Conversation context
    conversation_id: str
    
    # Redmine context
    current_project_id: int | None
    current_issue_id: int | None
