# UE Knowledge Base

This is a two-layer knowledge base for Unreal Engine 5 + MCP development.

## Structure

### `knowledge/` — Refined notes (grep layer)
Battle-tested, Claude-maintained notes combining UE5 documentation with MCP-specific how-tos, gotchas, and workarounds. These are the primary reference.

- `knowledge/ue5/` — UE5 engine topics (blueprints, animation, materials, input, etc.)
- `knowledge/mcp/` — MCP tool patterns, what works, what doesn't
- `knowledge/troubleshooting/` — Solutions to problems we've hit

### `docs/` — Raw documentation (RAG layer)
Bulk ingested PDFs, scraped UE docs, tutorials. Searchable via semantic search (mcp-local-rag).

- `docs/pdfs/` — PDF tutorials and documentation
- `docs/ue5-docs/` — Scraped/converted UE5 documentation pages

## How to use this knowledge base

1. **Before doing something in UE5**, search `knowledge/` first using Grep/Glob (fast, precise)
2. **If not found**, query the RAG layer using `query_documents` (semantic search over docs/)
3. **After completing a task**, update or create a note in `knowledge/` with what you learned
4. **Always include MCP commands** in knowledge notes — document both the UE way and the MCP way

## Rules for writing knowledge notes

- Keep notes concise and actionable
- Include working MCP tool calls as code blocks
- Document gotchas and things that DON'T work
- Link related notes using relative paths
- Each file should cover one topic
