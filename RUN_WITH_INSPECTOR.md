# Running with MCP Inspector

## ⚠️ Important: MCP Inspector Uses STDIO, Not HTTP

The MCP Inspector communicates via STDIO (standard input/output), not HTTP endpoints.

## How to Run with MCP Inspector

### Step 1: Stop the Docker Container
```bash
# Stop the running Docker container
docker stop $(docker ps -q --filter ancestor=local-utils-mcp)
```

### Step 2: Change Default Transport Back to STDIO

The `main.py` should default to STDIO mode. Change line 918:

```python
# Change this:
transport_mode = os.environ.get("MCP_TRANSPORT", "http")  

# To this:
transport_mode = os.environ.get("MCP_TRANSPORT", "stdio")  # Default to stdio
```

### Step 3: Run with MCP Inspector

```bash
# Option A: Using npx (recommended)
npx @modelcontextprotocol/inspector uv --directory /Volumes/CrucialX9_MAC/Local_MCPs/mcp-local run main.py

# Option B: If you have inspector installed globally
mcp-inspector uv --directory /Volumes/CrucialX9_MAC/Local_MCPs/mcp-local run main.py
```

### Step 4: Open Browser

The inspector will show you a URL like:
```
Inspector running at http://localhost:5173
```

Open this URL in your browser to use the MCP Inspector UI.

---

## Alternative: HTTP Mode for REST API Testing

If you want to test the HTTP endpoints directly (not via Inspector):

### Step 1: Keep Docker Running in HTTP Mode
```bash
docker run --rm -p 8000:8000 local-utils-mcp
```

### Step 2: Test with curl
```bash
# Health check
curl http://localhost:8000/health

# List available tools via MCP HTTP endpoint
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

### Step 3: Use ngrok for external access
```bash
ngrok http 8000
# Then use the ngrok URL for testing
```

---

## Summary

- **MCP Inspector** → Requires **STDIO mode** → Run locally with `uv run main.py`
- **REST API / HTTP Testing** → Requires **HTTP mode** → Use Docker or `MCP_TRANSPORT=http uv run main.py`
- **Claude Desktop** → Requires **STDIO mode** → Configure in Claude settings

Choose the mode based on your use case!
