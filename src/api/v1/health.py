"""Health check and utility endpoints."""
from datetime import datetime
from fastapi import APIRouter
from src.schemas.api import HealthResponse, AgentInfoResponse
from src.core.config import settings
from src.utils.helpers import format_timestamp

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status information
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=settings.environment,
        timestamp=format_timestamp()
    )


@router.get("/info", response_model=AgentInfoResponse)
async def agent_info():
    """
    Get information about available agents and configuration.
    
    Returns:
        Agent configuration information
    """
    return AgentInfoResponse(
        agent_type="multi-purpose",
        available_tools=["web_search", "calculator"],
        llm_provider=settings.default_llm_provider,
        model_name=settings.default_model
    )


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API welcome message
    """
    return {
        "message": "Welcome to Agentic AI Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
