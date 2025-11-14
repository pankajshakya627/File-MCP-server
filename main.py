"""
FastMCP Server - Local Utils
A comprehensive MCP server using FastMCP with file operations, text processing, and utilities.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Local Utils Server")


# ============================================================================
# FILE OPERATIONS
# ============================================================================


@mcp.tool()
def read_file(path: str) -> str:
    """Read and return the contents of a file.
    
    Args:
        path: Path to the file to read (supports ~ for home directory)
    
    Returns:
        File contents as string
    """
    try:
        file_path = Path(path).expanduser().resolve()
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        if not file_path.is_file():
            return f"❌ Error: Path is not a file: {path}"
        
        content = file_path.read_text(encoding='utf-8')
        size = len(content)
        lines = content.count('\n') + 1
        
        return f"✓ Read {file_path}\n  Size: {size} bytes, {lines} lines\n\n{content}"
    except UnicodeDecodeError:
        return f"❌ Error: File is not a text file or uses unsupported encoding: {path}"
    except PermissionError:
        return f"❌ Error: Permission denied: {path}"
    except Exception as e:
        return f"❌ Error reading file: {type(e).__name__}: {e}"


@mcp.tool()
def write_file(path: str, content: str, overwrite: bool = True) -> str:
    """Write content to a file. Creates parent directories if needed.
    
    Args:
        path: Path to the file to write (supports ~ for home directory)
        content: Content to write to the file
        overwrite: If False, will not overwrite existing files (default: True)
    
    Returns:
        Success message with file info
    """
    try:
        file_path = Path(path).expanduser().resolve()
        
        if file_path.exists() and not overwrite:
            return f"❌ Error: File already exists (use overwrite=true to replace): {path}"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        
        size = len(content)
        lines = content.count('\n') + 1
        
        return f"✓ Successfully wrote to {file_path}\n  Size: {size} bytes, {lines} lines"
    except PermissionError:
        return f"❌ Error: Permission denied: {path}"
    except Exception as e:
        return f"❌ Error writing file: {type(e).__name__}: {e}"


@mcp.tool()
def append_to_file(path: str, content: str) -> str:
    """Append content to the end of a file. Creates file if it doesn't exist.
    
    Args:
        path: Path to the file to append to
        content: Content to append
    
    Returns:
        Success message
    """
    try:
        file_path = Path(path).expanduser().resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return f"✓ Appended {len(content)} bytes to {file_path}"
    except Exception as e:
        return f"❌ Error appending to file: {type(e).__name__}: {e}"


@mcp.tool()
def update_file(path: str, old_text: str, new_text: str, count: int = -1) -> str:
    """Replace text in a file.
    
    Args:
        path: Path to the file to update
        old_text: Text to find and replace
        new_text: Replacement text
        count: Maximum number of replacements (-1 for all occurrences)
    
    Returns:
        Success message or error
    """
    try:
        file_path = Path(path).expanduser().resolve()
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        
        content = file_path.read_text(encoding='utf-8')
        
        if old_text not in content:
            return f"❌ Error: Text not found in file: '{old_text[:50]}...'" if len(old_text) > 50 else f"❌ Error: Text not found in file: '{old_text}'"
        
        occurrences = content.count(old_text)
        updated_content = content.replace(old_text, new_text, count)
        file_path.write_text(updated_content, encoding='utf-8')
        
        replaced = occurrences if count == -1 else min(count, occurrences)
        return f"✓ Updated {file_path}\n  Replaced {replaced} occurrence(s)"
    except Exception as e:
        return f"❌ Error updating file: {type(e).__name__}: {e}"


@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file.
    
    Args:
        path: Path to the file to delete
    
    Returns:
        Success message or error
    """
    try:
        file_path = Path(path).expanduser().resolve()
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        if not file_path.is_file():
            return f"❌ Error: Path is not a file: {path}"
        
        file_path.unlink()
        return f"✓ Deleted file: {file_path}"
    except Exception as e:
        return f"❌ Error deleting file: {type(e).__name__}: {e}"


# ============================================================================
# DIRECTORY OPERATIONS
# ============================================================================


