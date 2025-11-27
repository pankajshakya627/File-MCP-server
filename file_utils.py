
import os
import sys
import json
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
import aiofiles
import aiofiles.os

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_safe_path(path: str) -> Path:
    """Resolve path relative to sandbox directory."""
    
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

def format_file_size(size_in_bytes: int) -> str:
    """Format file size in bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} PB"

# ============================================================================
# CORE LOGIC
# ============================================================================

async def read_file_core(path: str) -> str:
    try:
        file_path = _get_safe_path(path)
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        if not file_path.is_file():
            return f"❌ Error: Path is not a file: {path}"
        
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
        size = len(content)
        lines = content.count('\n') + 1
        
        return f"✓ Read {file_path}\n  Size: {size} bytes, {lines} lines\n\n{content}"
    except UnicodeDecodeError:
        return f"❌ Error: File is not a text file or uses unsupported encoding: {path}"
    except PermissionError:
        return f"❌ Error: Permission denied: {path}"
    except Exception as e:
        return f"❌ Error reading file: {type(e).__name__}: {e}"

async def write_file_core(path: str, content: str, overwrite: bool = True) -> str:
    try:
        file_path = _get_safe_path(path)
        
        if file_path.exists() and not overwrite:
            return f"❌ Error: File already exists (use overwrite=true to replace): {path}"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
            await f.write(content)
        
        size = len(content)
        lines = content.count('\n') + 1
        
        return f"✓ Successfully wrote to {file_path}\n  Size: {size} bytes, {lines} lines"
    except PermissionError:
        return f"❌ Error: Permission denied: {path}"
    except Exception as e:
        return f"❌ Error writing file: {type(e).__name__}: {e}"

async def append_to_file_core(path: str, content: str) -> str:
    try:
        file_path = _get_safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, mode='a', encoding='utf-8') as f:
            await f.write(content)
        
        return f"✓ Appended {len(content)} bytes to {file_path}"
    except Exception as e:
        return f"❌ Error appending to file: {type(e).__name__}: {e}"

async def update_file_core(path: str, old_text: str, new_text: str, count: int = -1) -> str:
    try:
        file_path = _get_safe_path(path)
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
        
        if old_text not in content:
            return f"❌ Error: Text not found in file: '{old_text[:50]}...'" if len(old_text) > 50 else f"❌ Error: Text not found in file: '{old_text}'"
        
        occurrences = content.count(old_text)
        updated_content = content.replace(old_text, new_text, count)
        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
            await f.write(updated_content)
        
        replaced = occurrences if count == -1 else min(count, occurrences)
        return f"✓ Updated {file_path}\n  Replaced {replaced} occurrence(s)"
    except Exception as e:
        return f"❌ Error updating file: {type(e).__name__}: {e}"

async def delete_file_core(path: str) -> str:
    try:
        file_path = _get_safe_path(path)
        
        if not file_path.exists():
            return f"❌ Error: File does not exist: {path}"
        if not file_path.is_file():
            return f"❌ Error: Path is not a file: {path}"
        
        await aiofiles.os.remove(file_path)
        return f"✓ Deleted file: {file_path}"
    except Exception as e:
        return f"❌ Error deleting file: {type(e).__name__}: {e}"

async def list_directory_core(path: str = ".", show_hidden: bool = False, detailed: bool = False) -> str:
    try:
        dir_path = _get_safe_path(path)
        
        if not dir_path.exists():
            return f"❌ Error: Path does not exist: {path}"
        if not dir_path.is_dir():
            return f"❌ Error: Not a directory: {path}"
        
        items = await asyncio.to_thread(lambda: list(dir_path.iterdir()))
        
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

async def find_files_core(directory: str = ".", pattern: str = "*", recursive: bool = True, max_results: int = 100) -> str:
    try:
        dir_path = _get_safe_path(directory)
        
        if not dir_path.exists():
            return f"❌ Error: Directory does not exist: {directory}"
        if not dir_path.is_dir():
            return f"❌ Error: Not a directory: {directory}"
        
        if recursive:
            matches = await asyncio.to_thread(lambda: list(dir_path.glob(f"**/{pattern}")))
        else:
            matches = await asyncio.to_thread(lambda: list(dir_path.glob(pattern)))
        
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

async def create_directory_core(path: str, parents: bool = True) -> str:
    try:
        dir_path = _get_safe_path(path)
        
        if dir_path.exists():
            return f"❌ Error: Path already exists: {path}"
        
        await asyncio.to_thread(lambda: dir_path.mkdir(parents=parents, exist_ok=False))
        return f"✓ Created directory: {dir_path}"
    except Exception as e:
        return f"❌ Error creating directory: {type(e).__name__}: {e}"

async def organize_directory_core(directory: str = ".", by: str = "type", dry_run: bool = False) -> str:
    try:
        dir_path = _get_safe_path(directory)
        
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
        items = await asyncio.to_thread(lambda: [item for item in dir_path.iterdir() if item.is_file()])
        
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
                    await asyncio.to_thread(target_dir.mkdir, parents=True, exist_ok=True)
                    await asyncio.to_thread(item.rename, target_file)
                
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
                    await asyncio.to_thread(target_dir.mkdir, parents=True, exist_ok=True)
                    await asyncio.to_thread(item.rename, target_file)
                
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
                    await asyncio.to_thread(target_dir.mkdir, parents=True, exist_ok=True)
                    await asyncio.to_thread(item.rename, target_file)
                
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

async def count_words_core(text: str) -> str:
    def _count():
        words = len(text.split())
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        lines = text.count('\n') + 1
        return words, chars, chars_no_spaces, lines

    words, chars, chars_no_spaces, lines = await asyncio.to_thread(_count)
    
    return f"""📊 Text Statistics:
  Words: {words:,}
  Characters (with spaces): {chars:,}
  Characters (without spaces): {chars_no_spaces:,}
  Lines: {lines:,}"""

async def search_text_core(text: str, query: str, case_sensitive: bool = False) -> str:
    def _search():
        search_text_val = text if case_sensitive else text.lower()
        search_query_val = query if case_sensitive else query.lower()
        
        count = search_text_val.count(search_query_val)
        
        if count == 0:
            return f"🔍 No matches found for '{query}'"
        
        # Find positions
        positions = []
        start = 0
        while True:
            pos = search_text_val.find(search_query_val, start)
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

    return await asyncio.to_thread(_search)

async def calculate_core(expression: str) -> str:
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
        
        result = await asyncio.to_thread(eval, expression, {"__builtins__": {}}, safe_dict)
        return f"🔢 {expression} = {result}"
    except Exception as e:
        return f"❌ Error evaluating expression: {e}"
