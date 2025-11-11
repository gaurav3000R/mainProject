"""Redmine API client and tools."""

import httpx
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class RedmineConfig(BaseSettings):
    """Redmine configuration."""
    
    redmin_api_base_url: str = Field(default="", description="Redmine base URL")
    redmin_api_key: str = Field(default="", description="Redmine API key")
    
    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"


class RedmineAPIClient:
    """Client for Redmine REST API."""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize Redmine API client.
        
        Args:
            base_url: Redmine base URL
            api_key: Redmine API key
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-Redmine-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Redmine API."""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            return response.json()
    
    async def validate_connection(self) -> Dict[str, Any]:
        """Validate API credentials."""
        return await self._request("GET", "/users/current.json")
    
    async def get_projects(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch all projects."""
        result = await self._request("GET", "/projects.json", params={"limit": limit})
        return result.get("projects", [])
    
    async def get_issues(
        self,
        project_id: Optional[int] = None,
        status_id: Optional[str] = None,
        assigned_to_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch issues with optional filters.
        
        Args:
            project_id: Filter by project ID
            status_id: Filter by status (e.g., 'open', 'closed', '*' for all)
            assigned_to_id: Filter by assigned user ID
            limit: Maximum number of results
        """
        params = {"limit": limit}
        if project_id:
            params["project_id"] = project_id
        if status_id:
            params["status_id"] = status_id
        if assigned_to_id:
            params["assigned_to_id"] = assigned_to_id
        
        result = await self._request("GET", "/issues.json", params=params)
        return result.get("issues", [])
    
    async def get_issue(self, issue_id: int) -> Dict[str, Any]:
        """Get single issue by ID."""
        result = await self._request("GET", f"/issues/{issue_id}.json")
        return result.get("issue", {})
    
    async def create_issue(
        self,
        project_id: int,
        subject: str,
        description: str = "",
        tracker_id: int = 1,
        priority_id: int = 2
    ) -> Dict[str, Any]:
        """
        Create a new issue.
        
        Args:
            project_id: Project ID
            subject: Issue subject/title
            description: Issue description
            tracker_id: Tracker ID (default: 1)
            priority_id: Priority ID (default: 2 - Normal)
        """
        data = {
            "issue": {
                "project_id": project_id,
                "subject": subject,
                "description": description,
                "tracker_id": tracker_id,
                "priority_id": priority_id
            }
        }
        return await self._request("POST", "/issues.json", json_data=data)
    
    async def update_issue(
        self,
        issue_id: int,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        status_id: Optional[int] = None,
        priority_id: Optional[int] = None
    ) -> None:
        """Update an existing issue."""
        data = {"issue": {}}
        if subject:
            data["issue"]["subject"] = subject
        if description:
            data["issue"]["description"] = description
        if status_id:
            data["issue"]["status_id"] = status_id
        if priority_id:
            data["issue"]["priority_id"] = priority_id
        
        await self._request("PUT", f"/issues/{issue_id}.json", json_data=data)
    
    async def get_time_entries(
        self,
        project_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch time entries."""
        params = {"limit": limit}
        if project_id:
            params["project_id"] = project_id
        
        result = await self._request("GET", "/time_entries.json", params=params)
        return result.get("time_entries", [])
    
    async def get_issue_statuses(self) -> List[Dict[str, Any]]:
        """Fetch available issue statuses."""
        result = await self._request("GET", "/issue_statuses.json")
        return result.get("issue_statuses", [])
    
    async def get_priorities(self) -> List[Dict[str, Any]]:
        """Fetch issue priority levels."""
        result = await self._request("GET", "/enumerations/issue_priorities.json")
        return result.get("issue_priorities", [])
    
    async def get_trackers(self) -> List[Dict[str, Any]]:
        """Fetch available trackers."""
        result = await self._request("GET", "/trackers.json")
        return result.get("trackers", [])
    
    async def get_users(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch users."""
        result = await self._request("GET", "/users.json", params={"limit": limit})
        return result.get("users", [])


# Global client instance
_redmine_config = RedmineConfig()
redmine_client = RedmineAPIClient(
    base_url=_redmine_config.redmin_api_base_url,
    api_key=_redmine_config.redmin_api_key
) if _redmine_config.redmin_api_base_url and _redmine_config.redmin_api_key else None
