"""Writer API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.api import WriterRequest, WriterResponse
from src.agents.graphs.base import WriterGraphBuilder
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.utils.logger import app_logger

router = APIRouter(prefix="/writer", tags=["Writer"])


@router.post("/", response_model=WriterResponse)
async def write_content(
    request: WriterRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Content writing endpoint that creates structured content.
    
    Args:
        request: Writer request with topic and settings
        llm: LLM instance from dependency
        
    Returns:
        Writer response with outline, draft, and final content
    """
    try:
        app_logger.info(f"Processing writer request: {request.topic}")
        
        # Create writer graph
        graph_builder = WriterGraphBuilder(llm)
        graph = graph_builder.build()
        
        # Create input state
        input_state = {
            "topic": request.topic,
            "content_type": request.content_type,
            "messages": []
        }
        
        # Invoke graph
        result = graph.invoke(input_state)
        
        return WriterResponse(
            topic=request.topic,
            outline=result.get("outline", ""),
            draft=result.get("draft", ""),
            final_content=result.get("final_content", ""),
            content_type=request.content_type
        )
        
    except Exception as e:
        app_logger.error(f"Writer error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Content writing failed: {str(e)}")
