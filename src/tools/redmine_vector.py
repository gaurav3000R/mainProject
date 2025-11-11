"""Vector-based semantic search tools for Redmine."""

from typing import Optional
from langchain_core.tools import tool
from src.services.redmine_vectorstore import redmine_vectorstore
from src.utils.logger import app_logger


@tool
async def semantic_search_issues(query: str, limit: str = "5") -> str:
    """
    Perform SEMANTIC search to find issues by meaning, not just exact keywords.
    
    This tool understands concepts and finds related issues even if they use different words.
    Perfect for finding issues by description content or similar problems.
    
    Use this when you need to:
    - Find issues "similar to" something
    - Search by concept (e.g., "authentication" finds "login", "OAuth", "credentials")
    - Discover related issues
    - Find issues "about" a topic
    
    Args:
        query: Search query describing what to find (e.g., "payment gateway problems")
        limit: Maximum number of results (default: 5)
        
    Returns:
        Semantically similar issues with relevance scores
        
    Examples:
        - query="authentication problems" → Finds login, OAuth, credentials issues
        - query="payment gateway failing" → Finds transaction, checkout, payment issues
        - query="database performance" → Finds slow queries, optimization issues
        
    Note: This is SEMANTIC search, not exact match. It understands meaning!
    """
    if not redmine_vectorstore.is_available():
        return "⚠️ Semantic search not available. Vector store not initialized. Use search_redmine_issues for exact keyword search instead."
    
    try:
        limit_int = int(limit)
        results = redmine_vectorstore.semantic_search(query, k=limit_int)
        
        if not results:
            return f"No issues found semantically similar to '{query}'."
        
        output = [f"🔍 Found {len(results)} issues semantically related to '{query}':\n"]
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            score = result['score']
            relevance = "🟢 High" if score < 0.5 else "🟡 Medium" if score < 1.0 else "🔴 Low"
            
            output.append(f"\n{i}. **Issue #{metadata.get('issue_id', 'N/A')}**: {metadata.get('subject', 'N/A')}")
            output.append(f"   Project: {metadata.get('project_name', 'N/A')}")
            output.append(f"   Status: {metadata.get('status', 'N/A')} | Priority: {metadata.get('priority', 'N/A')}")
            output.append(f"   Relevance: {relevance} (score: {score:.3f})")
            
            # Show snippet of content
            content = result['content'][:200]
            output.append(f"   Preview: {content}...")
            output.append("")
        
        output.append("\n💡 These results are based on semantic similarity, not just keyword matching!")
        
        return "\n".join(output)
        
    except Exception as e:
        app_logger.error(f"Semantic search failed: {e}")
        return f"Error performing semantic search: {str(e)}"


@tool
async def find_similar_issues(issue_id: str) -> str:
    """
    Find issues that are similar to a specific issue.
    
    This uses AI to understand the issue content and find other issues
    that discuss similar topics or problems, even if they use different words.
    
    Perfect for:
    - "Show me issues similar to #123"
    - "Find related issues"
    - "What other issues are like this one?"
    
    Args:
        issue_id: The issue ID to find similar issues for (e.g., "123")
        
    Returns:
        List of similar issues ranked by similarity
        
    Examples:
        - issue_id="22812" → Finds issues with similar content
    """
    if not redmine_vectorstore.is_available():
        return "⚠️ Similar issue search not available. Vector store not initialized."
    
    try:
        issue_id_int = int(issue_id)
        results = redmine_vectorstore.search_similar_issues(issue_id_int, k=5)
        
        if not results:
            return f"No similar issues found for issue #{issue_id}. The issue might not be in the vector store yet."
        
        output = [f"🔗 Issues similar to #{issue_id}:\n"]
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            score = result['score']
            similarity = f"{(1 - score) * 100:.1f}%"
            
            output.append(f"{i}. **Issue #{metadata.get('issue_id', 'N/A')}**: {metadata.get('subject', 'N/A')}")
            output.append(f"   Project: {metadata.get('project_name', 'N/A')}")
            output.append(f"   Status: {metadata.get('status', 'N/A')}")
            output.append(f"   Similarity: {similarity}")
            output.append("")
        
        output.append(f"\n💡 Use get_redmine_issue_details to see full details of any issue above.")
        
        return "\n".join(output)
        
    except ValueError:
        return f"Error: '{issue_id}' is not a valid issue ID. Please provide a numeric issue ID."
    except Exception as e:
        app_logger.error(f"Failed to find similar issues: {e}")
        return f"Error finding similar issues: {str(e)}"


@tool
async def search_issues_by_project_semantic(project_name: str, query: str, limit: str = "5") -> str:
    """
    Semantic search for issues within a specific project.
    
    Combines project filtering with semantic search to find relevant issues
    in a particular project based on meaning, not just keywords.
    
    Args:
        project_name: Project name to search in (e.g., "Ni-kshay Setu Revamp")
        query: What to search for (e.g., "database optimization")
        limit: Maximum results (default: 5)
        
    Returns:
        Semantically similar issues from the specified project
        
    Examples:
        - project_name="PREPLEX", query="authentication" → Auth-related issues in PREPLEX
    """
    if not redmine_vectorstore.is_available():
        return "⚠️ Semantic search not available. Vector store not initialized."
    
    try:
        from src.services.redmine_metadata import metadata_loader
        
        # Get project info
        project = metadata_loader.get_project_by_name(project_name)
        if not project:
            return f"Project '{project_name}' not found. Available projects:\n{metadata_loader.get_all_projects_summary()}"
        
        project_id = project['id']
        limit_int = int(limit)
        
        # Search with project filter
        results = redmine_vectorstore.semantic_search(
            query,
            k=limit_int,
            filter_dict={"project_id": project_id}
        )
        
        if not results:
            return f"No issues found in project '{project['name']}' matching '{query}'."
        
        output = [f"🔍 Issues in **{project['name']}** related to '{query}':\n"]
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            
            output.append(f"{i}. **Issue #{metadata.get('issue_id', 'N/A')}**: {metadata.get('subject', 'N/A')}")
            output.append(f"   Status: {metadata.get('status', 'N/A')} | Priority: {metadata.get('priority', 'N/A')}")
            output.append(f"   Relevance: {(1 - result['score']) * 100:.1f}%")
            output.append("")
        
        return "\n".join(output)
        
    except Exception as e:
        app_logger.error(f"Project semantic search failed: {e}")
        return f"Error: {str(e)}"


@tool
async def get_vector_store_status() -> str:
    """
    Get the status and statistics of the vector store.
    
    Shows if semantic search is available and how many issues are indexed.
    
    Returns:
        Vector store status and statistics
    """
    stats = redmine_vectorstore.get_stats()
    
    if not stats.get('available'):
        return "❌ Vector store is not available. Semantic search is disabled."
    
    if 'error' in stats:
        return f"⚠️ Vector store available but error getting stats: {stats['error']}"
    
    output = [
        "✅ **Vector Store Status: Active**\n",
        f"Collection: {stats.get('collection_name', 'N/A')}",
        f"Documents Indexed: {stats.get('document_count', 0)}",
        f"Storage: {stats.get('persist_directory', 'N/A')}",
        "",
        "📊 **Capabilities:**",
        "  • Semantic issue search",
        "  • Find similar issues",
        "  • Project-scoped semantic search",
        "",
        "💡 Use semantic_search_issues for concept-based search!"
    ]
    
    return "\n".join(output)


# Export vector tools
vector_tools = [
    semantic_search_issues,
    find_similar_issues,
    search_issues_by_project_semantic,
    get_vector_store_status
]
