# test_cloud.py
import asyncio
from fastmcp import Client

async def main():
    async with Client("https://file-management.fastmcp.app/mcp") as client:
        # List tools
        tools = await client.list_tools()
        print(f"✅ Connected! Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}")

asyncio.run(main())