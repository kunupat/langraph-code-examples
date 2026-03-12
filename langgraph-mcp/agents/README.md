This directory contains two LangGraph agent implementations that load tools from a local MCP server:

1. **Simple ReActAgent** - A basic agent using local Ollama with `ministral-3:14b` model
2. **DeepAgent** - An advanced implementation with research and hotel search sub-agents using cloud Ollama models

## Prerequisites (Both Agents)
- Python 3.12+
- MCP server running at `http://localhost:8000/mcp` (see [MCP Server README](../mcp-server/README.md))

## Setup

```bash
cd langgraph-mcp/agents
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

## Running the Simple ReActAgent

Prerequisites:
- Ollama running with the `ministral-3:14b` model (see repository root README)

```bash
# Ensure the MCP server and Ollama are running
langgraph dev
```

## Running the DeepAgent

Prerequisites:
- Ollama account and cloud model (e.g., `nemotron-3-super:cloud`)
- Tavily API key for web search capabilities
- Required environment variables in `.env`:
  - `OLLAMA_API_KEY` - Your Ollama Cloud API key
  - `TAVILY_API_KEY` - Your Tavily API key

See the repository root README for detailed setup instructions and integration order.

```bash
# Ensure the MCP server is running
langgraph dev
```

## Configuration

- The simple agent expects the Ollama model named `ministral-3:14b` by default
- The deep agent uses cloud Ollama models specified in configuration
- See the project root README for complete integration steps and additional details

