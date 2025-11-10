"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings, langsmith_enabled
from src.api.middlewares.base import (
    LoggingMiddleware,
    ErrorHandlerMiddleware,
    RateLimitMiddleware,
    CORSHeadersMiddleware
)
from src.api.v1 import chat, research, writer, health
from src.utils.logger import app_logger
from src.utils.langsmith import verify_langsmith_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    app_logger.info("Starting Agentic AI Platform...")
    app_logger.info(f"Environment: {settings.environment}")
    app_logger.info(f"Debug mode: {settings.debug}")
    
    # Verify LangSmith connection
    if langsmith_enabled:
        verify_langsmith_connection()
    else:
        app_logger.warning("LangSmith tracing is disabled. Enable in .env with LANGCHAIN_TRACING_V2=true")
    
    yield
    
    # Shutdown
    app_logger.info("Shutting down Agentic AI Platform...")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Agentic AI Platform",
        description="Production-ready Agentic AI platform with LangGraph and FastAPI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )
    
    # Custom Middlewares (order matters!)
    app.add_middleware(CORSHeadersMiddleware)
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Rate Limiting (optional - uncomment to enable)
    if settings.is_production:
        app.add_middleware(
            RateLimitMiddleware,
            max_requests=settings.rate_limit_per_minute,
            window_seconds=60
        )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(chat.router, prefix=settings.api_v1_prefix)
    app.include_router(research.router, prefix=settings.api_v1_prefix)
    app.include_router(writer.router, prefix=settings.api_v1_prefix)
    
    return app


# Create app instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
