# FastMCP Local Utils Server

A comprehensive Model Context Protocol (MCP) server built with FastMCP, providing file operations, text processing, math utilities, and more. Perfect for integrating with Claude Desktop or deploying as a network service.

## 🌟 Features

### 📁 File Operations
- **Read/Write/Append** - Complete file manipulation
- **Smart Text Replacement** - Find and replace with occurrence counting
- **Safe Deletion** - Delete files with validation
- **Overwrite Protection** - Optional safeguards against accidental overwrites

### 📂 Directory Management
- **List Contents** - View files and directories with optional details (size, dates)
- **Find Files** - Recursive search with glob patterns
- **Create Directories** - Make new directories with parent creation
- **Smart Organization** - Auto-organize files by:
  - **Type**: Documents, Images, Videos, Audio, Code, Archives, etc.
  - **Date**: Year-Month folders based on modification time
  - **Size**: Small/Medium/Large categories

### 📝 Text Processing
- **Word Counter** - Count words, characters, and lines
- **Text Search** - Find text with context snippets
- **Statistics** - Detailed text analysis

### 🔢 Math Operations
- **Calculator** - Evaluate math expressions (supports sqrt, sin, cos, log, etc.)
- **Basic Math** - Add and multiply numbers with formatted output

### 🛠️ Utilities
- **Greetings** - Generate personalized messages
- **Time/Date** - Get current timestamp
- **Server Info** - Query available tools and capabilities

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/pankajshakya627/File-MCP-server.git
cd File-MCP-server

# Install dependencies (uv will handle this automatically)
uv sync

# Run the server
uv run main.py
```

### Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd mcp-local

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastmcp

# Run the server
python main.py
```

## 🚀 Usage

### STDIO Transport (Default)

Perfect for Claude Desktop and local development:

```bash
uv run main.py
```

### Development Mode

With auto-reload on code changes:

```bash
uv run fastmcp dev main.py
```

## 🔧 Configuration for Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "local-utils": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-local",
        "run",
        "main.py"
      ]
    }
  }
}
```

Replace `/absolute/path/to/mcp-local` with the actual path to your project directory.

After updating the config:
1. Restart Claude Desktop
2. Look for the 🔌 icon to confirm the server is connected
3. Start using the tools in your conversations!

## 📚 Available Tools

### File Operations

#### `read_file(path: str) -> str`
Read and return file contents with metadata.

```python
# Example usage in Claude
"Read the file at ~/Documents/notes.txt"
```

#### `write_file(path: str, content: str, overwrite: bool = True) -> str`
Write content to a file. Creates parent directories if needed.

```python
"Write 'Hello World' to ~/test.txt"
"Write the content to config.json without overwriting if it exists"
```

#### `append_to_file(path: str, content: str) -> str`
Append content to the end of a file.

```python
"Append today's log entry to ~/logs/app.log"
```

#### `update_file(path: str, old_text: str, new_text: str, count: int = -1) -> str`
Replace text in a file with occurrence counting.

```python
"Replace 'TODO' with 'DONE' in ~/project/tasks.md"
"Replace the first occurrence of 'debug = True' with 'debug = False'"
```

#### `delete_file(path: str) -> str`
Safely delete a file with validation.

```python
"Delete the file ~/temp/old_data.csv"
```

### Directory Operations

#### `list_directory(path: str = ".", show_hidden: bool = False, detailed: bool = False) -> str`
List directory contents with optional details.

```python
"List all files in ~/Documents"
"Show detailed information for files in the current directory"
"List hidden files in ~/.config"
```

#### `find_files(directory: str = ".", pattern: str = "*", recursive: bool = True, max_results: int = 100) -> str`
Find files matching a pattern.

```python
"Find all Python files in ~/projects"
"Find all *.md files in the current directory, non-recursively"
"Find all test_*.py files"
```

#### `create_directory(path: str, parents: bool = True) -> str`
Create a new directory.

```python
"Create a directory at ~/projects/new-app/src"
```

#### `organize_directory(directory: str = ".", by: str = "type", dry_run: bool = False) -> str`
Organize files into subdirectories.

**Organization Methods:**
- `type`: By file extension (Documents, Images, Videos, Audio, Code, Archives, Other)
- `date`: By modification date (YYYY-MM folders)
- `size`: By file size (Small, Medium, Large)

```python
"Organize ~/Downloads by file type"
"Organize the current directory by date (dry run first)"
"Organize ~/Desktop by size"
```

### Text Processing

#### `count_words(text: str) -> str`
Analyze text statistics (words, characters, lines).

```python
"Count the words in this text: [your text here]"
```

#### `search_text(text: str, query: str, case_sensitive: bool = False) -> str`
Search for text with context snippets.

```python
"Search for 'function' in this code: [your code here]"
"Search for 'TODO' (case sensitive) in the text"
```

### Math Operations

#### `calculate(expression: str) -> str`
Safely evaluate mathematical expressions.

**Supported functions:** abs, round, min, max, sum, pow, sqrt, sin, cos, tan, log, log10, exp, pi, e

```python
"Calculate 2 + 2 * 3"
"Calculate sqrt(144)"
"Calculate sin(pi/2)"
"Calculate log10(1000)"
```

#### `add_numbers(a: float, b: float) -> str`
Add two numbers.

#### `multiply_numbers(a: float, b: float) -> str`
Multiply two numbers.

### Utilities

#### `get_greeting(name: str) -> str`
Generate a personalized greeting.

#### `get_current_time(timezone: str = "local") -> str`
Get current date and time.

```python
"What's the current time?"
```

## 🔍 Resources

### `server://info`
Get comprehensive server information, including all available tools and capabilities.

