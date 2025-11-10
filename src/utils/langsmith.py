"""
LangSmith integration utilities.
Provides helpers for tracing and monitoring.
"""
from typing import Optional
from src.core.config import settings, langsmith_enabled
from src.utils.logger import app_logger


def is_langsmith_enabled() -> bool:
    """Check if LangSmith tracing is enabled."""
    return langsmith_enabled


def get_langsmith_url() -> Optional[str]:
    """Get LangSmith project URL."""
    if not langsmith_enabled:
        return None
    return f"{settings.langchain_endpoint}/projects/p/{settings.langchain_project}"


def verify_langsmith_connection() -> bool:
    """
    Verify LangSmith connection.
    
    Returns:
        True if connected successfully, False otherwise
    """
    if not langsmith_enabled:
        app_logger.warning("LangSmith is not enabled. Check your .env configuration.")
        return False
    
    try:
        from langsmith import Client
        
        client = Client(
            api_key=settings.langchain_api_key,
            api_url=settings.langchain_endpoint
        )
        
        # Try to get projects to verify connection
        try:
            client.read_project(project_name=settings.langchain_project)
            app_logger.info(f"✅ LangSmith connected successfully!")
            app_logger.info(f"📊 Project: {settings.langchain_project}")
            app_logger.info(f"🔗 URL: {get_langsmith_url()}")
            return True
        except Exception as e:
            # Project might not exist, try to create it
            app_logger.info(f"Creating new LangSmith project: {settings.langchain_project}")
            client.create_project(
                project_name=settings.langchain_project,
                description="Agentic AI Platform - LangGraph Applications"
            )
            app_logger.info(f"✅ LangSmith project created and connected!")
            app_logger.info(f"🔗 URL: {get_langsmith_url()}")
            return True
            
    except ImportError:
        app_logger.error("langsmith package not installed. Run: uv add langsmith")
        return False
    except Exception as e:
        app_logger.error(f"❌ LangSmith connection failed: {str(e)}")
        return False


def log_trace_url(run_id: str) -> None:
    """Log the trace URL for a specific run."""
    if langsmith_enabled:
        trace_url = f"{settings.langchain_endpoint}/public/{run_id}"
        app_logger.info(f"🔍 View trace: {trace_url}")
