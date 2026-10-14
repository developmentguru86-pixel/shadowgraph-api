// List ShadowGraph's MCP tools and call a free one with the official TypeScript SDK.
// Needs: npm i @modelcontextprotocol/sdk   (Node 18+)
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const client = new Client({ name: "shadowgraph-example", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(new URL("https://shadowalpha.online/_api/mcp")));

const { tools } = await client.listTools();
for (const t of tools) console.log(t.name.padEnd(40), t.description.slice(0, 70));

const filings = await client.callTool({ name: "shadowgraph_company_filings", arguments: { symbol: "NVDA", limit: 3 } });
console.log(filings.content[0].text.slice(0, 500));
await client.close();
