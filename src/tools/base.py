"""Tools for agents - web search, custom tools, etc."""
from typing import List, Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from langgraph.prebuilt import ToolNode
from src.core.config import settings
from src.core.exceptions import ToolException, ConfigurationException
from src.utils.logger import app_logger


def get_web_search_tool(max_results: int = 5) -> TavilySearchResults:
    """
    Get web search tool using Tavily.
    
    Args:
        max_results: Maximum number of search results
        
    Returns:
        TavilySearchResults tool instance
    """
    if not settings.tavily_api_key:
        raise ConfigurationException("TAVILY_API_KEY not configured")
    
    try:
        tool = TavilySearchResults(
            api_key=settings.tavily_api_key,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False
        )
        app_logger.info(f"Initialized Tavily search tool with max_results={max_results}")
        return tool
    except Exception as e:
        app_logger.error(f"Failed to initialize Tavily tool: {str(e)}")
        raise ToolException(f"Failed to initialize search tool: {str(e)}")


def get_calculator_tool() -> Tool:
    """Get calculator tool for mathematical operations."""
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression safely."""
        try:
            # Only allow safe mathematical operations
            allowed_chars = set("0123456789+-*/()., ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return Tool(
        name="calculator",
        func=calculator,
        description="Useful for mathematical calculations. Input should be a mathematical expression like '2 + 2' or '10 * 5'."
    )


def get_available_tools(tool_names: Optional[List[str]] = None) -> List[Tool]:
    """
    Get list of available tools.
    
    Args:
        tool_names: Optional list of tool names to include. If None, returns all.
        
    Returns:
        List of tool instances
    """
    all_tools = {
        "web_search": get_web_search_tool,
        "calculator": get_calculator_tool
    }
    
    if tool_names is None:
        tool_names = list(all_tools.keys())
    
    tools = []
    for name in tool_names:
        if name not in all_tools:
            app_logger.warning(f"Unknown tool requested: {name}")
            continue
        
        try:
            tool = all_tools[name]()
            tools.append(tool)
            app_logger.info(f"Added tool: {name}")
        except Exception as e:
            app_logger.error(f"Failed to initialize tool {name}: {str(e)}")
    
    return tools


def create_tool_node(tools: List[Tool]) -> ToolNode:
    """
    Create a LangGraph tool node.
    
    Args:
        tools: List of tools to include in the node
        
    Returns:
        ToolNode instance
    """
    try:
        return ToolNode(tools=tools)
    except Exception as e:
        app_logger.error(f"Failed to create tool node: {str(e)}")
        raise ToolException(f"Failed to create tool node: {str(e)}")