@mcp.tool()
def list_directory(path: str = ".", show_hidden: bool = False, detailed: bool = False) -> str:
    """List files and directories in a given path.
    
    Args:
        path: Directory path to list (supports ~ for home directory)
        show_hidden: Include hidden files (starting with .)
        detailed: Show detailed information (size, modified date)
    
    Returns:
        Formatted list of items
    """
    try:
        dir_path = Path(path).expanduser().resolve()
        
        if not dir_path.exists():
            return f"❌ Error: Path does not exist: {path}"
        if not dir_path.is_dir():
            return f"❌ Error: Not a directory: {path}"
        
        items = list(dir_path.iterdir())
        
        if not show_hidden:
            items = [item for item in items if not item.name.startswith('.')]
        
        items = sorted(items, key=lambda x: (not x.is_dir(), x.name.lower()))
        
        if not items:
            return f"📁 {dir_path}\n  (empty directory)"
        
        result = [f"📁 {dir_path}\n"]
        
        for item in items:
            if detailed:
                size = item.stat().st_size if item.is_file() else 0
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                size_str = format_file_size(size) if item.is_file() else ""
                date_str = mtime.strftime('%Y-%m-%d %H:%M')
                result.append(
                    f"  {'📂' if item.is_dir() else '📄'} {item.name:<40} {size_str:>10} {date_str}"
                )
            else:
                result.append(f"  {'📂' if item.is_dir() else '📄'} {item.name}")
        
        return "\n".join(result)
    except PermissionError:
        return f"❌ Error: Permission denied: {path}"
    except Exception as e:
        return f"❌ Error listing directory: {type(e).__name__}: {e}"


@mcp.tool()
def find_files(
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
    try:
        dir_path = Path(directory).expanduser().resolve()
        
        if not dir_path.exists():
            return f"❌ Error: Directory does not exist: {directory}"
        if not dir_path.is_dir():
            return f"❌ Error: Not a directory: {directory}"
        
        if recursive:
            matches = list(dir_path.glob(f"**/{pattern}"))
        else:
            matches = list(dir_path.glob(pattern))
        
        # Filter out directories, keep only files
        matches = [m for m in matches if m.is_file()]
        matches = sorted(matches)[:max_results]
        
        if not matches:
            return f"🔍 No files matching pattern '{pattern}' in {directory}"
        
        result = [f"🔍 Found {len(matches)} file(s) matching '{pattern}':\n"]
        
        for match in matches:
            try:
                rel_path = match.relative_to(dir_path)
                size = format_file_size(match.stat().st_size)
                result.append(f"  📄 {rel_path} ({size})")
            except ValueError:
                result.append(f"  📄 {match}")
        
        if len(matches) == max_results:
            result.append(f"\n⚠️  Results limited to {max_results} files")
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error finding files: {type(e).__name__}: {e}"


@mcp.tool()
def create_directory(path: str, parents: bool = True) -> str:
    """Create a new directory.
    
    Args:
        path: Path to the directory to create
        parents: If True, create parent directories as needed
    
    Returns:
        Success message or error
    """
    try:
        dir_path = Path(path).expanduser().resolve()
        
        if dir_path.exists():
            return f"❌ Error: Path already exists: {path}"
        
        dir_path.mkdir(parents=parents, exist_ok=False)
        return f"✓ Created directory: {dir_path}"
    except Exception as e:
        return f"❌ Error creating directory: {type(e).__name__}: {e}"


@mcp.tool()
def organize_directory(directory: str = ".", by: str = "type", dry_run: bool = False) -> str:
    """Organize a directory by moving files into subdirectories.
    
    Args:
        directory: Directory to organize (supports ~ for home directory)
        by: Organization method - 'type', 'date', or 'size'
        dry_run: If True, show what would be done without actually moving files
    
    Returns:
        Summary of organization performed
    """
    try:
        dir_path = Path(directory).expanduser().resolve()
        
        if not dir_path.is_dir():
            return f"❌ Error: Not a directory: {directory}"
        
        # Define file type categories
        type_categories = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.csv', '.ppt', '.pptx', '.odt', '.rtf'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            'Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.html', '.css', '.json', '.yaml', '.yml', '.xml', '.md', '.sh', '.bat', '.swift', '.kt', '.scala', '.ipynb'],
            'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'],
            'Executables': ['.exe', '.app', '.dmg', '.deb', '.rpm', '.msi'],
        }
        
        moved_count = 0
        summary = []
        
        # Get all files (excluding directories)
        items = [item for item in dir_path.iterdir() if item.is_file()]
        
        if not items:
            return f"📁 {dir_path}\n  (no files to organize)"
        
        if by == 'type':
            for item in items:
                suffix = item.suffix.lower()
                category = 'Other'
                
                for cat, exts in type_categories.items():
                    if suffix in exts:
                        category = cat
                        break
                
                target_dir = dir_path / category
                target_file = target_dir / item.name
                
                # Handle name conflicts
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1
                
                if not dry_run:
                    target_dir.mkdir(exist_ok=True)
                    item.rename(target_file)
                
                moved_count += 1
                summary.append(f"  {item.name} → {category}/")
        
        elif by == 'date':
            for item in items:
                mtime = item.stat().st_mtime
                date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m')
                
                target_dir = dir_path / date_str
                target_file = target_dir / item.name
                
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1
                
                if not dry_run:
                    target_dir.mkdir(exist_ok=True)
                    item.rename(target_file)
                
                moved_count += 1
                summary.append(f"  {item.name} → {date_str}/")
        
        elif by == 'size':
            for item in items:
                size_bytes = item.stat().st_size
                
                if size_bytes < 1_000_000:  # < 1 MB
                    category = 'Small'
                elif size_bytes < 100_000_000:  # < 100 MB
                    category = 'Medium'
                else:
                    category = 'Large'
                
                target_dir = dir_path / category
                target_file = target_dir / item.name
                
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1
                
                if not dry_run:
                    target_dir.mkdir(exist_ok=True)
                    item.rename(target_file)
                
                moved_count += 1
                summary.append(f"  {item.name} → {category}/")
        
        else:
            return f"❌ Error: Unknown organization method '{by}'. Use 'type', 'date', or 'size'."
        
        mode = "🔍 DRY RUN - Would organize" if dry_run else "✓ Organized"
        result = [f"{mode} directory by {by}"]
        result.append(f"  Files processed: {moved_count}\n")
        
        if summary and len(summary) <= 30:
            result.extend(summary)
        else:
            result.extend(summary[:30])
            result.append(f"\n  ... and {len(summary) - 30} more files")
        
        if dry_run:
            result.append("\n💡 Run with dry_run=false to actually move files")
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error organizing directory: {type(e).__name__}: {e}"


