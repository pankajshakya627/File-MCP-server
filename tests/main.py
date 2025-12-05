"""
FastMCP Server - Local Utils
A comprehensive MCP server using FastMCP with file operations, text processing, and utilities.

CUSTOM GPT INSTRUCTIONS:
You are a helpful assistant with access to a remote file management system.
You can read, write, edit, and organize files and directories using the provided tools.

**Important Rules:**
1.  **Creating Directories**: Always use the `create_directory` tool to create new folders before writing files into them if they don't exist.
2.  **Sandboxed Environment**: You are operating within a sandboxed directory. You cannot access files outside of this sandbox.
3.  **Path Handling**: You can use relative paths (e.g., "my_folder/file.txt") or absolute paths. The system handles them automatically.
4.  **Concurrency**: You can perform multiple file operations in parallel if needed.

**Capabilities:**
- Read files: `read_file`
- Write files: `write_file`
- Create folders: `create_directory`
- List files: `list_directory`
- Search text: `search_text`
- Organize folders: `organize_directory`
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from fastmcp import FastMCP
from starlette.responses import JSONResponse


# Initialize FastMCP server
# Initialize FastMCP server
mcp = FastMCP("Local Utils Server")

from file_utils import (
    read_file_core, write_file_core, append_to_file_core, update_file_core, delete_file_core,
    list_directory_core, find_files_core, create_directory_core, organize_directory_core,
    count_words_core, search_text_core, calculate_core
)

def _get_safe_path(path: str) -> Path:
    """Resolve path relative to sandbox directory."""
    import os
    import tempfile
    
    # Default to /tmp/Dev_Pankaj for cloud compatibility
    default_sandbox = os.path.join(tempfile.gettempdir(), "Dev_Pankaj")
    sandbox_dir = os.environ.get("SANDBOX_DIR", default_sandbox)
    base_dir = Path(sandbox_dir).resolve()
    
    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)
    
    # Treat all paths as relative to base_dir
    p = Path(path).expanduser()
    if p.is_absolute():
        # Strip root to make it relative
        p = Path(str(p).lstrip('/'))
        
    target = (base_dir / p).resolve()
    
    # Ensure we haven't escaped via '..'
    if not str(target).startswith(str(base_dir)):
        raise ValueError(f"Access denied: Path must be within {base_dir}")
        
    return target


# ============================================================================
# FILE OPERATIONS
# ============================================================================
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


@mcp.tool()
async def read_file(path: str) -> str:
    """Read and return the contents of a file.
    
    Args:
        path: Path to the file to read (supports ~ for home directory)
    
    Returns:
        File contents as string
    """
    return await read_file_core(path)


@mcp.tool()
async def write_file(path: str, content: str, overwrite: bool = True) -> str:
    """Write content to a file. Creates parent directories if needed.
    
    Args:
        path: Path to the file to write (supports ~ for home directory)
        content: Content to write to the file
        overwrite: If False, will not overwrite existing files (default: True)
    
    Returns:
        Success message with file info
    """
    return await write_file_core(path, content, overwrite)


@mcp.tool()
async def append_to_file(path: str, content: str) -> str:
    """Append content to the end of a file. Creates file if it doesn't exist.
    
    Args:
        path: Path to the file to append to
        content: Content to append
    
    Returns:
        Success message
    """
    return await append_to_file_core(path, content)


@mcp.tool()
async def update_file(path: str, old_text: str, new_text: str, count: int = -1) -> str:
    """Replace text in a file.
    
    Args:
        path: Path to the file to update
        old_text: Text to find and replace
        new_text: Replacement text
        count: Maximum number of replacements (-1 for all occurrences)
    
    Returns:
        Success message or error
    """
    return await update_file_core(path, old_text, new_text, count)


@mcp.tool()
async def delete_file(path: str) -> str:
    """Delete a file.
    
    Args:
        path: Path to the file to delete
    
    Returns:
        Success message or error
    """
    return await delete_file_core(path)


# ============================================================================
# DIRECTORY OPERATIONS
# ============================================================================


@mcp.tool()
async def list_directory(path: str = ".", show_hidden: bool = False, detailed: bool = False) -> str:
    """List files and directories in a given path.
    
    Args:
        path: Directory path to list (supports ~ for home directory)
        show_hidden: Include hidden files (starting with .)
        detailed: Show detailed information (size, modified date)
    
    Returns:
        Formatted list of items
    """
    return await list_directory_core(path, show_hidden, detailed)


@mcp.tool()
async def find_files(
    directory: str = ".", 
    pattern: str = "*", 
    recursive: bool = True,
    max_results: int = 100
) -> str:
    """Find files matching a pattern in a directory.
    
    Args:
        directory: Directory to search in (supports ~ for home directory)
        pattern: File pattern to match (e.g., '*.py', '*.txt', 'test*')
        recursive: If True, search recursively through subdirectories
        max_results: Maximum number of results to return
    
    Returns:
        List of matching files (one per line)
    """
    return await find_files_core(directory, pattern, recursive, max_results)


@mcp.tool()
async def create_directory(path: str, parents: bool = True) -> str:
    """Create a new directory.
    
    Args:
        path: Path to the directory to create
        parents: If True, create parent directories as needed
    
    Returns:
        Success message or error
    """
    return await create_directory_core(path, parents)


@mcp.tool()
async def organize_directory(directory: str = ".", by: str = "type", dry_run: bool = False) -> str:
    """Organize a directory by moving files into subdirectories.
    
    Args:
        directory: Directory to organize (supports ~ for home directory)
        by: Organization method - 'type', 'date', or 'size'
        dry_run: If True, show what would be done without actually moving files
    
    Returns:
        Summary of organization performed
    """
    return await organize_directory_core(directory, by, dry_run)


# ============================================================================
# TEXT PROCESSING
# ============================================================================


@mcp.tool()
async def count_words(text: str) -> str:
    """Count words, characters, and lines in a text string.
    
    Args:
        text: Text to analyze
    
    Returns:
        Statistics about the text
    """
    return await count_words_core(text)


@mcp.tool()
async def search_text(text: str, query: str, case_sensitive: bool = False) -> str:
    """Search for occurrences of a query string in text.
    
    Args:
        text: Text to search in
        query: String to search for
        case_sensitive: If True, perform case-sensitive search
    
    Returns:
        Number of matches and context around each match
    """
    return await search_text_core(text, query, case_sensitive)


# ============================================================================
# MATH OPERATIONS
# ============================================================================


@mcp.tool()
async def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")
    
    Returns:
        Result of the calculation
    """
    return await calculate_core(expression)


