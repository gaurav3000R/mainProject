"""News summarization workflow graph."""

from langgraph.graph import StateGraph, END
from src.agents.states.news import NewsSummaryState
from src.agents.nodes.news import fetch_news_node, summarize_news_node, save_result_node
from src.llms.base import BaseLLM
from src.utils.logger import app_logger


class NewsSummarizationGraph:
    """
    LangGraph workflow: Start → Fetch News → Summarize → Save → End
    """
    
    def __init__(self, llm: BaseLLM):
        """
        Initialize news summarization graph.
        
        Args:
            llm: Language model for summarization
        """
        self.llm = llm
        self.graph = self._build_graph()
        app_logger.info("Initialized NewsSummarizationGraph")
    
    def _build_graph(self) -> StateGraph:
        """
        Build the workflow graph.
        
        Flow: Start → Fetch News → Summarize → Save → End
        
        Returns:
            Compiled StateGraph
        """
        # Create graph
        workflow = StateGraph(NewsSummaryState)
        
        # Add nodes
        workflow.add_node("fetch_news", fetch_news_node)
        workflow.add_node(
            "summarize",
            lambda state: summarize_news_node(state, self.llm)
        )
        workflow.add_node("save_result", save_result_node)
        
        # Define edges (workflow flow)
        workflow.set_entry_point("fetch_news")
        workflow.add_edge("fetch_news", "summarize")
        workflow.add_edge("summarize", "save_result")
        workflow.add_edge("save_result", END)
        
        app_logger.info("Built news summarization workflow graph")
        
        return workflow.compile()
    
    def run(
        self,
        query: str,
        max_results: int = 5
    ) -> NewsSummaryState:
        """
        Run the news summarization workflow.
        
        Args:
            query: Search query for news
            max_results: Maximum number of articles to fetch
            
        Returns:
            Final workflow state with summary
        """
        app_logger.info(f"Running news summarization for query: {query}")
        
        # Initial state
        initial_state: NewsSummaryState = {
            "query": query,
            "max_results": max_results,
            "news_articles": [],
            "summary": "",
            "saved_path": None,
            "error": None,
            "status": "started"
        }
        
        # Run workflow
        result = self.graph.invoke(initial_state)
        
        app_logger.info(f"News summarization completed. Status: {result.get('status')}")
        
        return result
    
    async def arun(
        self,
        query: str,
        max_results: int = 5
    ) -> NewsSummaryState:
        """
        Async run the news summarization workflow.
        
        Args:
            query: Search query for news
            max_results: Maximum number of articles to fetch
            
        Returns:
            Final workflow state with summary
        """
        app_logger.info(f"Running async news summarization for query: {query}")
        
        # Initial state
        initial_state: NewsSummaryState = {
            "query": query,
            "max_results": max_results,
            "news_articles": [],
            "summary": "",
            "saved_path": None,
            "error": None,
            "status": "started"
        }
        
        # Run workflow asynchronously
        result = await self.graph.ainvoke(initial_state)
        
        app_logger.info(f"Async news summarization completed. Status: {result.get('status')}")
        
        return result
