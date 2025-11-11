"""News summarization API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.agents.graphs.news import NewsSummarizationGraph
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.utils.logger import app_logger

router = APIRouter(prefix="/news", tags=["News"])


class NewsSummaryRequest(BaseModel):
    """Request for news summarization."""
    query: str = Field(..., description="Search query for news", min_length=1)
    max_results: int = Field(default=5, description="Maximum number of articles", ge=1, le=20)


class NewsSummaryResponse(BaseModel):
    """Response from news summarization."""
    success: bool
    query: str
    articles_count: int
    summary: str
    saved_path: Optional[str] = None
    status: str
    error: Optional[str] = None


class ArticleDetail(BaseModel):
    """Detailed article information."""
    title: str
    content: str
    url: Optional[str] = None
    source: Optional[str] = None


class NewsSummaryDetailResponse(BaseModel):
    """Detailed response with articles."""
    success: bool
    query: str
    articles: List[ArticleDetail]
    summary: str
    saved_path: Optional[str] = None
    status: str
    error: Optional[str] = None


@router.post("/summarize", response_model=NewsSummaryResponse)
async def summarize_news(
    request: NewsSummaryRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Fetch news, summarize, and save results.
    
    Workflow: Start → Fetch News (API) → Summarize → Save Result → End
    
    Args:
        request: News summary request with query
        llm: Language model instance
        
    Returns:
        Summary response
    
    Example:
        ```
        POST /api/v1/news/summarize
        {
            "query": "artificial intelligence news today",
            "max_results": 5
        }
        ```
    """
    try:
        app_logger.info(f"News summarization request: {request.query}")
        
        # Create and run workflow
        graph = NewsSummarizationGraph(llm)
        result = await graph.arun(
            query=request.query,
            max_results=request.max_results
        )
        
        # Build response
        return NewsSummaryResponse(
            success=result.get("status") == "completed",
            query=result.get("query", ""),
            articles_count=len(result.get("news_articles", [])),
            summary=result.get("summary", ""),
            saved_path=result.get("saved_path"),
            status=result.get("status", "unknown"),
            error=result.get("error")
        )
        
    except Exception as e:
        app_logger.error(f"News summarization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"News summarization failed: {str(e)}"
        )


@router.post("/summarize/detailed", response_model=NewsSummaryDetailResponse)
async def summarize_news_detailed(
    request: NewsSummaryRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Fetch news, summarize, and save results with detailed article information.
    
    Args:
        request: News summary request with query
        llm: Language model instance
        
    Returns:
        Detailed summary response with articles
    
    Example:
        ```
        POST /api/v1/news/summarize/detailed
        {
            "query": "climate change 2024",
            "max_results": 10
        }
        ```
    """
    try:
        app_logger.info(f"Detailed news summarization request: {request.query}")
        
        # Create and run workflow
        graph = NewsSummarizationGraph(llm)
        result = await graph.arun(
            query=request.query,
            max_results=request.max_results
        )
        
        # Format articles
        articles = [
            ArticleDetail(
                title=article.get("title", "Untitled"),
                content=article.get("content", ""),
                url=article.get("url"),
                source=article.get("source")
            )
            for article in result.get("news_articles", [])
        ]
        
        # Build response
        return NewsSummaryDetailResponse(
            success=result.get("status") == "completed",
            query=result.get("query", ""),
            articles=articles,
            summary=result.get("summary", ""),
            saved_path=result.get("saved_path"),
            status=result.get("status", "unknown"),
            error=result.get("error")
        )
        
    except Exception as e:
        app_logger.error(f"Detailed news summarization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"News summarization failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "news_summarization",
        "workflow": "Start → Fetch News → Summarize → Save → End"
    }
