"""
Enhanced graph execution with custom LangSmith tracing.
Use this module for better trace organization and visibility.
"""

from typing import Dict, Any, Optional, List
from langchain_core.runnables import RunnableConfig
from src.agents.graphs.deployable import (
    chatbot_graph,
    chatbot_with_tools_graph,
    research_graph,
    writer_graph,
    news_graph,
    redmine_graph
)
from src.utils.langsmith import get_langsmith_url
from src.utils.logger import app_logger


class TracedGraphExecutor:
    """Execute graphs with enhanced LangSmith tracing."""
    
    GRAPHS = {
        "chatbot": chatbot_graph,
        "chatbot_with_tools": chatbot_with_tools_graph,
        "research": research_graph,
        "writer": writer_graph,
        "news": news_graph,
        "redmine": redmine_graph,
    }
    
    @classmethod
    def execute(
        cls,
        graph_name: str,
        state: Dict[str, Any],
        run_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a graph with custom tracing configuration.
        
        Args:
            graph_name: Name of graph to execute
            state: Initial state for graph
            run_name: Custom name for trace (default: graph_name)
            tags: Tags for filtering traces
            metadata: Additional metadata for trace
            
        Returns:
            Graph execution result
            
        Example:
            >>> result = TracedGraphExecutor.execute(
            ...     "chatbot",
            ...     {"messages": [HumanMessage(content="Hello")]},
            ...     run_name="user_123_chat",
            ...     tags=["production", "user_chat"],
            ...     metadata={"user_id": "123", "session": "abc"}
            ... )
        """
        if graph_name not in cls.GRAPHS:
            raise ValueError(f"Unknown graph: {graph_name}. Available: {list(cls.GRAPHS.keys())}")
        
        # Build graph
        graph_fn = cls.GRAPHS[graph_name]
        graph = graph_fn()
        
        # Configure tracing
        config = RunnableConfig(
            run_name=run_name or f"{graph_name}_execution",
            tags=tags or [graph_name, "traced_execution"],
            metadata=metadata or {}
        )
        
        # Log execution
        app_logger.info(f"Executing {graph_name} with trace: {config.get('run_name')}")
        app_logger.info(f"View at: {get_langsmith_url()}")
        
        # Execute
        result = graph.invoke(state, config=config)
        
        app_logger.info(f"Execution complete. Check LangSmith dashboard.")
        
        return result
    
    @classmethod
    async def aexecute(
        cls,
        graph_name: str,
        state: Dict[str, Any],
        run_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Async version of execute."""
        if graph_name not in cls.GRAPHS:
            raise ValueError(f"Unknown graph: {graph_name}")
        
        graph_fn = cls.GRAPHS[graph_name]
        graph = graph_fn()
        
        config = RunnableConfig(
            run_name=run_name or f"{graph_name}_async",
            tags=tags or [graph_name, "async_execution"],
            metadata=metadata or {}
        )
        
        app_logger.info(f"Async executing {graph_name} with trace: {config.get('run_name')}")
        
        result = await graph.ainvoke(state, config=config)
        
        app_logger.info(f"Async execution complete.")
        
        return result


# Convenience functions
def execute_chatbot(message: str, run_name: Optional[str] = None, **kwargs):
    """Execute chatbot with tracing."""
    from langchain_core.messages import HumanMessage
    return TracedGraphExecutor.execute(
        "chatbot",
        {"messages": [HumanMessage(content=message)]},
        run_name=run_name or f"chat_{message[:20]}",
        **kwargs
    )


def execute_research(query: str, run_name: Optional[str] = None, **kwargs):
    """Execute research with tracing."""
    return TracedGraphExecutor.execute(
        "research",
        {
            "query": query,
            "search_results": [],
            "sources": [],
            "summary": ""
        },
        run_name=run_name or f"research_{query[:20]}",
        **kwargs
    )


def execute_writer(topic: str, content_type: str = "article", run_name: Optional[str] = None, **kwargs):
    """Execute writer with tracing."""
    return TracedGraphExecutor.execute(
        "writer",
        {
            "topic": topic,
            "content_type": content_type,
            "outline": "",
            "draft": "",
            "final_content": ""
        },
        run_name=run_name or f"write_{topic[:20]}",
        **kwargs
    )


if __name__ == "__main__":
    # Example usage
    print("Traced Graph Executor - Examples")
    print("="*60)
    
    # Example 1: Simple chatbot
    print("\n1. Chatbot with custom trace name:")
    result = execute_chatbot(
        "Hello, this is a traced execution!",
        run_name="example_chat_001",
        tags=["example", "demo"],
        metadata={"version": "1.0", "env": "test"}
    )
    print(f"✓ Completed. Check: {get_langsmith_url()}")
    
    print("\n" + "="*60)
    print("Check your LangSmith dashboard to see the traces!")
    print("="*60)
