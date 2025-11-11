"""LangChain tools for Redmine API interaction."""

from typing import Optional, Dict, Any
from langchain_core.tools import tool
from src.services.redmine_client import redmine_client
from src.utils.logger import app_logger


@tool
async def get_redmine_projects(limit: str = "20") -> str:
    """
    Get list of all projects from Redmine.
    
    Use this tool to:
    - See all available projects
    - Find a project by name
    - Get project IDs for other operations
    
    Args:
        limit: Maximum number of projects to return (default: 20)
        
    Returns:
        Formatted string with project information including IDs, names, and descriptions
        
    Example output:
        Found 5 projects:
        - **Project Name** (ID: 123)
          Identifier: project-slug
          Description: Project description...
    """
    try:
        # Convert string to int
        limit_int = int(limit)
        projects = await redmine_client.get_projects(limit=limit_int)
        
        if not projects:
            return "No projects found."
        
        result = [f"Found {len(projects)} projects:\n"]
        for p in projects:
            result.append(
                f"- **{p['name']}** (ID: {p['id']})\n"
                f"  Identifier: {p.get('identifier', 'N/A')}\n"
                f"  Description: {p.get('description', 'No description')[:100]}\n"
            )
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error fetching projects: {e}")
        return f"Error fetching projects: {str(e)}"


@tool
async def get_redmine_issues(
    project_id: str = "null",
    status: str = "open",
    limit: str = "20"
) -> str:
    """
    Get list of issues from Redmine.
    
    Args:
        project_id: Optional project ID to filter by (use "null" for all projects)
        status: Status filter ('open', 'closed', '*' for all). Default: 'open'
        limit: Maximum number of issues to return (default: 20)
        
    Returns:
        Formatted string with issue information
    """
    try:
        # Convert parameters
        proj_id = None if project_id == "null" or not project_id else int(project_id)
        limit_int = int(limit)
        
        issues = await redmine_client.get_issues(
            project_id=proj_id,
            status_id=status,
            limit=limit_int
        )
        
        if not issues:
            return f"No {status} issues found."
        
        result = [f"Found {len(issues)} issues:\n"]
        for issue in issues:
            result.append(
                f"- **#{issue['id']}: {issue['subject']}**\n"
                f"  Project: {issue.get('project', {}).get('name', 'N/A')}\n"
                f"  Status: {issue.get('status', {}).get('name', 'N/A')}\n"
                f"  Priority: {issue.get('priority', {}).get('name', 'N/A')}\n"
                f"  Assigned: {issue.get('assigned_to', {}).get('name', 'Unassigned')}\n"
                f"  Created: {issue.get('created_on', 'N/A')}\n"
            )
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error fetching issues: {e}")
        return f"Error fetching issues: {str(e)}"


@tool
async def get_redmine_issue_details(issue_id: str) -> str:
    """
    Get detailed information about a specific issue by its numeric ID.
    
    IMPORTANT: This tool requires a numeric issue ID (e.g., "123", "456").
    If you only have an issue title or name, use search_redmine_issues instead.
    
    Args:
        issue_id: The numeric issue ID (e.g., "123", not a title or name)
        
    Returns:
        Formatted string with detailed issue information
        
    Examples:
        - Good: issue_id="123"
        - Good: issue_id="456"
        - Bad: issue_id="Fix login bug" (use search_redmine_issues instead)
        - Bad: issue_id="Project Name" (use get_redmine_projects instead)
    """
    try:
        # Validate that issue_id is numeric
        if not issue_id.replace("-", "").isdigit():
            return f"Error: '{issue_id}' is not a valid issue ID. Issue IDs must be numbers. If you're looking for an issue by name, use search_redmine_issues tool instead."
        
        issue_id_int = int(issue_id)
        issue = await redmine_client.get_issue(issue_id_int)
        
        if not issue:
            return f"Issue #{issue_id} not found."
        
        result = [
            f"**Issue #{issue['id']}: {issue['subject']}**\n",
            f"Project: {issue.get('project', {}).get('name', 'N/A')}",
            f"Tracker: {issue.get('tracker', {}).get('name', 'N/A')}",
            f"Status: {issue.get('status', {}).get('name', 'N/A')}",
            f"Priority: {issue.get('priority', {}).get('name', 'N/A')}",
            f"Assigned: {issue.get('assigned_to', {}).get('name', 'Unassigned')}",
            f"Author: {issue.get('author', {}).get('name', 'N/A')}",
            f"Created: {issue.get('created_on', 'N/A')}",
            f"Updated: {issue.get('updated_on', 'N/A')}",
            f"\n**Description:**\n{issue.get('description', 'No description')}"
        ]
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error fetching issue details: {e}")
        return f"Error fetching issue #{issue_id}: {str(e)}"


@tool
async def create_redmine_issue(
    project_id: str,
    subject: str,
    description: str = "",
    priority: str = "normal"
) -> str:
    """
    Create a new issue in Redmine.
    
    Args:
        project_id: The project ID to create the issue in
        subject: Issue title/subject
        description: Detailed description of the issue
        priority: Priority level ('low', 'normal', 'high', 'urgent', 'immediate')
        
    Returns:
        Success message with created issue ID
    """
    try:
        project_id_int = int(project_id)
        
        # Map priority names to IDs (standard Redmine)
        priority_map = {
            "low": 1,
            "normal": 2,
            "high": 3,
            "urgent": 4,
            "immediate": 5
        }
        priority_id = priority_map.get(priority.lower(), 2)
        
        result = await redmine_client.create_issue(
            project_id=project_id_int,
            subject=subject,
            description=description,
            priority_id=priority_id
        )
        
        issue = result.get("issue", {})
        issue_id = issue.get("id")
        
        return f"✅ Successfully created issue #{issue_id}: {subject}"
    except Exception as e:
        app_logger.error(f"Error creating issue: {e}")
        return f"Error creating issue: {str(e)}"


