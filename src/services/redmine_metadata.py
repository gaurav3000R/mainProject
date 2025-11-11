"""
Redmine Metadata Loader and Enhancer for Adaptive RAG.

Loads metadata from redmine_metadata.json to provide context-aware responses.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.utils.logger import app_logger


class RedmineMetadataLoader:
    """Load and query Redmine metadata for enhanced RAG responses."""
    
    def __init__(self, metadata_file: str = "redminDocs/redmine_metadata.json"):
        """
        Initialize metadata loader.
        
        Args:
            metadata_file: Path to metadata JSON file
        """
        self.metadata_file = Path(metadata_file)
        self.metadata: Dict[str, Any] = {}
        self.projects: List[Dict] = []
        self.statuses: List[Dict] = []
        self.priorities: List[Dict] = []
        self.trackers: List[Dict] = []
        self.load_metadata()
    
    def load_metadata(self):
        """Load metadata from JSON file."""
        try:
            if not self.metadata_file.exists():
                app_logger.warning(f"Metadata file not found: {self.metadata_file}")
                return
            
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
            
            # Extract commonly used data
            self.projects = self.metadata.get('endpoints', {}).get('getProjects', {}).get('data', [])
            self.statuses = self.metadata.get('endpoints', {}).get('getIssueStatuses', {}).get('data', [])
            self.priorities = self.metadata.get('endpoints', {}).get('getPriorities', {}).get('data', [])
            self.trackers = self.metadata.get('endpoints', {}).get('getTrackers', {}).get('data', [])
            
            app_logger.info(f"Loaded metadata: {len(self.projects)} projects, "
                          f"{len(self.statuses)} statuses, {len(self.priorities)} priorities")
        except Exception as e:
            app_logger.error(f"Failed to load metadata: {e}")
    
    def get_project_by_name(self, name: str) -> Optional[Dict]:
        """
        Find project by name (case-insensitive, partial match).
        
        Args:
            name: Project name to search
            
        Returns:
            Project dict or None
        """
        name_lower = name.lower()
        for project in self.projects:
            if name_lower in project.get('name', '').lower():
                return project
        return None
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dict or None
        """
        for project in self.projects:
            if project.get('id') == project_id:
                return project
        return None
    
    def get_all_projects_summary(self) -> str:
        """
        Get formatted summary of all projects.
        
        Returns:
            Formatted string with project info
        """
        if not self.projects:
            return "No projects available."
        
        lines = [f"Available Projects ({len(self.projects)}):\n"]
        for p in self.projects:
            lines.append(f"• **{p['name']}** (ID: {p['id']})")
            lines.append(f"  Identifier: {p.get('identifier', 'N/A')}")
            desc = p.get('description', 'No description')[:100]
            lines.append(f"  Description: {desc}...")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_status_by_name(self, name: str) -> Optional[Dict]:
        """Find status by name."""
        name_lower = name.lower()
        for status in self.statuses:
            if name_lower in status.get('name', '').lower():
                return status
        return None
    
    def get_priority_by_name(self, name: str) -> Optional[Dict]:
        """Find priority by name."""
        name_lower = name.lower()
        for priority in self.priorities:
            if name_lower in priority.get('name', '').lower():
                return priority
        return None
    
    def get_tracker_by_name(self, name: str) -> Optional[Dict]:
        """Find tracker by name."""
        name_lower = name.lower()
        for tracker in self.trackers:
            if name_lower in tracker.get('name', '').lower():
                return tracker
        return None
    
    def get_all_statuses_formatted(self) -> str:
        """Get formatted list of all statuses."""
        if not self.statuses:
            return "No statuses available."
        
        lines = ["Available Issue Statuses:"]
        for s in self.statuses:
            lines.append(f"• {s['name']} (ID: {s['id']})")
        
        return "\n".join(lines)
    
    def get_all_priorities_formatted(self) -> str:
        """Get formatted list of all priorities."""
        if not self.priorities:
            return "No priorities available."
        
        lines = ["Available Priorities:"]
        for p in self.priorities:
            lines.append(f"• {p['name']} (ID: {p['id']})")
        
        return "\n".join(lines)
    
    def get_all_trackers_formatted(self) -> str:
        """Get formatted list of all trackers."""
        if not self.trackers:
            return "No trackers available."
        
        lines = ["Available Trackers:"]
        for t in self.trackers:
            lines.append(f"• {t['name']} (ID: {t['id']})")
        
        return "\n".join(lines)
    
    def get_metadata_summary(self) -> str:
        """Get complete metadata summary for context."""
        parts = [
            f"Redmine Instance: {self.metadata.get('base_url', 'N/A')}",
            f"Last Updated: {self.metadata.get('fetched_at', 'N/A')}",
            "",
            "Available Resources:",
            f"• Projects: {len(self.projects)}",
            f"• Statuses: {len(self.statuses)}",
            f"• Priorities: {len(self.priorities)}",
            f"• Trackers: {len(self.trackers)}",
            "",
            self.get_all_statuses_formatted(),
            "",
            self.get_all_priorities_formatted(),
            "",
            self.get_all_trackers_formatted()
        ]
        
        return "\n".join(parts)
    
    def search_projects(self, query: str) -> List[Dict]:
        """
        Search projects by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching projects
        """
        query_lower = query.lower()
        matches = []
        
        for project in self.projects:
            if (query_lower in project.get('name', '').lower() or
                query_lower in project.get('description', '').lower() or
                query_lower in project.get('identifier', '').lower()):
                matches.append(project)
        
        return matches
    
    def get_context_for_query(self, query: str) -> str:
        """
        Get relevant context from metadata based on query.
        
        Args:
            query: User query
            
        Returns:
            Relevant context string
        """
        query_lower = query.lower()
        context_parts = []
        
        # Check if asking about projects
        if any(word in query_lower for word in ['project', 'projects']):
            context_parts.append(self.get_all_projects_summary())
        
        # Check if asking about statuses
        if any(word in query_lower for word in ['status', 'statuses']):
            context_parts.append(self.get_all_statuses_formatted())
        
        # Check if asking about priorities
        if any(word in query_lower for word in ['priority', 'priorities']):
            context_parts.append(self.get_all_priorities_formatted())
        
        # Check if asking about trackers
        if any(word in query_lower for word in ['tracker', 'trackers']):
            context_parts.append(self.get_all_trackers_formatted())
        
        # Search for specific project mentions
        for project in self.projects:
            if project['name'].lower() in query_lower:
                context_parts.append(f"Project Context: {project['name']} (ID: {project['id']})")
                break
        
        return "\n\n".join(context_parts) if context_parts else ""


# Global metadata loader instance
metadata_loader = RedmineMetadataLoader()
