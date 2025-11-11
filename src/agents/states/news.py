"""State definitions for news summarization workflow."""

from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage


class NewsSummaryState(TypedDict):
    """State for news summarization workflow."""
    
    # Input
    query: str
    max_results: int
    
    # Intermediate
    news_articles: List[Dict[str, Any]]
    
    # Output
    summary: str
    saved_path: Optional[str]
    
    # Metadata
    error: Optional[str]
    status: str
