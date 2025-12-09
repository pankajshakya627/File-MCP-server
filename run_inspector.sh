#!/bin/bash
# Helper script to run MCP server with Inspector

echo "=================================================="
echo "Starting MCP Server with Inspector"
echo "=================================================="
echo ""
echo "This will:"
echo "  1. Run the MCP server in STDIO mode"
echo "  2. Launch MCP Inspector UI"
echo "  3. Open http://localhost:5173 in browser"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run with MCP Inspector
npx @modelcontextprotocol/inspector uv --directory "$(pwd)" run main.py