```python
"Show me information about the server capabilities"
```

## 📋 Prompts

### `code_review_prompt(code: str, language: str = "python")`
Generate a comprehensive code review template.

### `file_analysis_prompt(file_path: str)`
Generate a file analysis template.

## 🎯 Example Use Cases

### Organize a Messy Downloads Folder

```
Preview organization:
"Organize ~/Downloads by type with dry_run=true"

Apply changes:
"Organize ~/Downloads by type"
```

### Batch Text Replacement

```
"Update all TODO comments to DONE in ~/project/main.py"
```

### Find and Analyze Code Files

```
"Find all Python files in ~/projects/myapp"
"Read ~/projects/myapp/src/main.py"
"Count the words in the file"
```

### Create Project Structure

```
"Create directories at ~/projects/new-app/src, ~/projects/new-app/tests, ~/projects/new-app/docs"
"Write a README.md template to ~/projects/new-app/README.md"
```

### File Organization Workflow

```
1. "List files in ~/Desktop with details"
2. "Organize ~/Desktop by type with dry_run=true" (preview)
3. "Organize ~/Desktop by type" (apply)
```

## 🔐 Security Considerations

### File System Access
- The server has access to your entire file system
- Always verify paths before operations
- Use `dry_run=true` for organize operations to preview changes
- The server respects file permissions and will report permission errors

### Network Deployment
- When using HTTP transport, consider:
  - Binding to `127.0.0.1` (localhost only) for local testing
  - Implementing authentication for production use
  - Using HTTPS in production environments
  - Restricting access with firewall rules

### Calculator Safety
- The `calculate()` function uses a restricted environment
- Only mathematical functions are available (no file I/O, no system calls)
- Safe for evaluating user-provided expressions

## 🛠️ Development

### Project Structure

```
mcp-local/
├── main.py              # Main server code
├── README.md            # This file
├── pyproject.toml       # Project metadata and dependencies
└── .python-version      # Python version specification
```

### Running Tests

```bash
# Test individual tools
fastmcp dev main.py

# Use MCP Inspector for interactive testing
fastmcp dev main.py
```

### Adding New Tools

1. Add the tool function with `@mcp.tool()` decorator
2. Include proper docstring with Args and Returns
3. Add error handling
4. Update the `get_server_info()` resource
5. Test thoroughly

Example:

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """Description of what the tool does.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    """
    try:
        # Implementation
        return f"✓ Success: {result}"
    except Exception as e:
        return f"❌ Error: {e}"
```

## 📖 Resources

- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - feel free to use this project for any purpose.

## 🐛 Troubleshooting

### Server Won't Start

**Issue**: Port already in use
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>
```

**Issue**: Permission denied when accessing files
- Check file permissions: `ls -la <path>`
- Ensure the server has read/write access

### Claude Desktop Integration

**Issue**: Server not showing in Claude
1. Check config file path and syntax (valid JSON)
2. Ensure absolute paths are used
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

**Issue**: Tools not working
1. Verify the server is running: check for 🔌 icon
2. Try running the server manually to see errors
3. Check Python and uv versions

### Common Errors

**"File does not exist"**
- Verify the path is correct
- Use absolute paths or `~` for home directory
- Check for typos in the file name

**"Permission denied"**
- Check file/directory permissions
- Don't try to access system files without proper permissions
- On Windows, some system directories require admin access

## 💡 Tips

1. **Use Tab Completion**: In Claude, start typing a file path and it may suggest completions
2. **Preview Operations**: Use `dry_run=true` for organize operations
3. **Relative Paths**: The server resolves paths relative to where it's running
4. **Home Directory**: Use `~` for cross-platform home directory access
5. **Batch Operations**: Use `find_files()` to get a list, then operate on each file

## 🎓 Learning Resources

### FastMCP Basics
- Start with simple tools like `get_greeting()` and `add_numbers()`
- Explore file operations with safe test files
- Try the calculator with various expressions

### MCP Protocol
- Understand resources vs tools vs prompts
- Learn about different transport types
- Explore the MCP Inspector tool

### Best Practices
- Always handle errors gracefully
- Provide informative success/error messages
- Use type hints for better IDE support
- Write comprehensive docstrings

---

**Built with ❤️ using FastMCP**

For questions or support, please open an issue on GitHub.