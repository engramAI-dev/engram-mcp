"""Engram MCP plugin.

Stdio MCP server that exposes an Engram workspace (indexed GitHub +
Notion knowledge) to MCP clients like Cursor, Claude Code, Claude
Desktop, and Codex.

The plugin is a thin HTTP client against the Engram backend — no DB,
no embedding model, no vector store runs locally. Install, paste your
Engram token, and the host LLM can search, cite, and fetch documents
from your workspace.
"""

__version__ = "0.1.0"
