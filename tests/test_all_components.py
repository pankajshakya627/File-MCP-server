# test_all_components.py
"""Test all MCP components: Tools, Resources, and Prompts"""
import asyncio
from fastmcp import Client


async def main():
    async with Client("https://file-management.fastmcp.app/mcp") as client:
        print("=" * 60)
        print("🔧 TOOLS")
        print("=" * 60)
        tools = await client.list_tools()
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:50]}..." if tool.description else f"  - {tool.name}")
        
        print("\n" + "=" * 60)
        print("📚 RESOURCES")
        print("=" * 60)
        resources = await client.list_resources()
        print(f"Found {len(resources)} resources:")
        for resource in resources:
            print(f"  - {resource.uri}: {resource.name}")
        
        # Read a resource
        if resources:
            print("\n📖 Reading 'server://info' resource:")
            content = await client.read_resource("server://info")
            print(f"  {str(content)[:200]}...")
        
        print("\n" + "=" * 60)
        print("💬 PROMPTS")
        print("=" * 60)
        prompts = await client.list_prompts()
        print(f"Found {len(prompts)} prompts:")
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description[:50]}..." if prompt.description else f"  - {prompt.name}")
        
        # Test a prompt
        if prompts:
            print("\n📝 Getting 'code_review_prompt' with sample code:")
            result = await client.get_prompt("code_review_prompt", {"code": "def hello(): return 'world'"})
            print(f"  {str(result)[:300]}...")
        
        print("\n" + "=" * 60)
        print("✅ ALL COMPONENTS VERIFIED!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
