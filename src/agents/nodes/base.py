"""Node functions for agent workflows."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.states.base import AgentState, ChatbotState, ResearchState, WriterState
from src.llms.base import BaseLLM
from src.utils.logger import app_logger


class ChatbotNode:
    """Simple chatbot node for conversations."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    def process(self, state: ChatbotState) -> Dict[str, Any]:
        """
        Process chatbot message.
        
        Args:
            state: Current chatbot state
            
        Returns:
            Updated state with AI response
        """
        app_logger.info("Processing chatbot node")
        
        try:
            messages = state["messages"]
            response = self.llm.invoke(messages)
            
            return {"messages": [response]}
        except Exception as e:
            app_logger.error(f"Chatbot node error: {str(e)}")
            error_message = AIMessage(content=f"I apologize, but I encountered an error: {str(e)}")
            return {"messages": [error_message]}


class ResearchNode:
    """Research node that searches and summarizes information."""
    
    def __init__(self, llm: BaseLLM, search_tool: Any):
        self.llm = llm
        self.search_tool = search_tool
    
    def search(self, state: ResearchState) -> Dict[str, Any]:
        """
        Search for information on the query.
        
        Args:
            state: Research state with query
            
        Returns:
            Updated state with search results
        """
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
    
    def summarize(self, state: ResearchState) -> Dict[str, Any]:
        """
        Summarize search results.
        
        Args:
            state: Research state with search results
            
        Returns:
            Updated state with summary
        """
        app_logger.info("Summarizing research results")
        
        try:
            results = state.get("search_results", [])
            if not results:
                return {"summary": "No results found."}
            
            # Create context from search results
            context = "\n\n".join([
                f"Source: {r.get('url', 'Unknown')}\nContent: {r.get('content', '')}"
                for r in results[:5]  # Limit to top 5 results
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


class WriterNode:
    """Content writing node."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    def create_outline(self, state: WriterState) -> Dict[str, Any]:
        """
        Create content outline.
        
        Args:
            state: Writer state with topic
            
        Returns:
            Updated state with outline
        """
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
    
    def write_draft(self, state: WriterState) -> Dict[str, Any]:
        """
        Write content draft.
        
        Args:
            state: Writer state with outline
            
        Returns:
            Updated state with draft
        """
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
    
    def polish(self, state: WriterState) -> Dict[str, Any]:
        """
        Polish and finalize content.
        
        Args:
            state: Writer state with draft
            
        Returns:
            Updated state with final content
        """
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
            return {"final_content": draft}  # Return draft if polishing fails
