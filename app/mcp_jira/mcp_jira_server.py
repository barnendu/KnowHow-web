#!/usr/bin/env python3
"""
MCP Jira Server Implementation
Custom MCP server for Jira integration without external MCP dependencies
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from jira import JIRA

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPRequest:
    """MCP request structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str = ""
    params: Optional[Dict[str, Any]] = None

@dataclass
class MCPResponse:
    """MCP response structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

@dataclass
class JiraConfig:
    """Jira configuration"""
    url: str
    username: str
    api_token: str

class JiraMCPServer:
    """Custom MCP Server for Jira integration"""
    
    def __init__(self):
        self.jira_client: Optional[JIRA] = None
        self.config: Optional[JiraConfig] = None
        self.request_id = 0
        
    def initialize(self):
        """Initialize the server"""
        logger.info("Initializing Jira MCP Server")
        
        # Get Jira configuration from environment
        jira_url = os.getenv("JIRA_URL")
        email = os.getenv("EMAIL")
        api_token = os.getenv("ATLASSIAN_API_TOKEN")
        
        if not all([jira_url, email, api_token]):
            logger.error("Missing Jira configuration environment variables")
            return False
        
        self.config = JiraConfig(
            url=jira_url,
            username=email,
            api_token=api_token
        )
        
        # Initialize Jira client
        try:
            self.jira_client = JIRA(
                server=self.config.url,
                basic_auth=(self.config.username, self.config.api_token)
            )
            logger.info("Jira client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Jira client: {e}")
            return False
    
    def handle_request(self, request_data: Dict) -> Dict:
        """Handle incoming MCP request"""
        try:
            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")
            
            if method == "tools/list":
                return self._list_tools_response(request_id)
            elif method == "tools/call":
                return self._call_tool_response(request_id, params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": "Method not found"}
                }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_data.get("id"),
                "error": {"code": -1, "message": str(e)}
            }
    
    def _list_tools_response(self, request_id: str) -> Dict:
        """Return list of available tools"""
        tools = [
            {
                "name": "create_issue",
                "description": "Create a new Jira issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project": {"type": "string", "description": "Project key"},
                        "summary": {"type": "string", "description": "Issue summary"},
                        "description": {"type": "string", "description": "Issue description"},
                        "issue_type": {"type": "string", "description": "Issue type (Bug, Task, etc.)"}
                    },
                    "required": ["project", "summary", "issue_type"]
                }
            },
            {
                "name": "get_issue",
                "description": "Get issue details by key",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "issue_key": {"type": "string", "description": "Issue key (e.g., PROJ-123)"}
                    },
                    "required": ["issue_key"]
                }
            },
            {
                "name": "search_issues",
                "description": "Search for issues using JQL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "jql": {"type": "string", "description": "JQL query string"},
                        "max_results": {"type": "integer", "description": "Maximum results to return", "default": 50}
                    },
                    "required": ["jql"]
                }
            },
            {
                "name": "add_comment",
                "description": "Add comment to an issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "issue_key": {"type": "string", "description": "Issue key"},
                        "comment": {"type": "string", "description": "Comment text"}
                    },
                    "required": ["issue_key", "comment"]
                }
            },
            {
                "name": "update_issue",
                "description": "Update an existing issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "issue_key": {"type": "string", "description": "Issue key"},
                        "summary": {"type": "string", "description": "New summary"},
                        "description": {"type": "string", "description": "New description"}
                    },
                    "required": ["issue_key"]
                }
            },
            {
                "name": "get_projects",
                "description": "Get list of available projects",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
    
    def _call_tool_response(self, request_id: str, params: Dict) -> Dict:
        """Execute tool and return response"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not self.jira_client:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -1, "message": "Jira client not initialized"}
            }
        
        try:
            if tool_name == "create_issue":
                result = self._create_issue(arguments)
            elif tool_name == "get_issue":
                result = self._get_issue(arguments)
            elif tool_name == "search_issues":
                result = self._search_issues(arguments)
            elif tool_name == "add_comment":
                result = self._add_comment(arguments)
            elif tool_name == "update_issue":
                result = self._update_issue(arguments)
            elif tool_name == "get_projects":
                result = self._get_projects(arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -1, "message": f"Unknown tool: {tool_name}"}
                }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            }
            
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -1, "message": str(e)}
            }
    
    def _create_issue(self, args: Dict) -> Dict:
        """Create a new Jira issue"""
        issue_dict = {
            'project': {'key': args['project']},
            'summary': args['summary'],
            'description': args.get('description', ''),
            'issuetype': {'name': args['issue_type']}
        }
        
        issue = self.jira_client.create_issue(fields=issue_dict)
        return {
            "key": issue.key,
            "id": issue.id,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "url": f"{self.config.url}/browse/{issue.key}"
        }
    
    def _get_issue(self, args: Dict) -> Dict:
        """Get issue details"""
        issue = self.jira_client.issue(args['issue_key'])
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description or "",
            "status": issue.fields.status.name,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
            "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
            "created": str(issue.fields.created),
            "updated": str(issue.fields.updated)
        }
    
    def _search_issues(self, args: Dict) -> List[Dict]:
        """Search for issues using JQL"""
        max_results = args.get('max_results', 50)
        issues = self.jira_client.search_issues(args['jql'], maxResults=max_results)
        
        return [
            {
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None
            }
            for issue in issues
        ]
    
    def _add_comment(self, args: Dict) -> Dict:
        """Add comment to an issue"""
        self.jira_client.add_comment(args['issue_key'], args['comment'])
        return {"message": f"Comment added to {args['issue_key']}"}
    
    def _update_issue(self, args: Dict) -> Dict:
        """Update an existing issue"""
        issue = self.jira_client.issue(args['issue_key'])
        update_fields = {}
        
        if 'summary' in args:
            update_fields['summary'] = args['summary']
        if 'description' in args:
            update_fields['description'] = args['description']
        
        issue.update(fields=update_fields)
        return {"message": f"Issue {args['issue_key']} updated successfully"}
    
    def _get_projects(self, args: Dict) -> List[Dict]:
        """Get list of projects"""
        projects = self.jira_client.projects()
        return [
            {
                "key": project.key,
                "name": project.name,
                "description": getattr(project, 'description', '')
            }
            for project in projects
        ]

def main():
    """Main entry point for the MCP server"""
    server = JiraMCPServer()
    
    if not server.initialize():
        logger.error("Failed to initialize server")
        sys.exit(1)
    
    logger.info("Jira MCP Server initialized successfully")
    logger.info("Server is ready to handle requests")
    
    # Keep the server running
    try:
        while True:
            # Read input from stdin
            line = input()
            if line.strip():
                try:
                    request_data = json.loads(line)
                    response = server.handle_request(request_data)
                    print(json.dumps(response))
                except json.JSONDecodeError:
                    logger.error("Invalid JSON input")
                except Exception as e:
                    logger.error(f"Error processing request: {e}")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except EOFError:
        logger.info("Server stopped")

if __name__ == "__main__":
    main() 