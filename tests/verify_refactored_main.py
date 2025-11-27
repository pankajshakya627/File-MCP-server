
import asyncio
import sys
import os
import shutil
import tempfile
from pathlib import Path

# Add the directory containing main.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

from main import write_file, read_file, list_directory, create_directory

async def verify_main_mcp():
    print("Starting verification of refactored main.py...")
    
    # Clean up sandbox
    tmp_sandbox = Path(tempfile.gettempdir()) / "Dev_Pankaj"
    if tmp_sandbox.exists():
        shutil.rmtree(tmp_sandbox)
        
    print(f"Sandbox: {tmp_sandbox}")

    # 1. Test Create Directory
    print("\nStep 1: Testing create_directory tool")
    result = await create_directory.fn("refactor_test")
    print(f"Result: {result}")
    if "Created directory" in result:
        print("✅ create_directory success")
    else:
        print("❌ create_directory failed")

    # 2. Test Write File
    print("\nStep 2: Testing write_file tool")
    result = await write_file.fn("refactor_test/test.txt", "Content from main.py")
    print(f"Result: {result}")
    if "Successfully wrote" in result:
        print("✅ write_file success")
    else:
        print("❌ write_file failed")

    # 3. Test Read File
    print("\nStep 3: Testing read_file tool")
    result = await read_file.fn("refactor_test/test.txt")
    print(f"Result: {result}")
    if "Content from main.py" in result:
        print("✅ read_file success")
    else:
        print("❌ read_file failed")

    # 4. Test List Directory
    print("\nStep 4: Testing list_directory tool")
    result = await list_directory.fn("refactor_test")
    print(f"Result: {result}")
    if "test.txt" in result:
        print("✅ list_directory success")
    else:
        print("❌ list_directory failed")

if __name__ == "__main__":
    asyncio.run(verify_main_mcp())
