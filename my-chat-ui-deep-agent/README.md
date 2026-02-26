Frontend Next.js (Turbo) chat UI used in this example monorepo.

Prerequisites
- Node.js (16+ recommended)
- pnpm package manager

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
- Configure backend endpoints or API keys as needed; see the project root README for integration order (Ollama -> MCP server -> agent -> UI).

