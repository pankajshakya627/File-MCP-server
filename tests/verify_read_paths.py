
import asyncio
import sys
import os
from pathlib import Path
import shutil
import tempfile

# Add the directory containing local_main_mcp.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

from local_main_mcp import write_file, list_directory, read_file

async def test_read_paths():
    print("Starting verification for read path resolution...")
    
    # Clean up if exists
    tmp_sandbox = Path(tempfile.gettempdir()) / "Dev_Pankaj"
    if tmp_sandbox.exists():
        shutil.rmtree(tmp_sandbox)
    
    print(f"\nSandbox location: {tmp_sandbox}")
    
    # 1. Create a file in the sandbox
    print("\nStep 1: Creating 'read_test.txt' in sandbox")
    await write_file.fn("read_test.txt", "Content to read")
    
    # 2. List directory using "." (should resolve to sandbox root)
    print("\nStep 2: Listing directory '.'")
    listing = await list_directory.fn(".")
    print(f"Listing result:\n{listing}")
    
    if "read_test.txt" in listing:
        print("✅ Success: 'read_test.txt' found in listing of '.'")
    else:
        print("❌ Failure: 'read_test.txt' NOT found in listing of '.'")

    # 3. Read file using relative path
    print("\nStep 3: Reading 'read_test.txt'")
    content = await read_file.fn("read_test.txt")
    print(f"Read result: {content}")
    
    if "Content to read" in content:
        print("✅ Success: Content matched")
    else:
        print("❌ Failure: Content mismatch or error")

if __name__ == "__main__":
    asyncio.run(test_read_paths())
