# Connect to the ShadowGraph MCP server

| | |
|---|---|
| Endpoint | `https://shadowalpha.online/_api/mcp` |
| Transport | Streamable HTTP (JSON responses) |
| Protocol versions | `2025-11-25` (also negotiates `2025-06-18`, `2025-03-26`, `2024-11-05`) and `2026-07-28` |
| MCP Registry | `online.shadowalpha/shadowgraph` ([`spec/server.json`](../spec/server.json)) |
| Auth | None. Paid tools use the Machine Payments Protocol, see [payments.md](payments.md) |

## Claude Code

```bash
claude mcp add --transport http shadowgraph https://shadowalpha.online/_api/mcp
```

Then type `/mcp` in Claude Code to see the tools.

## Claude (web and desktop app)

Settings → Connectors → Add custom connector

- Name: `ShadowGraph`
- URL: `https://shadowalpha.online/_api/mcp`

Then enable the connector in a chat from the tools menu.

## Claude Desktop (config file)

`claude_desktop_config.json`, bridged through [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) (needs Node.js):

```json
{
  "mcpServers": {
    "shadowgraph": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://shadowalpha.online/_api/mcp"]
    }
  }
}
```

## Cursor

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "shadowgraph": { "url": "https://shadowalpha.online/_api/mcp" }
  }
}
```

## VS Code

`.vscode/mcp.json`:

```json
{
  "servers": {
    "shadowgraph": { "type": "http", "url": "https://shadowalpha.online/_api/mcp" }
  }
}
```

## SDKs

- TypeScript: [`examples/javascript/mcp-client.mjs`](../examples/javascript/mcp-client.mjs)
- Python: [`examples/python/mcp_client.py`](../examples/python/mcp_client.py)

## Raw JSON-RPC

```bash
curl -s https://shadowalpha.online/_api/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Tools

| Tool | Price | Arguments |
|---|---|---|
| `shadowgraph_market_recap` | Free | `limit` 1–10 |
| `shadowgraph_company_filings` | Free | `symbol` (required), `limit` 1–10 |
| `shadowgraph_eu_tenders` | Free | `keyword`, `country` (two letters), `limit` 1–10 |
| `shadowgraph_free_preview` | Free | none |
| `shadowgraph_service_info` | Free | none |
| `shadowgraph_global_snapshot` | $0.50 / call | none |
| `shadowgraph_market_signal` | $0.75 / call | none |
| `shadowgraph_procurement_opportunity` | $1.00 / call | none |
| `shadowgraph_global_brief` | $2.50 / call | none |
| `shadowgraph_deep_research` | $5.00 / call | none |

`tools/list` on the live server is the authoritative list.
