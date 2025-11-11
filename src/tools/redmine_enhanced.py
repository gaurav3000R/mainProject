"""Enhanced Redmine tools with metadata context."""

from typing import Optional
from langchain_core.tools import tool
from src.services.redmine_metadata import metadata_loader
from src.utils.logger import app_logger


@tool
async def get_project_info_by_name(project_name: str) -> str:
    """
    Get project information by project name using cached metadata.
    
    This is FASTER than calling the API directly. Use this when you know the project name
    and want to get its ID, description, or other details.
    
    Args:
        project_name: Full or partial project name (e.g., "Ni-kshay", "PREPLEX")
        
    Returns:
        Project information or error message
        
    Examples:
        - project_name="Ni-kshay Setu" → Returns project details
        - project_name="PREPLEX" → Returns project details
    """
    try:
        project = metadata_loader.get_project_by_name(project_name)
        
        if not project:
            # Show available projects
            available = metadata_loader.get_all_projects_summary()
            return f"Project '{project_name}' not found.\n\n{available}"
        
        result = [
            f"**{project['name']}** (ID: {project['id']})",
            f"Identifier: {project.get('identifier', 'N/A')}",
            f"Description: {project.get('description', 'No description')}",
            f"Status: {'Active' if project.get('status') == 1 else 'Closed'}",
            f"Created: {project.get('created_on', 'N/A')}",
            f"",
            f"💡 Use this project ID ({project['id']}) for other operations."
        ]
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error getting project info: {e}")
        return f"Error: {str(e)}"


@tool
async def list_all_available_resources() -> str:
    """
    List ALL available Redmine resources from cached metadata.
    
    Use this to show users what's available in their Redmine instance:
    - All projects with IDs
    - All statuses
    - All priorities  
    - All trackers
    
    This is useful when users ask "what do I have?" or "show me everything".
    
    Returns:
        Complete formatted list of all resources
    """
    try:
        parts = [
            "🎯 **YOUR REDMINE RESOURCES**",
            "="*60,
            "",
            metadata_loader.get_all_projects_summary(),
            "",
            metadata_loader.get_all_statuses_formatted(),
            "",
            metadata_loader.get_all_priorities_formatted(),
            "",
            metadata_loader.get_all_trackers_formatted()
        ]
        
        return "\n".join(parts)
    except Exception as e:
        app_logger.error(f"Error listing resources: {e}")
        return f"Error: {str(e)}"


@tool
async def search_projects_by_keyword(keyword: str) -> str:
    """
    Search for projects by keyword in name, description, or identifier.
    
    Use this when user wants to find projects matching certain keywords.
    
    Args:
        keyword: Search term (e.g., "health", "setu", "preplex")
        
    Returns:
        Matching projects or "no matches" message
    """
    try:
        matches = metadata_loader.search_projects(keyword)
        
        if not matches:
            return f"No projects found matching '{keyword}'.\n\n{metadata_loader.get_all_projects_summary()}"
        
        result = [f"Found {len(matches)} project(s) matching '{keyword}':\n"]
        for p in matches:
            result.append(f"• **{p['name']}** (ID: {p['id']})")
            result.append(f"  {p.get('description', 'No description')[:150]}...")
            result.append("")
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error searching projects: {e}")
        return f"Error: {str(e)}"


@tool
async def get_status_id_by_name(status_name: str) -> str:
    """
    Get status ID by status name from metadata.
    
    Use this before updating an issue status to get the correct ID.
    
    Args:
        status_name: Status name (e.g., "closed", "in progress", "open")
        
    Returns:
        Status ID and name
    """
    try:
        status = metadata_loader.get_status_by_name(status_name)
        
        if not status:
            available = metadata_loader.get_all_statuses_formatted()
            return f"Status '{status_name}' not found.\n\n{available}"
        
        return f"Status: **{status['name']}** → ID: {status['id']}"
    except Exception as e:
        app_logger.error(f"Error getting status ID: {e}")
        return f"Error: {str(e)}"


@tool
async def get_priority_id_by_name(priority_name: str) -> str:
    """
    Get priority ID by priority name from metadata.
    
    Use this before creating/updating an issue to get the correct priority ID.
    
    Args:
        priority_name: Priority name (e.g., "high", "urgent", "normal")
        
    Returns:
        Priority ID and name
    """
    try:
        priority = metadata_loader.get_priority_by_name(priority_name)
        
        if not priority:
            available = metadata_loader.get_all_priorities_formatted()
            return f"Priority '{priority_name}' not found.\n\n{available}"
        
        return f"Priority: **{priority['name']}** → ID: {priority['id']}"
    except Exception as e:
        app_logger.error(f"Error getting priority ID: {e}")
        return f"Error: {str(e)}"


# Export enhanced tools
enhanced_tools = [
    get_project_info_by_name,
    list_all_available_resources,
    search_projects_by_keyword,
    get_status_id_by_name,
    get_priority_id_by_name
]
