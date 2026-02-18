# LangGraph MCP Codebase Instructions

## Project Overview

This monorepo demonstrates integrating **LangGraph** (agent orchestration) with **FastMCP** (Model Context Protocol servers) in Python. Two independent projects share common dependencies:

- **`agent/`**: LangGraph-based agent application with LLM orchestration
- **`mcp-server/`**: FastMCP server exposing LangGraph capabilities via MCP protocol

IMPORTANT: Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.


## Architecture & Key Patterns

### Dependency Management
- **Tool**: UV (uv - Astral's Python installer/manager) replaces pip/venv
- **Setup pattern**: Each project has independent `pyproject.toml` with isolated `uv.lock` and `.venv`
- **Bootstrap**: Run `uv sync` in each project directory to install dependencies and create virtual environments
- **Run pattern**: `uv run <command>` executes within project's environment (no manual activation needed)

### Project Structure
```
agent/
  pyproject.toml          # Declares langgraph, langchain, python-dotenv
  src/langgraph_agent/    # Agent application code
  .venv/                  # Isolated UV environment

mcp-server/
  pyproject.toml          # Declares fastmcp, langgraph, langchain, python-dotenv  
  src/langgraph_mcp_server/  # MCP server code
  .venv/                  # Isolated UV environment
```

### Development Workflows

**Initial setup:**
```bash
cd agent && uv sync && cd ..
cd mcp-server && uv sync && cd ..
```

**Running projects:**
```bash
cd agent && uv run python main.py
cd mcp-server && uv run python server.py
```

**Testing** (each project supports pytest):
```bash
uv run pytest
```

**Adding dependencies** (within project directory):
```bash
uv add langgraph  # production dep
uv add --dev pytest-asyncio  # dev dep
```

## Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **langgraph** | 1.0.8 | Agent state machine, graph-based orchestration |
| **langchain** | >=0.1.0 | LLM abstractions, prompt templates, output parsing |
| **fastmcp** | 2.14.5 (server only) | MCP protocol server implementation |
| **python-dotenv** | >=1.0.0 | Environment variable loading from `.env` files |

## Implementation Conventions

### Agent Project
- Entry point: `main.py` (referenced in README, not yet implemented)
- Expected pattern: Define LangGraph state graph with `StateGraph` or `MessageGraph`
- Use `langchain` for LLM calls, chain composition
- Environment config: Load via `.env` and `python-dotenv`
- Testing: `uv run pytest` in agent directory

### MCP Server Project
- Entry point: `server.py` (referenced in README, not yet implemented)
- Expected pattern: Use `fastmcp` decorators (`@mcp.tool()`, `@mcp.resource()`) to expose tools/resources
- Integration: Call LangGraph agents from MCP handlers
- Environment config: Same dotenv pattern as agent
- Testing: `uv run pytest` in mcp-server directory

## Critical Notes for AI Development

1. **Never modify uv.lock directly** – regenerate via `uv sync`
2. **Python 3.10+ required** – check with `python --version` before dev
3. **Async/await patterns**: Both langgraph and fastmcp use async heavily; pytest-asyncio included
4. **Environment variables**: Both projects expect `.env` files for secrets (API keys, LLM config)
5. **Monorepo isolation**: Changes in one project require `uv sync` in that directory only
6. **Import paths**: Use `from langgraph_agent.module import func` not relative paths across projects

## Testing & Validation

- Unit tests: `uv run pytest tests/` (create `tests/` directories as needed)
- Integration tests: Can test agent→server communication via MCP protocol
- Async tests: Use `pytest-asyncio` fixtures (already in dev-dependencies)

## File Organization Examples

**Agent implementation structure** (not yet present):
```
agent/src/langgraph_agent/
  __init__.py
  graph.py        # Define StateGraph, agents
  chains.py       # LangChain chains, prompts
  tools.py        # Tool definitions for agent
  main.py         # Entry point, CLI
```

**Server implementation structure** (not yet present):
```
mcp-server/src/langgraph_mcp_server/
  __init__.py
  server.py       # FastMCP server & routes
  handlers.py     # MCP tool/resource handlers
  agent_client.py # Interface to agent project logic
```