# ============================================================================
# TEXT PROCESSING
# ============================================================================


@mcp.tool()
def count_words(text: str) -> str:
    """Count words, characters, and lines in a text string.
    
    Args:
        text: Text to analyze
    
    Returns:
        Statistics about the text
    """
    words = len(text.split())
    chars = len(text)
    chars_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    lines = text.count('\n') + 1
    
    return f"""📊 Text Statistics:
  Words: {words:,}
  Characters (with spaces): {chars:,}
  Characters (without spaces): {chars_no_spaces:,}
  Lines: {lines:,}"""


@mcp.tool()
def search_text(text: str, query: str, case_sensitive: bool = False) -> str:
    """Search for occurrences of a query string in text.
    
    Args:
        text: Text to search in
        query: String to search for
        case_sensitive: If True, perform case-sensitive search
    
    Returns:
        Number of matches and context around each match
    """
    search_text = text if case_sensitive else text.lower()
    search_query = query if case_sensitive else query.lower()
    
    count = search_text.count(search_query)
    
    if count == 0:
        return f"🔍 No matches found for '{query}'"
    
    # Find positions
    positions = []
    start = 0
    while True:
        pos = search_text.find(search_query, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    result = [f"🔍 Found {count} occurrence(s) of '{query}':\n"]
    
    for i, pos in enumerate(positions[:10], 1):  # Show first 10 matches
        # Get context (50 chars before and after)
        start = max(0, pos - 50)
        end = min(len(text), pos + len(query) + 50)
        context = text[start:end]
        
        result.append(f"  {i}. Position {pos}: ...{context}...")
    
    if len(positions) > 10:
        result.append(f"\n  ... and {len(positions) - 10} more occurrences")
    
    return "\n".join(result)


# ============================================================================
# MATH OPERATIONS
# ============================================================================


@mcp.tool()
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")
    
    Returns:
        Result of the calculation
    """
    try:
        # Safe mathematical functions
        import math
        safe_dict = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow,
            'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
            'tan': math.tan, 'log': math.log, 'log10': math.log10,
            'exp': math.exp, 'pi': math.pi, 'e': math.e,
        }
        
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"🔢 {expression} = {result}"
    except Exception as e:
        return f"❌ Error evaluating expression: {e}"


@mcp.tool()
def add_numbers(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    return f"🔢 {a} + {b} = {result}"


@mcp.tool()
def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers together."""
    result = a * b
    return f"🔢 {a} × {b} = {result}"


# ============================================================================
# UTILITY TOOLS
# ============================================================================


@mcp.tool()
def get_greeting(name: str) -> str:
    """Generate a personalized greeting."""
    return f"👋 Hello, {name}! Welcome to the Local Utils MCP server."


@mcp.tool()
def get_current_time(timezone: str = "local") -> str:
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
def get_server_info() -> str:
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
    mcp.run()