"""Research API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.api import ResearchRequest, ResearchResponse
from src.agents.graphs.base import ResearchGraphBuilder
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.utils.logger import app_logger

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/", response_model=ResearchResponse)
async def research(
    request: ResearchRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Research endpoint that searches and summarizes information.
    
    Args:
        request: Research request with query
        llm: LLM instance from dependency
        
    Returns:
        Research response with summary and sources
    """
    try:
        app_logger.info(f"Processing research request: {request.query}")
        
        # Create research graph
        graph_builder = ResearchGraphBuilder(llm)
        graph = graph_builder.build()
        
        # Create input state
        input_state = {
            "query": request.query,
            "messages": []
        }
        
        # Invoke graph
        result = graph.invoke(input_state)
        
        return ResearchResponse(
            query=request.query,
            summary=result.get("summary", "No summary available"),
            sources=result.get("sources", []),
            search_results=result.get("search_results") if request.max_results else None
        )
        
    except Exception as e:
        app_logger.error(f"Research error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")
