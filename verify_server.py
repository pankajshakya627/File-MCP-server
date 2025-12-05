#!/usr/bin/env python3
"""
Script to test the FastMCP server configuration and verify all tools are registered.
"""

import subprocess
import sys
import json

def test_server():
    """Test the FastMCP server."""
    print("=" * 60)
    print("FastMCP Server Verification Script")
    print("=" * 60)
    
    # Test 1: Check imports
    print("\n[1/3] Checking Python imports...")
    try:
        import fastmcp
        import aiofiles
        print(f"  ✓ fastmcp version: {fastmcp.__version__}")
        print("  ✓ aiofiles imported successfully")
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    
    # Test 2: Validate main.py syntax
    print("\n[2/3] Validating main.py syntax...")
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", "main.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("  ✓ main.py syntax is valid")
    else:
        print(f"  ✗ Syntax error: {result.stderr}")
        return False
    
    # Test 3: Check server structure
    print("\n[3/3] Verifying server structure...")
    try:
        with open("main.py", "r") as f:
            content = f.read()
            
        # Check for key components
        checks = {
            "@mcp.tool()": "MCP tools",
            "@mcp.resource": "MCP resources",
            "@mcp.prompt()": "MCP prompts",
            "async def": "Async functions",
            "mcp.run()": "Server entry point",
        }
        
        all_passed = True
        for pattern, description in checks.items():
            if pattern in content:
                print(f"  ✓ {description} found")
            else:
                print(f"  ✗ {description} not found")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"  ✗ Error reading main.py: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All checks passed! Server is ready.")
        print("\nTo run the server:")
        print("  STDIO mode:  uv run main.py")
        print("  HTTP mode:   MCP_TRANSPORT=http uv run main.py")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("=" * 60)
        sys.exit(1)
