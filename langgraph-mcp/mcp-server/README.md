# LangGraph MCP Server

A basic HTTP MCP (Model Context Protocol) server built with FastMCP and LangGraph integration.

## Features

- **Echo Tool**: Echoes back input messages
- **Calculate Tool**: Evaluates mathematical expressions
- **Get Info Tool**: Returns server information
- **HTTP Transport**: Runs on HTTP with SSE (Server-Sent Events) endpoint

## Quick Start

### Setup

```bash
cd mcp-server
uv sync
```

### Running the Server

```bash
uv run python -m langgraph_mcp_server.server
```

The server will start at `http://localhost:8000`

### Available Endpoints

- **GET `/`** - Root endpoint
- **POST `/mcp/sse`** - SSE (Server-Sent Events) endpoint for MCP protocol

## Available Tools

### 1. Echo
Echoes back the input message.

**Parameters:**
- `message` (string): The message to echo

**Example:**
```bash
# Via MCP client
tool_name: "echo"
arguments: {"message": "Hello, MCP Server!"}
```

### 2. Calculate
Evaluates mathematical expressions.

**Parameters:**
- `expression` (string): A mathematical expression (e.g., "2 + 2", "10 * 5")

**Example:**
```bash
# Via MCP client
tool_name: "calculate"
arguments: {"expression": "10 + 20"}
# Returns: "10 + 20 = 30"
```

### 3. Get Info
Returns information about the server.

**Example:**
```bash
# Via MCP client
tool_name: "get_info"
arguments: {}
```

## Architecture

The server is built with:
- **FastMCP**: Model Context Protocol server implementation
- **Uvicorn**: ASGI server for HTTP transport
- **Pydantic**: Data validation

## Extending the Server

To add new tools, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_tool(param: str) -> str:
    """Description of my tool."""
    return f"Result: {param}"
```

## Configuration

The server runs with default settings:
- **Host**: `0.0.0.0`
- **Port**: `8000`
- **Log Level**: `info`

Modify `server.py` to change these settings.
