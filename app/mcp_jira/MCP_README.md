# MCP Jira Integration

This directory contains the Model Context Protocol (MCP) implementation for Jira integration.

## Overview

The MCP Jira integration provides a standardized way to interact with Jira through the Model Context Protocol. It consists of:

1. **MCP Server** (`mcp_jira_server.py`) - Implements the MCP server protocol for Jira operations
2. **MCP Client** (`mcp_jira_client.py`) - Client for communicating with the MCP server
3. **MCP Utilities** (`mcp_utils.py`) - Helper functions for MCP operations
4. **API Integration** (`views/integrated_views.py`) - Flask routes that use MCP for Jira operations

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │    │   MCP Client    │    │   MCP Server    │
│                 │    │                 │    │                 │
│ /api/integration│───▶│  JiraMCPClient  │───▶│  JiraMCPServer  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   Jira API      │
                                               │                 │
                                               │  REST API       │
                                               └─────────────────┘
```

## Features

### MCP Server Tools

The MCP server provides the following tools:

1. **create_issue** - Create a new Jira issue
2. **get_issue** - Get issue details by key
3. **search_issues** - Search for issues using JQL
4. **add_comment** - Add comment to an issue
5. **update_issue** - Update an existing issue
6. **get_projects** - Get list of available projects

### API Endpoints

The Flask app provides the following endpoints:

- `POST /api/integration/jira` - Create Jira issue
- `POST /api/integration/jira/search` - Search Jira issues
- `GET /api/integration/jira/issue/<issue_key>` - Get issue details
- `POST /api/integration/jira/issue/<issue_key>/comment` - Add comment
- `GET /api/integration/jira/projects` - Get available projects

## Setup

### 1. Install Dependencies

```bash
pip install mcp-cli jira
```

### 2. Environment Variables

Set the following environment variables:

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export EMAIL="your-email@example.com"
export ATLASSIAN_API_TOKEN="your-api-token"
```

### 3. Run the MCP Server

```bash
python app/web/mcp_jira_server.py
```

## Usage

### Creating a Jira Issue

```python
from app.web.mcp_utils import run_async_mcp_operation, create_jira_issue_mcp

# Create an issue
result = run_async_mcp_operation(create_jira_issue_mcp("Your ticket text here"))
print(result)
```

### Searching Issues

```python
from app.web.mcp_utils import run_async_mcp_operation, search_jira_issues_mcp

# Search for issues
result = run_async_mcp_operation(search_jira_issues_mcp("project = EP AND status = Open"))
print(result)
```

### API Usage

```bash
# Create an issue
curl -X POST http://localhost:5000/api/integration/jira \
  -H "Content-Type: application/json" \
  -d '{"ticket": "Your ticket text here"}'

# Search issues
curl -X POST http://localhost:5000/api/integration/jira/search \
  -H "Content-Type: application/json" \
  -d '{"jql": "project = EP", "max_results": 10}'
```

## Benefits of MCP Integration

1. **Standardized Protocol** - Uses the Model Context Protocol for consistent communication
2. **Separation of Concerns** - Server and client are separate, allowing for better modularity
3. **Extensibility** - Easy to add new tools and capabilities
4. **Error Handling** - Robust error handling and logging
5. **Async Support** - Full async/await support for better performance

## Configuration

The MCP server configuration is stored in `mcp_config.json`:

```json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["app/web/mcp_jira_server.py"],
      "env": {
        "JIRA_URL": "${JIRA_URL}",
        "EMAIL": "${EMAIL}",
        "ATLASSIAN_API_TOKEN": "${ATLASSIAN_API_TOKEN}"
      }
    }
  }
}
```

## Error Handling

The MCP integration includes comprehensive error handling:

- Connection failures
- Authentication errors
- Invalid tool calls
- Jira API errors

All errors are logged and returned with appropriate HTTP status codes.

## Testing

To test the MCP integration:

1. Start the Flask app
2. Run the MCP server
3. Test the API endpoints
4. Check the logs for any errors

## Troubleshooting

### Common Issues

1. **Connection Failed** - Check environment variables and network connectivity
2. **Authentication Error** - Verify Jira credentials
3. **Tool Not Found** - Ensure the MCP server is running and tools are registered
4. **Async Runtime Error** - Check that asyncio is properly configured

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

1. **WebSocket Support** - Real-time communication
2. **Caching** - Cache frequently accessed data
3. **Rate Limiting** - Implement rate limiting for API calls
4. **Webhook Support** - Handle Jira webhooks
5. **Bulk Operations** - Support for bulk issue operations 