@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    return f"🔢 {a} + {b} = {result}"


@mcp.tool()
async def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers together."""
    result = a * b
    return f"🔢 {a} × {b} = {result}"


# ============================================================================
# UTILITY TOOLS
# ============================================================================


@mcp.tool()
async def get_greeting(name: str) -> str:
    """Generate a personalized greeting."""
    return f"👋 Hello, {name}! Welcome to the Local Utils MCP server."


@mcp.tool()
async def get_current_time(timezone: str = "local") -> str:
    """Get the current date and time.
    
    Args:
        timezone: Timezone (currently only 'local' is supported)
    
    Returns:
        Current date and time
    """
    now = datetime.now()
    return f"🕐 {now.strftime('%Y-%m-%d %H:%M:%S %A')}"


# ============================================================================
# RESOURCES
# ============================================================================


@mcp.resource("server://info")
async def get_server_info() -> str:
    """Return server information and available tools."""
    return json.dumps(
        {
            "name": "Local Utils Server",
            "version": "2.0.0",
            "description": "Comprehensive file operations, text processing, and utilities",
            "categories": {
                "File Operations": [
                    "read_file - Read file contents",
                    "write_file - Write content to a file",
                    "append_to_file - Append to a file",
                    "update_file - Replace text in a file",
                    "delete_file - Delete a file",
                ],
                "Directory Operations": [
                    "list_directory - List directory contents",
                    "find_files - Find files matching a pattern",
                    "create_directory - Create a new directory",
                    "organize_directory - Organize files by type/date/size",
                ],
                "Text Processing": [
                    "count_words - Analyze text statistics",
                    "search_text - Search for text with context",
                ],
                "Math Operations": [
                    "calculate - Evaluate mathematical expressions",
                    "add_numbers - Add two numbers",
                    "multiply_numbers - Multiply two numbers",
                ],
                "Utilities": [
                    "get_greeting - Generate a personalized greeting",
                    "get_current_time - Get current date and time",
                ],
            },
        },
        indent=2,
    )


@mcp.resource("server://tools")
async def get_tools_info() -> str:
    """Return detailed information about all available tools."""
    tools_info = {
        "file_operations": {
            "read_file": {
                "description": "Read and return the contents of a file",
                "parameters": {"path": "Path to file (supports ~ for home directory)"},
                "returns": "File contents with metadata"
            },
            "write_file": {
                "description": "Write content to a file, creates if doesn't exist",
                "parameters": {
                    "path": "Path to file",
                    "content": "Content to write"
                },
                "returns": "Success message with file info"
            },
            "append_to_file": {
                "description": "Append content to end of a file",
                "parameters": {
                    "path": "Path to file",
                    "content": "Content to append"
                },
                "returns": "Success message"
            },
            "update_file": {
                "description": "Find and replace text in a file",
                "parameters": {
                    "path": "Path to file",
                    "old_text": "Text to find",
                    "new_text": "Replacement text"
                },
                "returns": "Success message with count of replacements"
            },
            "delete_file": {
                "description": "Delete a file permanently",
                "parameters": {"path": "Path to file"},
                "returns": "Confirmation message"
            }
        },
        "directory_operations": {
            "list_directory": {
                "description": "List files and directories in a path",
                "parameters": {"path": "Directory path (default: current)"},
                "returns": "List of files/folders with type indicators"
            },
            "find_files": {
                "description": "Search for files matching a pattern",
                "parameters": {
                    "directory": "Directory to search",
                    "pattern": "Glob pattern (e.g., *.py)",
                    "recursive": "Search subdirectories (default: true)"
                },
                "returns": "List of matching files"
            },
            "create_directory": {
                "description": "Create a new directory",
                "parameters": {
                    "path": "Path to create",
                    "parents": "Create parent dirs (default: true)"
                },
                "returns": "Success message"
            },
            "organize_directory": {
                "description": "Organize files by type, date, or size",
                "parameters": {
                    "directory": "Directory to organize",
                    "by": "Method: 'type', 'date', or 'size'"
                },
                "returns": "Summary of organization performed"
            }
        },
        "text_processing": {
            "count_words": {
                "description": "Count words in text",
                "parameters": {"text": "Text to analyze"},
                "returns": "Word count and statistics"
            },
            "search_text": {
                "description": "Search for text with context",
                "parameters": {
                    "text": "Text to search in",
                    "query": "Text to find",
                    "context_lines": "Lines before/after match (default: 1)"
                },
                "returns": "Matches with surrounding context"
            }
        },
        "math_operations": {
            "add_numbers": {
                "description": "Add two numbers",
                "parameters": {"a": "First number", "b": "Second number"},
                "returns": "Sum"
            },
            "multiply_numbers": {
                "description": "Multiply two numbers",
                "parameters": {"a": "First number", "b": "Second number"},
                "returns": "Product"
            },
            "calculate": {
                "description": "Evaluate mathematical expressions",
                "parameters": {"expression": "Math expression (e.g., '2 + 3 * 4')"},
                "returns": "Result of calculation"
            }
        },
        "utilities": {
            "get_greeting": {
                "description": "Generate a personalized greeting",
                "parameters": {"name": "Person's name"},
                "returns": "Greeting message"
            },
            "get_current_time": {
                "description": "Get current date and time",
                "parameters": {},
                "returns": "Current date/time with timezone"
            }
        }
    }
    return json.dumps(tools_info, indent=2)


@mcp.resource("server://usage")
async def get_usage_guide() -> str:
    """Return usage guide and best practices for the MCP server."""
    guide = {
        "quick_start": {
            "description": "Get started with the MCP server",
            "steps": [
                "1. Start server: uv run main.py",
                "2. Call tools via JSON-RPC 2.0",
                "3. Use with Claude or other MCP clients"
            ]
        },
        "file_operations_tips": [
            "Always use absolute paths or ~ for home directory",
            "Check file exists before reading",
            "Create parent directories automatically with write_file",
            "Use find_files with patterns like *.py, *.txt"
        ],
        "error_handling": {
            "file_not_found": "Check path exists and is accessible",
            "permission_denied": "Verify file permissions",
            "unsupported_encoding": "File may be binary, use base64 encoding"
        },
        "best_practices": [
            "Organize large directories by type/date/size",
            "Use search_text with context for code analysis",
            "Always validate file paths before operations",
            "Use recursive=true for thorough file searches"
        ],
        "examples": {
            "read_file": "read_file('/path/to/file.txt')",
            "find_python_files": "find_files('.', '*.py', true)",
            "organize_downloads": "organize_directory('~/Downloads', 'type')",
            "add_numbers": "add_numbers(10, 20)"
        }
    }
    return json.dumps(guide, indent=2)


@mcp.resource("server://status")
async def get_server_status() -> str:
    """Return current server status and capabilities."""
    status = {
        "status": "operational",
        "version": "2.0.0",
        "uptime": "running",
        "capabilities": {
            "file_operations": True,
            "directory_operations": True,
            "text_processing": True,
            "math_operations": True,
            "utilities": True
        },
        "supported_transports": [
            "stdio (JSON-RPC 2.0 over stdin/stdout)",
            "HTTP Streamable (POST /mcp endpoint)"
        ],
        "resources": {
            "server://info": "Server metadata and tool categories",
            "server://tools": "Detailed tool reference",
            "server://usage": "Usage guide and examples",
            "server://status": "Server status and capabilities"
        },
        "python_version": sys.version.split()[0],
        "fastmcp_version": "2.13.0.2"
    }
    return json.dumps(status, indent=2)


# ============================================================================
# PROMPTS
# ============================================================================


@mcp.prompt()
def code_review_prompt(code: str, language: str = "python") -> str:
    """Generate a code review prompt for a given code snippet."""
    return f"""Please review the following {language} code:

```{language}
{code}
```

Provide feedback on:
1. Code quality and readability
2. Potential bugs or issues
3. Performance considerations
4. Best practices and idioms
5. Security concerns (if applicable)
6. Suggestions for improvement
"""


@mcp.prompt()
def file_analysis_prompt(file_path: str) -> str:
    """Generate a prompt to analyze a file."""
    return f"""Please analyze the file at: {file_path}

Provide insights on:
1. File type and purpose
2. Structure and organization
3. Key contents or patterns
4. Potential issues or improvements
5. Suggestions for better organization
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


if __name__ == "__main__":
    # mcp.run()
    mcp.run(
    transport="http",
    host="0.0.0.0",
    port=8000,
)
