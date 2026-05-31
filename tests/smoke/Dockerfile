# Smoke-test image. Build context is the repo root:
#   docker build -f tests/smoke/Dockerfile -t engram-mcp-smoke .
#
# The harness exercises the stdio MCP handshake against the
# installed `engram-mcp` console script — no live Engram backend.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY tests ./tests

RUN pip install -e ".[dev]"

CMD ["python", "tests/smoke/test_stdio_smoke.py"]
