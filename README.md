This repository contains three cooperating projects used for a small LangGraph + MCP example.

Overview
- `my-chat-ui` — Next.js + Turbo monorepo UI for chat (frontend).
- `langgraph-mcp/mcp-server` — FastMCP HTTP server exposing tools via MCP.
- `langgraph-mcp/agent` — LangGraph agent that loads tools from the MCP server and uses Ollama LLM.

Quick start (recommended run order)
1. Start the Ollama model (local model server).
2. Start the MCP server.
3. Start the agent (it loads tools from the MCP server).
4. Start the chat UI.

1) Ollama `ministral-3:14b` model
- Prereq: Install Ollama (https://ollama.com). Replace `ministral-3:14b` with your desired model name if needed.
- Pull the model locally:

	```bash
	ollama pull ministral-3:14b
	```

- Run the model as a local service (starts the model so `langchain-ollama`/`langchain_ollama` can connect):

	```bash
	ollama run ministral-3:14b
	```

2) MCP server (langgraph-mcp/mcp-server)
- Purpose: exposes tools (e.g., weather, hotel search) over an MCP HTTP endpoint at `http://localhost:8000/mcp`.

- Initialize and run:

	```bash
	cd langgraph-mcp/mcp-server
	python -m venv .venv
	source .venv/bin/activate
	pip install -e .
	python -m langgraph_mcp_server.server
	```

Notes:
- The server uses `uvicorn` internally and will print the HTTP and MCP endpoint on startup.

3) Agent (langgraph-mcp/agent)
- Purpose: a LangGraph ReAct agent that loads tools from the MCP server and queries the Ollama model.

- Initialize and run:

	```bash
	cd langgraph-mcp/agent
	python -m venv .venv
	source .venv/bin/activate
	pip install -e .
	# Run the agent module (it builds the graph and connects to MCP model)
	langgraph dev
	```

- If the project provides a `.env.example`, copy it and set any secrets before running:

	```bash
	cp .env.example .env
	# edit .env as needed
	```

4) Chat UI (my-chat-ui)
- Purpose: user-facing web app (Next.js / Turbo monorepo) that connects to the backend services.

- Initialize and run (requires Node.js and `pnpm`):

	```bash
	# from repository root
	cd my-chat-ui
	pnpm install
	pnpm dev
	```

- The `dev` script runs the monorepo dev servers (Turbo) used by the app.

Integration summary
- The UI sends user requests to your backend (typically the MCP server or an MCP-aware gateway). The agent connects to the MCP server at `http://localhost:8000/mcp` to load tools and orchestrates the LLM (Ollama) to answer queries. The MCP server is independent and should be started before the agent so the agent can fetch tool definitions.

Troubleshooting
- If the agent cannot load tools, verify the MCP server is running and reachable at `http://localhost:8000/mcp`.
- If the agent fails to initialize the LLM, confirm Ollama is running and the model name matches the one configured (the agent code in this repo uses `ministral-3:14b`).

Contributing
- Each subproject has its own `README.md` with more details.

---

That's it — start Ollama, then the MCP server, then the agent, then the UI.
