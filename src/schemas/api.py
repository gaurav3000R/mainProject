"""Pydantic schemas for API requests and responses."""
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


# Request Schemas
class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    
    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ResearchRequest(BaseModel):
    """Request schema for research endpoint."""
    query: str = Field(..., min_length=1, max_length=500, description="Research query")
    max_results: int = Field(5, ge=1, le=10, description="Maximum search results")


class WriterRequest(BaseModel):
    """Request schema for content writing endpoint."""
    topic: str = Field(..., min_length=1, max_length=500, description="Content topic")
    content_type: Literal["blog", "article", "essay", "report"] = Field(
        "article",
        description="Type of content to generate"
    )
    tone: Optional[Literal["professional", "casual", "technical", "creative"]] = Field(
        "professional",
        description="Writing tone"
    )


class AgentConfigRequest(BaseModel):
    """Request schema for agent configuration."""
    agent_type: Literal["chatbot", "chatbot_with_tools", "research", "writer"] = Field(
        ...,
        description="Type of agent to create"
    )
    llm_provider: Optional[Literal["groq", "openai"]] = Field(
        None,
        description="LLM provider to use"
    )
    model_name: Optional[str] = Field(None, description="Specific model name")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Temperature")
    tools: Optional[List[str]] = Field(None, description="Tools to enable")


# Response Schemas
class MessageResponse(BaseModel):
    """Response schema for single message."""
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role (user/assistant/system)")
    timestamp: Optional[str] = Field(None, description="Message timestamp")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    message: str = Field(..., description="AI response message")
    conversation_id: str = Field(..., description="Conversation ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ResearchResponse(BaseModel):
    """Response schema for research endpoint."""
    query: str = Field(..., description="Original query")
    summary: str = Field(..., description="Research summary")
    sources: List[str] = Field(..., description="Source URLs")
    search_results: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Raw search results"
    )


class WriterResponse(BaseModel):
    """Response schema for writer endpoint."""
    topic: str = Field(..., description="Content topic")
    outline: str = Field(..., description="Content outline")
    draft: str = Field(..., description="Draft content")
    final_content: str = Field(..., description="Final polished content")
    content_type: str = Field(..., description="Type of content")


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
    timestamp: str = Field(..., description="Current timestamp")


class AgentInfoResponse(BaseModel):
    """Response schema for agent information."""
    agent_type: str = Field(..., description="Agent type")
    available_tools: List[str] = Field(..., description="Available tools")
    llm_provider: str = Field(..., description="LLM provider")
    model_name: str = Field(..., description="Model name")
