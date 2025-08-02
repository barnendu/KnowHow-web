#!/usr/bin/env python3
"""
Test script for MCP Jira integration
"""

import json
import logging
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_utils import (
    create_jira_issue_mcp,
    search_jira_issues_mcp,
    get_jira_projects_mcp
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mcp_integration():
    """Test the MCP integration"""
    
    print("Testing MCP Jira Integration")
    print("=" * 40)
    
    # Test 1: Get available projects
    print("\n1. Testing get_projects...")
    try:
        projects = get_jira_projects_mcp()
        print(f"✅ Successfully retrieved {len(projects)} projects")
        for project in projects[:3]:  # Show first 3 projects
            print(f"   - {project['key']}: {project['name']}")
    except Exception as e:
        print(f"❌ Failed to get projects: {e}")
        return False
    
    # Test 2: Search for issues
    print("\n2. Testing search_issues...")
    try:
        issues = search_jira_issues_mcp("project = EP", max_results=5)
        print(f"✅ Successfully retrieved {len(issues)} issues")
        for issue in issues[:3]:  # Show first 3 issues
            print(f"   - {issue['key']}: {issue['summary']}")
    except Exception as e:
        print(f"❌ Failed to search issues: {e}")
        return False
    
    # Test 3: Create a test issue (optional)
    print("\n3. Testing create_issue...")
    test_ticket = """
    As a user, I want to test the MCP integration
    So that I can verify the system works correctly
    
    Acceptance Criteria:
    - The issue should be created successfully
    - The issue should have proper formatting
    - The issue should be assigned to the correct project
    
    Functional Test Cases:
    - Verify issue creation via MCP
    - Verify issue details are correct
    - Verify issue can be found via search
    """
    
    try:
        result = create_jira_issue_mcp(test_ticket)
        print(f"✅ Successfully created issue: {result['key']}")
        print(f"   - Summary: {result['summary']}")
        print(f"   - URL: {result['url']}")
    except Exception as e:
        print(f"❌ Failed to create issue: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("✅ All tests passed! MCP integration is working correctly.")
    return True

def test_parse_ticket():
    """Test the parse_ticket function"""
    print("\nTesting parse_ticket function")
    print("=" * 40)
    
    from tasks.parse_ticket import parse_ticket
    
    test_ticket = """
    As a developer, I want to implement user authentication
    So that users can securely access the application
    
    Acceptance Criteria:
    - Users can register with email and password
    - Users can login with valid credentials
    - Users can logout from the application
    - Password reset functionality is available
    
    Functional Test Cases:
    - Test user registration with valid data
    - Test user login with correct credentials
    - Test user login with incorrect credentials
    - Test password reset functionality
    """
    
    try:
        result = parse_ticket(test_ticket)
        print("✅ Successfully parsed ticket")
        print(f"   - Title: {result['fields']['summary']}")
        print(f"   - Project: {result['fields']['project']['key']}")
        print(f"   - Issue Type: {result['fields']['issuetype']['name']}")
        print(f"   - Description length: {len(result['fields']['description']['content'][0]['content'][0]['text'])} characters")
    except Exception as e:
        print(f"❌ Failed to parse ticket: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("MCP Jira Integration Test Suite")
    print("=" * 50)
    
    # Check environment variables
    required_env_vars = ["JIRA_URL", "EMAIL", "ATLASSIAN_API_TOKEN"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please set the following environment variables:")
        for var in missing_vars:
            print(f"   export {var}='your-value'")
        return False
    
    print("✅ Environment variables are set")
    
    # Test parse_ticket function
    if not test_parse_ticket():
        return False
    
    # Test MCP integration
    if not test_mcp_integration():
        return False
    
    print("\n🎉 All tests completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 