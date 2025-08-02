#!/usr/bin/env python3
"""
MCP Jira Client Implementation
Client for communicating with the custom Jira MCP server
"""

import asyncio
import json
import logging
import subprocess
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JiraIssue:
    """Jira issue data structure"""
    key: str
    summary: str
    description: str
    status: str
    url: str

class JiraMCPClient:
    """Client for communicating with Jira MCP server"""
    
    def __init__(self, server_path: str = "python app/mcp_jira/mcp_jira_server.py"):
        self.server_path = server_path
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
    
    def connect(self):
        """Connect to the MCP server"""
        try:
            # Start the server process
            self.process = subprocess.Popen(
                self.server_path.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Wait a moment for the server to initialize
            time.sleep(1)
            
            # Check if the process is still running
            if self.process.poll() is not None:
                stderr_output = self.process.stderr.read() if self.process.stderr else "No stderr output"
                raise Exception(f"Server process failed to start: {stderr_output}")
            
            logger.info("Connected to Jira MCP server")
            
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise
    
    def send_request(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Send MCP request to server"""
        if not self.process:
            raise Exception("Not connected to MCP server")
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": str(self.request_id),
            "method": method,
            "params": params or {}
        }
        
        try:
            # Send request to server
            request_json = json.dumps(request) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            # Read response from server
            response_line = self.process.stdout.readline()
            if not response_line:
                raise Exception("No response from server")
            
            response = json.loads(response_line.strip())
            
            if "error" in response:
                raise Exception(f"Server error: {response['error']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        response = self.send_request("tools/list")
        return response.get("result", {}).get("tools", [])
    
    def call_tool(self, name: str, arguments: Dict) -> Any:
        """Call a specific tool"""
        response = self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
        
        # Parse the response content
        result = response.get("result", {})
        content = result.get("content", [])
        
        if content and len(content) > 0:
            text_content = content[0].get("text", "")
            try:
                return json.loads(text_content)
            except json.JSONDecodeError:
                return text_content
        else:
            return None
    
    def create_issue(self, project: str, summary: str, description: str = "", issue_type: str = "Task") -> Dict[str, Any]:
        """Create a new Jira issue"""
        return self.call_tool("create_issue", {
            "project": project,
            "summary": summary,
            "description": description,
            "issue_type": issue_type
        })
    
    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get issue details"""
        return self.call_tool("get_issue", {
            "issue_key": issue_key
        })
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for issues using JQL"""
        return self.call_tool("search_issues", {
            "jql": jql,
            "max_results": max_results
        })
    
    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """Add comment to an issue"""
        return self.call_tool("add_comment", {
            "issue_key": issue_key,
            "comment": comment
        })
    
    def update_issue(self, issue_key: str, summary: str = None, description: str = None) -> Dict[str, Any]:
        """Update an existing issue"""
        args = {"issue_key": issue_key}
        if summary:
            args["summary"] = summary
        if description:
            args["description"] = description
        
        return self.call_tool("update_issue", args)
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of available projects"""
        return self.call_tool("get_projects", {})
    
    def close(self):
        """Close the client session"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            logger.info("Disconnected from MCP server")

# Example usage
def main():
    """Example usage of the MCP Jira client"""
    client = JiraMCPClient()
    
    try:
        client.connect()
        
        # List available tools
        print("Available tools:")
        tools = client.list_tools()
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")
        
        # Get available projects
        print("\nAvailable projects:")
        projects = client.get_projects()
        for project in projects:
            print(f"- {project['key']}: {project['name']}")
        
        # Create a new issue
        print("\nCreating new issue...")
        result = client.create_issue(
            project="EP",
            summary="Test issue created via MCP",
            description="This is a test issue created through MCP integration",
            issue_type="Task"
        )
        print(f"Created issue: {result}")
        
        # Search for issues
        print("\nSearching for issues...")
        search_result = client.search_issues(
            jql="project = EP AND status = Open",
            max_results=10
        )
        print(f"Search results: {search_result}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main() 