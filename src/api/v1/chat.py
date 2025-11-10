"""Chat API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from src.schemas.api import ChatRequest, ChatResponse
from src.agents.graphs.base import ChatbotWithToolsGraphBuilder
from src.api.dependencies import get_llm
from src.llms.base import BaseLLM
from src.services.memory import memory_manager
from src.utils.logger import app_logger
from src.utils.helpers import generate_token

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm: BaseLLM = Depends(get_llm)
):
    """
    Chat endpoint with tool integration and conversation memory.
    
    Args:
        request: Chat request with message and optional conversation_id
        llm: LLM instance from dependency
        
    Returns:
        Chat response with AI message
    """
    try:
        app_logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or generate_token(16)
        
        # Get conversation history
        history_messages = memory_manager.get_messages(conversation_id)
        
        # Add current user message
        memory_manager.add_user_message(conversation_id, request.message)
        
        # Create graph with tools
        graph_builder = ChatbotWithToolsGraphBuilder(llm, tool_names=["web_search"])
        graph = graph_builder.build()
        
        # Create input state with history + new message
        all_messages = history_messages + [HumanMessage(content=request.message)]
        input_state = {
            "messages": all_messages
        }
        
        # Invoke graph
        result = graph.invoke(input_state)
        
        # Extract response
        last_message = result["messages"][-1]
        response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Save AI response to memory
        memory_manager.add_ai_message(conversation_id, response_content)
        
        # Get conversation metadata
        metadata = memory_manager.get_conversation_metadata(conversation_id)
        
        return ChatResponse(
            message=response_content,
            conversation_id=conversation_id,
            metadata={
                "message_count": metadata.get("message_count", 0),
                "has_tool_calls": any(hasattr(msg, 'tool_calls') and msg.tool_calls for msg in result["messages"]),
                "history_length": len(history_messages)
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


@router.get("/conversations")
async def list_conversations():
    """
    List all active conversations.
    
    Returns:
        List of conversation metadata
    """
    try:
        conversations = memory_manager.list_conversations()
        return {
            "conversations": conversations,
            "total": len(conversations)
        }
    except Exception as e:
        app_logger.error(f"List conversations error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history and metadata.
    
    Args:
        conversation_id: Conversation identifier
        
    Returns:
        Conversation details
    """
    try:
        messages = memory_manager.get_messages(conversation_id)
        metadata = memory_manager.get_conversation_metadata(conversation_id)
        
        # Format messages
        formatted_messages = [
            {
                "role": "user" if msg.__class__.__name__ == "HumanMessage" else "assistant",
                "content": msg.content
            }
            for msg in messages
        ]
        
        return {
            "conversation_id": conversation_id,
            "messages": formatted_messages,
            "metadata": metadata
        }
    except Exception as e:
        app_logger.error(f"Get conversation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation.
    
    Args:
        conversation_id: Conversation identifier
        
    Returns:
        Success message
    """
    try:
        memory_manager.delete_conversation(conversation_id)
        return {
            "message": f"Conversation {conversation_id} deleted",
            "success": True
        }
    except Exception as e:
        app_logger.error(f"Delete conversation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/{conversation_id}/clear")
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history (keep conversation but remove messages).
    
    Args:
        conversation_id: Conversation identifier
        
    Returns:
        Success message
    """
    try:
        memory_manager.clear_conversation(conversation_id)
        return {
            "message": f"Conversation {conversation_id} cleared",
            "success": True
        }
    except Exception as e:
        app_logger.error(f"Clear conversation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
