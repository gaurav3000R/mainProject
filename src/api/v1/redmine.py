"""Redmine chatbot API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.agents.graphs.redmine import AdaptiveRedmineChatbot
from src.services.memory import memory_manager
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.utils.logger import app_logger
from src.utils.helpers import generate_token

router = APIRouter(prefix="/redmine", tags=["Redmine"])


class RedmineChatRequest(BaseModel):
    """Request for Redmine chatbot."""
    message: str = Field(..., description="User message", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")


class RedmineChatResponse(BaseModel):
    """Response from Redmine chatbot."""
    message: str
    conversation_id: str
    tool_calls: List[str] = []
    metadata: Dict[str, Any] = {}


class RedmineValidateResponse(BaseModel):
    """Response from Redmine validation."""
    success: bool
    message: str
    user_info: Optional[Dict[str, Any]] = None


@router.post("/chat", response_model=RedmineChatResponse)
async def chat_with_redmine(
    request: RedmineChatRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Chat with Redmine platform using natural language with Adaptive RAG.
    
    **Adaptive RAG Features:**
    - Intelligently routes queries to best datasource
    - Uses Redmine tools for real-time data
    - Falls back to web search for external info
    - Direct answers for simple queries
    - Self-correction via grading
    
    The chatbot can help you:
    - View projects and issues
    - Create and update issues
    - Search for specific information
    - Get time entries and analytics
    - Access project metadata
    
    Example queries:
    - "Show me all open issues" → Redmine tools
    - "What is Agile methodology?" → Direct answer
    - "How to configure CI/CD?" → Web search
    - "Create a new bug for project 5" → Redmine tools
    
    Args:
        request: Chat request with message
        llm: Language model instance
        
    Returns:
        Chat response with assistant message
    """
    try:
        app_logger.info(f"Adaptive RAG Redmine chat: {request.message[:100]}")
        
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or generate_token(16)
        
        # Get conversation history from memory
        history_messages = memory_manager.get_messages(conversation_id)
        
        # Create Adaptive RAG chatbot
        graph = AdaptiveRedmineChatbot(llm)
        
        # Prepare state with history
        state = {
            "messages": history_messages,
            "conversation_id": conversation_id,
            "current_project_id": None,
            "current_issue_id": None
        }
        
        # Process message
        result = await graph.achat(
            message=request.message,
            conversation_id=conversation_id,
            state=state if history_messages else None
        )
        
        # Extract response
        last_message = result["messages"][-1]
        response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Save to memory
        memory_manager.add_user_message(conversation_id, request.message)
        memory_manager.add_ai_message(conversation_id, response_content)
        
        # Extract tool calls if any
        tool_calls = []
        for msg in result["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                tool_calls.extend([tc['name'] for tc in msg.tool_calls])
        
        return RedmineChatResponse(
            message=response_content,
            conversation_id=conversation_id,
            tool_calls=tool_calls,
            metadata={
                "message_count": len(result["messages"]),
                "tools_used": len(tool_calls) > 0,
                "adaptive_rag": True
            }
        )
        
    except Exception as e:
        app_logger.error(f"Redmine chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.post("/validate", response_model=RedmineValidateResponse)
async def validate_redmine_connection():
    """
    Validate Redmine API connection and credentials.
    
    Returns:
        Validation result with user information
    """
    try:
        from src.services.redmine_client import redmine_client
        
        if not redmine_client:
            raise HTTPException(
                status_code=400,
                detail="Redmine API not configured. Set REDMIN_API_BASE_URL and REDMIN_API_KEY in .env"
            )
        
        user_info = await redmine_client.validate_connection()
        
        return RedmineValidateResponse(
            success=True,
            message="Successfully connected to Redmine",
            user_info=user_info.get("user", {})
        )
        
    except Exception as e:
        app_logger.error(f"Redmine validation error: {str(e)}")
        return RedmineValidateResponse(
            success=False,
            message=f"Failed to connect to Redmine: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    from src.services.redmine_client import redmine_client
    
    return {
        "status": "healthy",
        "service": "redmine_chatbot",
        "configured": redmine_client is not None
    }


@router.get("/capabilities")
async def get_capabilities():
    """
    Get list of chatbot capabilities.
    
    Returns:
        Available commands and features
    """
    return {
        "capabilities": [
            "View all projects",
            "List issues (open, closed, or all)",
            "Get issue details by ID",
            "Create new issues",
            "Update existing issues",
            "Search issues by keywords",
            "View time entries",
            "Get project metadata (statuses, priorities, trackers)"
        ],
        "example_queries": [
            "Show me all projects",
            "What are the open issues?",
            "Show details of issue #123",
            "Create a new bug in project 5: Fix login error",
            "Update issue #45 status to closed",
            "Search for issues about payment",
            "Show me time entries for project 3",
            "What statuses are available?"
        ],
        "tools_available": [
            "get_redmine_projects",
            "get_redmine_issues",
            "get_redmine_issue_details",
            "create_redmine_issue",
            "update_redmine_issue",
            "search_redmine_issues",
            "get_redmine_time_entries",
            "get_redmine_metadata"
        ]
    }
