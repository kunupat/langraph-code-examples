Minimal LangGraph agent that loads tools from a local MCP server and uses Ollama.

Prerequisites
- Python 3.12+
- Ollama running with the `ministral-3:14b` model (see repository root README)

Setup

```bash
cd langgraph-mcp/agent
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env  # optional: configure secrets
```

Run

```bash
# Ensure the MCP server and Ollama are running
langgraph dev
```

Notes
- The agent expects an MCP server at `http://localhost:8000/mcp` and uses the Ollama model named `ministral-3:14b` by default.
- See the project root README for integration order and additional details.

