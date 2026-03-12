# Langgraph Code Examples

This repository contains following projects used for a small LangGraph + MCP example and other examples.

## Overview
1. `my-chat-ui` — Next.js + Turbo monorepo UI for chat (frontend).

2. `my-chat-ui-deep-agent`- A simple front-end in Next.js built on top of the `my-chat-ui` to add Deep Agent specific UI components (reference: https://github.com/langchain-ai/langgraphjs/tree/main/examples/ui-react).

	>However use this instead- `deep-agents-ui` - A separate cloned project (not committed into this repo) that serves the same purpose as `my-chat-ui-deep-agent` but is maintained independently. It is ignored by Git via `.gitignore`.`

3. `langgraph-mcp/mcp-server` — FastMCP HTTP server exposing tools via MCP.

4. `langgraph-mcp/agents` — It has two agents: 
	1. A simple **LangGraph agent** that loads tools from the MCP server and uses Ollama LLM. 
	2. A simple **DeepAgent** implementation with a research sub-agent, hotel search sub-agent and a main agent that can call the research agent or hotel search agent as a tool. Both agents use the same MCP server for tools and Ollama for LLM. Reference: https://github.com/langchain-ai/deepagents/tree/main/examples/deep_research

# Running The Simple ReAct Agent

## Quick start (recommended run order)
1. Start the Ollama model (local model server).
2. Start the MCP server.
3. Start the agent (it loads tools from the MCP server).
4. Start the chat UI.

### 1. Ollama `ministral-3:14b` model
- Prereq: Install Ollama (https://ollama.com). Replace `ministral-3:14b` with your desired model name if needed.
- Pull the model locally:

	```bash
	ollama pull ministral-3:14b
	```

- Run the model as a local service (starts the model so `ChatOllama` can connect):

	```bash
	ollama run ministral-3:14b
	```

### 2. MCP server (langgraph-mcp/mcp-server)
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

### 3. Agent (langgraph-mcp/agents)
- Purpose: a LangGraph ReAct agent that loads tools from the MCP server and queries the Ollama model.

- Initialize and run:

	```bash
	cd langgraph-mcp/agents
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

### 4. Chat UI (my-chat-ui)
- Purpose: user-facing web app (Next.js / Turbo monorepo) that connects to the backend services.

- Initialize and run (requires Node.js and `pnpm`):

	```bash
	# from repository root
	cd my-chat-ui
	pnpm install
	pnpm dev
	```

- The `dev` script runs the monorepo dev servers (Turbo) used by the app.

# Running The Example Deep Agent

## Quick start (recommended run order)
1. Pull and connect to a cloud Ollama model (Recommended to use Ollama Cloud model such as `nemotron-3-super:cloud`, `gpt-oss:120b-cloud` instead of local model server).
2. Start the MCP server.
3. Start the deep agent (it loads tools from the MCP server).
4. Start the chat UI.

### 1) Ollama cloud model
- **Prereq:**
	- Install Ollama (https://ollama.com).
	- Create an account on Ollama Cloud (https://signin.ollama.com).
	- Create an API key in the Ollama Cloud dashboard and set it in your `.env` file as `OLLAMA_API_KEY=your_ollama_api_key_here`.

- Sign in to Ollama Cloud from your terminal (Ref. this if needed more information: https://docs.ollama.com/cloud#running-cloud-models):

	```bash
	ollama signin
	```
	Authenticate by logging in with your credentials. This allows you to pull and run cloud-hosted models.

- Pull the model locally:

	```bash
	ollama pull nemotron-3-super:cloud
	```

### 2. Tavily Setup
- **Prereq:** Create an account on Tavily (https://tavily.com) and get your API key. Set it in your `.env` file as `TAVILY_API_KEY=your_tavily_api_key_here`.

### 3. MCP server (langgraph-mcp/mcp-server)
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

### 4. Deep Agent (langgraph-mcp/agents)
- Purpose: a simple Deep Agent implementation with a research sub-agent, hotel search sub-agent, and a main agent that can call the research agent or hotel search agent as a tool. Both agents use the same MCP server for tools and Ollama for LLM.

- Initialize and run:

	```bash
	cd langgraph-mcp/agents
	python -m venv .venv
	source .venv/bin/activate
	pip install -e .
	# Run the agent module (it builds the graph and connects to MCP model)
	langgraph dev
	```

### 5. Deep Agents UI
- Uses the `deep-agents-ui` project instead of the `my-chat-ui-deep-agent` in this repo. It is a separate cloned project that serves the same purpose but is maintained independently by Langchain community. It is ignored by Git via `.gitignore`.
- Reference: https://github.com/langchain-ai/deep-agents-ui
- Initialize and run:

	```bash
	git clone https://github.com/langchain-ai/deep-agents-ui.git
	cd deep-agents-ui
	yarn install
	yarn dev
	```

## Integration summary
- The UI sends user requests to your backend (typically the MCP server or an MCP-aware gateway). The agent connects to the MCP server at `http://localhost:8000/mcp` to load tools and orchestrates the LLM (Ollama) to answer queries. The MCP server is independent and should be started before the agent so the agent can fetch tool definitions.

## Troubleshooting
- If the agent cannot load tools, verify the MCP server is running and reachable at `http://localhost:8000/mcp`.
- If the agent fails to initialize the LLM, confirm Ollama is running and the model name matches the one configured (the agent code in this repo uses `ministral-3:14b`).

## Contributing
- Each subproject has its own `README.md` with more details.

---

That's it — start Ollama, then the MCP server, then the agent, then the UI.
