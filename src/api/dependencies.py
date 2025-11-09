"""Dependency injection for FastAPI routes."""
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from src.llms.base import LLMFactory, BaseLLM
from src.agents.graphs.base import GraphFactory
from src.core.config import settings
from src.utils.helpers import decode_access_token
from src.utils.logger import app_logger


def get_llm(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: Optional[float] = None
) -> BaseLLM:
    """
    Get LLM instance.
    
    Args:
        provider: LLM provider name
        model_name: Model name
        temperature: Temperature setting
        
    Returns:
        LLM instance
    """
    return LLMFactory.create(
        provider=provider,
        model_name=model_name,
        temperature=temperature
    )


def get_graph(
    graph_type: str,
    llm: BaseLLM = Depends(get_llm),
    **kwargs
):
    """
    Get compiled graph.
    
    Args:
        graph_type: Type of graph to create
        llm: LLM instance
        **kwargs: Additional arguments
        
    Returns:
        Compiled graph
    """
    return GraphFactory.create(graph_type, llm, **kwargs)


async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Verify API key from header (optional authentication).
    
    Args:
        x_api_key: API key from header
        
    Raises:
        HTTPException: If authentication is required and key is invalid
    """
    # If you want to enable API key authentication, implement it here
    # For now, this is a placeholder
    return True


async def verify_token(authorization: Optional[str] = Header(None)):
    """
    Verify JWT token from Authorization header.
    
    Args:
        authorization: Bearer token from header
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid
    """
    if not authorization:
        return None  # Optional authentication
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )


def get_current_user(token_payload: dict = Depends(verify_token)):
    """
    Get current authenticated user.
    
    Args:
        token_payload: Decoded token payload
        
    Returns:
        User information
    """
    if not token_payload:
        return None
    
    return {
        "user_id": token_payload.get("sub"),
        "email": token_payload.get("email")
    }
