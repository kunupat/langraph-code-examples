FastMCP-based MCP server exposing tools over HTTP for the LangGraph example.

Prerequisites
- Python 3.10+

Setup

```bash
cd langgraph-mcp/mcp-server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run

```bash
# Starts the FastMCP HTTP server and exposes the MCP endpoint
python -m langgraph_mcp_server.server
# Server listens on http://0.0.0.0:8000 and MCP endpoint is http://localhost:8000/mcp
```

Notes
- Ensure this server is started before the agent so the agent can fetch tool definitions.
- See the project root README for overall integration steps.

