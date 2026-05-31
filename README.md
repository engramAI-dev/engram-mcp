# engram-mcp

[![PyPI](https://img.shields.io/pypi/v/engram-mcp.svg)](https://pypi.org/project/engram-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCP plugin that connects Cursor, Claude Code, Claude Desktop, and any
other MCP-speaking host to your [Engram](https://github.com/hidden-ones-dev/Engram)
workspace — the indexed knowledge of your GitHub repos and Notion pages.

The plugin is a **thin client**: no local database, no embedding model,
no vector store. It forwards tool calls to the Engram backend over
HTTPS and renders the results for your LLM.

## Install

```bash
pip install engram-mcp
# or
uv tool install engram-mcp
```

## Configure your MCP client

You need two things:

1. Your Engram backend URL — `https://your-engram.example.com` in
   production, or `http://localhost:8000` for local development.
2. An Engram MCP token — mint one from your Engram web app under
   **Settings → MCP Tokens**. Tokens are scoped to your user and expire
   after 90 days.

### Claude Desktop / Claude Code

Add to `claude_desktop_config.json` (or the equivalent Claude Code
config):

```jsonc
{
  "mcpServers": {
    "engram": {
      "command": "engram-mcp",
      "env": {
        "ENGRAM_BASE_URL": "https://your-engram.example.com",
        "ENGRAM_TOKEN": "eng_mcp_..."
      }
    }
  }
}
```

### Cursor

In Cursor settings → MCP → Add new server:

```jsonc
{
  "engram": {
    "command": "engram-mcp",
    "env": {
      "ENGRAM_BASE_URL": "https://your-engram.example.com",
      "ENGRAM_TOKEN": "eng_mcp_..."
    }
  }
}
```

### Codex CLI

```toml
# ~/.codex/config.toml
[mcp_servers.engram]
command = "engram-mcp"
env = { ENGRAM_BASE_URL = "https://your-engram.example.com", ENGRAM_TOKEN = "eng_mcp_..." }
```

## Tools exposed

| Tool | What it does |
|---|---|
| `search_knowledge` | Ranked search across your indexed GitHub + Notion content. Supports `source` filter and `intent` shaping (`explain` / `generate` / `question`). |
| `cite` | Locators only (source, path, line range, URL) for an answer the LLM has already drafted — cheap on context. |
| `fetch_document` | Full document fetch by id, optionally with surrounding context lines. Use after `search_knowledge` surfaces something interesting. |

## How it works

```
┌───────────────────┐  stdio MCP   ┌───────────────────┐  HTTPS   ┌──────────────────┐
│ Cursor / Claude   │ ───────────► │ engram-mcp        │ ───────► │ Engram backend   │
│ Code / Desktop    │              │ (this package)    │  bearer  │ (indexing, RAG,  │
└───────────────────┘              └───────────────────┘   token  │  cross-val)      │
                                                                  └──────────────────┘
```

The plugin holds no state. Your token authenticates each request to
the Engram backend, which resolves it to your user + workspace, runs
retrieval against the indexed corpus, and returns ranked chunks. The
plugin formats those chunks as markdown for the host LLM.

## Auth

`v0.x` uses **paste tokens** — generate one in the Engram web app,
paste into the env var. Tokens are stored hashed server-side and you
can revoke them from the same settings page.

`v1.x` will add **OAuth 2.1** (device flow + Dynamic Client
Registration) so you can add Engram as a `claude.ai` connector with
zero copy-paste. Paste tokens will keep working.

## Development

```bash
git clone https://github.com/hidden-ones-dev/engram-mcp
cd engram-mcp
pip install -e ".[dev]"
pytest
```

Point at a local Engram backend:

```bash
export ENGRAM_BASE_URL=http://localhost:8000
export ENGRAM_TOKEN=eng_mcp_...
python -m engram_mcp   # speaks stdio MCP; pipe from a host or test harness
```

## License

MIT — see [LICENSE](LICENSE).

## Related

- [Engram](https://github.com/hidden-ones-dev/Engram) — the backend
  this plugin talks to.
- [Model Context Protocol](https://modelcontextprotocol.io) — the
  protocol spec.
