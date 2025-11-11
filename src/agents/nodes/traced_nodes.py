"""
Enhanced node functions with LangSmith @traceable decorators.
This demonstrates best practices from LangSmith documentation.
"""

from typing import Dict, Any
from langsmith import traceable
from langchain_core.messages import HumanMessage, AIMessage
from src.agents.states.base import ChatbotState, ResearchState, WriterState
from src.llms.base import BaseLLM
from src.utils.logger import app_logger


class TracedChatbotNode:
    """Chatbot node with explicit LangSmith tracing."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    @traceable(name="chatbot_process", run_type="chain")
    def process(self, state: ChatbotState) -> Dict[str, Any]:
        """
        Process chatbot message with LangSmith tracing.
        
        The @traceable decorator automatically:
        - Creates a trace in LangSmith
        - Logs inputs and outputs
        - Tracks execution time
        - Captures errors
        """
        app_logger.info("Processing chatbot node (traced)")
        
        try:
            messages = state["messages"]
            response = self.llm.invoke(messages)
            
            return {"messages": [response]}
        except Exception as e:
            app_logger.error(f"Chatbot node error: {str(e)}")
            error_message = AIMessage(content=f"Error: {str(e)}")
            return {"messages": [error_message]}


class TracedResearchNode:
    """Research node with detailed tracing."""
    
    def __init__(self, llm: BaseLLM, search_tool: Any):
        self.llm = llm
        self.search_tool = search_tool
    
    @traceable(name="research_search", run_type="tool")
    def search(self, state: ResearchState) -> Dict[str, Any]:
        """Search with explicit tracing."""
        app_logger.info(f"Searching for: {state.get('query')}")
        
        try:
            query = state.get("query", "")
            if not query:
                return {"search_results": [], "sources": []}
            
            results = self.search_tool.invoke(query)
            sources = [r.get("url", "") for r in results if "url" in r]
            
            app_logger.info(f"Found {len(results)} search results")
            return {
                "search_results": results,
                "sources": sources
            }
        except Exception as e:
            app_logger.error(f"Search error: {str(e)}")
            return {"search_results": [], "sources": []}
    
    @traceable(name="research_summarize", run_type="llm")
    def summarize(self, state: ResearchState) -> Dict[str, Any]:
        """Summarize with explicit tracing."""
        app_logger.info("Summarizing research results")
        
        try:
            results = state.get("search_results", [])
            if not results:
                return {"summary": "No results found."}
            
            # Create context
            context = "\n\n".join([
                f"Source: {r.get('url', 'Unknown')}\nContent: {r.get('content', '')}"
                for r in results[:5]
            ])
            
            prompt = f"""Based on the following search results, provide a comprehensive summary:

{context}

Please provide a clear, concise summary highlighting the key points."""
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            summary = response.content if hasattr(response, 'content') else str(response)
            
            return {"summary": summary}
        except Exception as e:
            app_logger.error(f"Summarization error: {str(e)}")
            return {"summary": f"Error during summarization: {str(e)}"}


class TracedWriterNode:
    """Content writer node with per-step tracing."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    @traceable(name="writer_create_outline", run_type="llm")
    def create_outline(self, state: WriterState) -> Dict[str, Any]:
        """Create outline with tracing."""
        app_logger.info(f"Creating outline for: {state.get('topic')}")
        
        try:
            topic = state.get("topic", "")
            content_type = state.get("content_type", "article")
            
            prompt = f"""Create a detailed outline for a {content_type} about: {topic}

Please structure the outline with:
1. Introduction
2. Main points (3-5 key sections)
3. Conclusion

Make it engaging and informative."""
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            outline = response.content if hasattr(response, 'content') else str(response)
            
            return {"outline": outline}
        except Exception as e:
            app_logger.error(f"Outline creation error: {str(e)}")
            return {"outline": f"Error creating outline: {str(e)}"}
    
    @traceable(name="writer_write_draft", run_type="llm")
    def write_draft(self, state: WriterState) -> Dict[str, Any]:
        """Write draft with tracing."""
        app_logger.info("Writing draft content")
        
        try:
            outline = state.get("outline", "")
            topic = state.get("topic", "")
            
            prompt = f"""Write a comprehensive draft based on this outline:

Topic: {topic}

Outline:
{outline}

Please write engaging, well-structured content following the outline."""
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            draft = response.content if hasattr(response, 'content') else str(response)
            
            return {"draft": draft}
        except Exception as e:
            app_logger.error(f"Draft writing error: {str(e)}")
            return {"draft": f"Error writing draft: {str(e)}"}
    
    @traceable(name="writer_polish", run_type="llm")
    def polish(self, state: WriterState) -> Dict[str, Any]:
        """Polish content with tracing."""
        app_logger.info("Polishing content")
        
        try:
            draft = state.get("draft", "")
            
            prompt = f"""Review and polish this draft. Improve:
- Clarity and readability
- Grammar and style
- Flow and transitions
- Engagement

Draft:
{draft}

Provide the polished final version."""
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            final = response.content if hasattr(response, 'content') else str(response)
            
            return {"final_content": final}
        except Exception as e:
            app_logger.error(f"Polishing error: {str(e)}")
            return {"final_content": draft}


# Utility function for custom tracing
@traceable(name="custom_agent_step", run_type="chain")
def traced_agent_step(step_name: str, inputs: Dict[str, Any], processor: callable) -> Dict[str, Any]:
    """
    Generic traced agent step.
    
    Example:
        result = traced_agent_step(
            "process_query",
            {"query": "Hello"},
            lambda x: {"response": "Hi"}
        )
    """
    app_logger.info(f"Executing traced step: {step_name}")
    return processor(inputs)
