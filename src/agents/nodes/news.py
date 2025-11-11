"""Nodes for news summarization workflow."""

import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from src.llms.base import BaseLLM
from src.tools.base import get_web_search_tool
from src.agents.states.news import NewsSummaryState
from src.utils.logger import app_logger


def fetch_news_node(state: NewsSummaryState) -> NewsSummaryState:
    """
    Fetch news articles using web search.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with news articles
    """
    try:
        app_logger.info(f"Fetching news for query: {state['query']}")
        
        query = state["query"]
        max_results = state.get("max_results", 5)
        
        # Get web search tool
        web_search = get_web_search_tool(max_results=max_results)
        
        # Use web search tool to fetch news
        search_results = web_search.invoke({"query": query})
        
        # Parse results
        articles = []
        if isinstance(search_results, str):
            # Extract articles from search results
            articles = [{
                "title": f"Article {i+1}",
                "content": search_results[:500],  # First 500 chars
                "source": "web_search"
            }]
        elif isinstance(search_results, list):
            for i, result in enumerate(search_results[:max_results]):
                articles.append({
                    "title": result.get("title", f"Article {i+1}"),
                    "content": result.get("content", result.get("snippet", "")),
                    "url": result.get("url", ""),
                    "source": result.get("source", "web")
                })
        
        app_logger.info(f"Fetched {len(articles)} news articles")
        
        return {
            **state,
            "news_articles": articles,
            "status": "fetched"
        }
        
    except Exception as e:
        app_logger.error(f"Error fetching news: {str(e)}")
        return {
            **state,
            "news_articles": [],
            "error": f"Failed to fetch news: {str(e)}",
            "status": "error"
        }


def summarize_news_node(state: NewsSummaryState, llm: BaseLLM) -> NewsSummaryState:
    """
    Summarize news articles using LLM.
    
    Args:
        state: Current workflow state
        llm: Language model for summarization
        
    Returns:
        Updated state with summary
    """
    try:
        app_logger.info("Summarizing news articles")
        
        articles = state.get("news_articles", [])
        
        if not articles:
            return {
                **state,
                "summary": "No articles found to summarize.",
                "status": "completed"
            }
        
        # Prepare articles text
        articles_text = "\n\n".join([
            f"**{article.get('title', 'Untitled')}**\n{article.get('content', '')[:500]}"
            for article in articles
        ])
        
        # Create prompt for summarization
        prompt = f"""You are a news summarizer. Analyze the following news articles and provide a concise, informative summary.

News Articles:
{articles_text}

Instructions:
1. Provide a comprehensive summary (200-300 words)
2. Highlight key facts and events
3. Maintain objectivity
4. Structure: Overview, Key Points, Conclusion

Summary:"""
        
        # Get summary from LLM
        messages = [{"role": "user", "content": prompt}]
        response = llm.invoke(messages)
        
        summary = response.content if hasattr(response, 'content') else str(response)
        
        app_logger.info("News summarization completed")
        
        return {
            **state,
            "summary": summary,
            "status": "summarized"
        }
        
    except Exception as e:
        app_logger.error(f"Error summarizing news: {str(e)}")
        return {
            **state,
            "summary": "",
            "error": f"Failed to summarize: {str(e)}",
            "status": "error"
        }


def save_result_node(state: NewsSummaryState) -> NewsSummaryState:
    """
    Save news summary to file.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with saved path
    """
    try:
        app_logger.info("Saving news summary")
        
        # Create data directory if not exists
        data_dir = Path("data/news_summaries")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_slug = state["query"].replace(" ", "_")[:30]
        filename = f"{timestamp}_{query_slug}.json"
        filepath = data_dir / filename
        
        # Prepare data to save
        data = {
            "query": state["query"],
            "timestamp": timestamp,
            "articles_count": len(state.get("news_articles", [])),
            "articles": state.get("news_articles", []),
            "summary": state.get("summary", ""),
            "status": "completed"
        }
        
        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        app_logger.info(f"Saved summary to {filepath}")
        
        return {
            **state,
            "saved_path": str(filepath),
            "status": "completed"
        }
        
    except Exception as e:
        app_logger.error(f"Error saving result: {str(e)}")
        return {
            **state,
            "saved_path": None,
            "error": f"Failed to save: {str(e)}",
            "status": "error"
        }
