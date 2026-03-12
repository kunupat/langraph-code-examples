Frontend Next.js (Turbo) chat UI for the simple ReActAgent example.

Prerequisites
- Node.js (16+ recommended)
- pnpm package manager
- Backend services running: Ollama, MCP server, and LangGraph agent (see [root README](../README.md))

Setup

```bash
cd my-chat-ui
pnpm install
```

Run (development)

```bash
pnpm dev
```

Notes
- The UI runs in the Turbo monorepo; `pnpm dev` starts the web and agents dev servers.
- This is the UI for the simple ReActAgent. For the DeepAgent UI, use [deep-agents-ui](https://github.com/langchain-ai/deep-agents-ui) instead.
- See the project root README for the recommended startup order: Ollama -> MCP server -> agent -> UI.

