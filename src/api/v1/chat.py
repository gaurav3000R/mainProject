"""Chat API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from src.schemas.api import ChatRequest, ChatResponse
from src.agents.graphs.base import ChatbotWithToolsGraphBuilder
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.utils.logger import app_logger
from src.utils.helpers import generate_token

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Chat endpoint with tool integration.
    
    Args:
        request: Chat request with message
        llm: LLM instance from dependency
        
    Returns:
        Chat response with AI message
    """
    try:
        app_logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Create graph with tools
        graph_builder = ChatbotWithToolsGraphBuilder(llm, tool_names=["web_search"])
        graph = graph_builder.build()
        
        # Create input state
        input_state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        # Invoke graph
        result = graph.invoke(input_state)
        
        # Extract response
        last_message = result["messages"][-1]
        response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Generate conversation ID
        conversation_id = request.conversation_id or generate_token(16)
        
        return ChatResponse(
            message=response_content,
            conversation_id=conversation_id,
            metadata={
                "message_count": len(result["messages"]),
                "has_tool_calls": any(hasattr(msg, 'tool_calls') and msg.tool_calls for msg in result["messages"])
            }
        )
        
    except Exception as e:
        app_logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/simple", response_model=ChatResponse)
async def simple_chat(
    request: ChatRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Simple chat endpoint without tools.
    
    Args:
        request: Chat request with message
        llm: LLM instance from dependency
        
    Returns:
        Chat response with AI message
    """
    try:
        app_logger.info(f"Processing simple chat: {request.message[:50]}...")
        
        # Direct LLM invocation
        messages = [HumanMessage(content=request.message)]
        response = llm.invoke(messages)
        
        response_content = response.content if hasattr(response, 'content') else str(response)
        conversation_id = request.conversation_id or generate_token(16)
        
        return ChatResponse(
            message=response_content,
            conversation_id=conversation_id,
            metadata={"mode": "simple"}
        )
        
    except Exception as e:
        app_logger.error(f"Simple chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
