"""Run the Engram MCP plugin over stdio.

    python -m engram_mcp

Required env vars:
  ENGRAM_TOKEN     MCP-scoped token minted from the Engram web app
                   (Settings → MCP Tokens). 90-day TTL.
  ENGRAM_BASE_URL  Engram backend URL. Defaults to http://localhost:8000
                   for local dev; set to your hosted Engram URL in prod.
"""

import asyncio
import os
import sys

from mcp.server.stdio import stdio_server

from engram_mcp.client import EngramClient
from engram_mcp.server import build_server


async def main() -> None:
    base_url = os.environ.get("ENGRAM_BASE_URL", "http://localhost:8000")
    token = os.environ.get("ENGRAM_TOKEN")
    if not token:
        print(
            "ENGRAM_TOKEN is required. Mint one at <your-engram>/settings",
            file=sys.stderr,
        )
        sys.exit(2)

    client = EngramClient(base_url=base_url, token=token)
    server = build_server(client)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def cli() -> None:
    """Console-script entry point — `engram-mcp` after `pip install`."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
