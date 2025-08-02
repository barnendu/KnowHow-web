#!/usr/bin/env python3
"""
MCP Utilities
Helper functions for MCP operations
"""

import logging
from typing import Any, Dict, Optional
from contextlib import contextmanager

from app.mcp_jira.mcp_jira_client import JiraMCPClient

logger = logging.getLogger(__name__)

@contextmanager
def get_mcp_client():
    """Context manager for MCP client"""
    client = JiraMCPClient()
    try:
        client.connect()
        yield client
    finally:
        client.close()

def create_jira_issue_mcp(ticket_text: str) -> Dict[str, Any]:
    """Create Jira issue using MCP client with parsed ticket"""
    from app.web.tasks.parse_ticket import parse_ticket
    
    # Parse the ticket
    ticket_payload = parse_ticket(ticket_text)
    
    with get_mcp_client() as client:
        # Extract data from parsed ticket
        summary = ticket_payload["fields"]["summary"]
        description = ticket_payload["fields"]["description"]["content"][0]["content"][0]["text"]
        project = ticket_payload["fields"]["project"]["key"]
        issue_type = ticket_payload["fields"]["issuetype"]["name"]
        
        # Create the issue using MCP client
        result = client.create_issue(
            project=project,
            summary=summary,
            description=description,
            issue_type=issue_type
        )
        
        return result

def search_jira_issues_mcp(jql: str, max_results: int = 50) -> Dict[str, Any]:
    """Search Jira issues using MCP client"""
    with get_mcp_client() as client:
        result = client.search_issues(jql=jql, max_results=max_results)
        return result

def get_jira_issue_mcp(issue_key: str) -> Dict[str, Any]:
    """Get Jira issue details using MCP client"""
    with get_mcp_client() as client:
        result = client.get_issue(issue_key)
        return result

def add_jira_comment_mcp(issue_key: str, comment: str) -> Dict[str, Any]:
    """Add comment to Jira issue using MCP client"""
    with get_mcp_client() as client:
        result = client.add_comment(issue_key, comment)
        return result

def update_jira_issue_mcp(issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update Jira issue using MCP client"""
    with get_mcp_client() as client:
        result = client.update_issue(issue_key, summary=summary, description=description)
        return result

def get_jira_projects_mcp() -> Dict[str, Any]:
    """Get available Jira projects using MCP client"""
    with get_mcp_client() as client:
        result = client.get_projects()
        return result 