@tool
async def update_redmine_issue(
    issue_id: str,
    subject: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    Update an existing Redmine issue.
    
    Args:
        issue_id: The issue ID to update
        subject: New subject/title (optional)
        description: New description (optional)
        status: New status (optional)
        
    Returns:
        Success message
    """
    try:
        issue_id_int = int(issue_id)
        
        # Note: Status IDs are installation-specific
        # You may need to fetch statuses first
        status_id = None
        if status:
            statuses = await redmine_client.get_issue_statuses()
            for s in statuses:
                if s['name'].lower() == status.lower():
                    status_id = s['id']
                    break
        
        await redmine_client.update_issue(
            issue_id=issue_id_int,
            subject=subject,
            description=description,
            status_id=status_id
        )
        
        return f"✅ Successfully updated issue #{issue_id}"
    except Exception as e:
        app_logger.error(f"Error updating issue: {e}")
        return f"Error updating issue #{issue_id}: {str(e)}"


@tool
async def get_redmine_time_entries(project_id: str = "null", limit: str = "20") -> str:
    """
    Get time entries from Redmine.
    
    Args:
        project_id: Optional project ID to filter by (use "null" for all)
        limit: Maximum number of entries to return (default: 20)
        
    Returns:
        Formatted string with time entry information
    """
    try:
        proj_id = None if project_id == "null" or not project_id else int(project_id)
        limit_int = int(limit)
        
        entries = await redmine_client.get_time_entries(project_id=proj_id, limit=limit_int)
        
        if not entries:
            return "No time entries found."
        
        result = [f"Found {len(entries)} time entries:\n"]
        total_hours = 0
        
        for entry in entries:
            hours = entry.get('hours', 0)
            total_hours += hours
            result.append(
                f"- {entry.get('spent_on', 'N/A')}: {hours}h\n"
                f"  User: {entry.get('user', {}).get('name', 'N/A')}\n"
                f"  Activity: {entry.get('activity', {}).get('name', 'N/A')}\n"
                f"  Comments: {entry.get('comments', 'No comments')}\n"
            )
        
        result.append(f"\n**Total Hours: {total_hours}h**")
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error fetching time entries: {e}")
        return f"Error fetching time entries: {str(e)}"


@tool
async def get_redmine_metadata() -> str:
    """
    Get Redmine metadata including statuses, priorities, and trackers.
    
    Returns:
        Formatted string with metadata information
    """
    try:
        statuses = await redmine_client.get_issue_statuses()
        priorities = await redmine_client.get_priorities()
        trackers = await redmine_client.get_trackers()
        
        result = [
            "**Issue Statuses:**",
            ", ".join([f"{s['name']} (ID: {s['id']})" for s in statuses]),
            "\n**Priorities:**",
            ", ".join([f"{p['name']} (ID: {p['id']})" for p in priorities]),
            "\n**Trackers:**",
            ", ".join([f"{t['name']} (ID: {t['id']})" for t in trackers])
        ]
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error fetching metadata: {e}")
        return f"Error fetching metadata: {str(e)}"


@tool
async def search_redmine_issues(query: str, limit: str = "10") -> str:
    """
    Search for issues by keywords in their subject or description.
    
    Use this tool when you need to find issues by:
    - Name or title (e.g., "login bug", "payment issue")
    - Keywords in description (e.g., "authentication", "timeout")
    - Project name (e.g., "Ni-kshay Setu Revamp")
    - Any text content
    
    This is useful when you don't have a numeric issue ID.
    
    Args:
        query: Search keywords (can be issue name, project name, or any text)
        limit: Maximum number of results (default: 10)
        
    Returns:
        Formatted string with matching issues
        
    Examples:
        - query="Ni-kshay Setu Revamp" → Finds issues in that project
        - query="login bug" → Finds issues mentioning login
        - query="payment" → Finds all payment-related issues
    """
    try:
        limit_int = int(limit)
        
        # Get all open issues and filter by query
        issues = await redmine_client.get_issues(status_id="*", limit=100)
        
        # Simple text search
        matching_issues = [
            issue for issue in issues
            if query.lower() in issue['subject'].lower() or
               query.lower() in issue.get('description', '').lower() or
               query.lower() in issue.get('project', {}).get('name', '').lower()
        ][:limit_int]
        
        if not matching_issues:
            return f"No issues found matching '{query}'."
        
        result = [f"Found {len(matching_issues)} issues matching '{query}':\n"]
        for issue in matching_issues:
            result.append(
                f"- **#{issue['id']}: {issue['subject']}**\n"
                f"  Status: {issue.get('status', {}).get('name', 'N/A')}\n"
                f"  Project: {issue.get('project', {}).get('name', 'N/A')}\n"
            )
        
        return "\n".join(result)
    except Exception as e:
        app_logger.error(f"Error searching issues: {e}")
        return f"Error searching issues: {str(e)}"


# List of all available Redmine tools
redmine_tools = [
    get_redmine_projects,
    get_redmine_issues,
    get_redmine_issue_details,
    create_redmine_issue,
    update_redmine_issue,
    get_redmine_time_entries,
    get_redmine_metadata,
    search_redmine_issues
]
