"""List ShadowGraph's MCP tools and call a free one with the official Python SDK.

Needs: pip install mcp
"""
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "https://shadowalpha.online/_api/mcp"


async def main() -> None:
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"{t.name:40} {t.description[:70]}")
            result = await session.call_tool("shadowgraph_company_filings", {"symbol": "NVDA", "limit": 3})
            print(result.content[0].text[:500])


asyncio.run(main())
