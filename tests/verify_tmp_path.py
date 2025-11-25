
import asyncio
import sys
import os
from pathlib import Path
import shutil
import tempfile

# Add the directory containing local_main_mcp.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

from local_main_mcp import write_file

async def test_tmp_path():
    print("Starting verification with default /tmp path...")
    
    # Clean up if exists
    tmp_sandbox = Path(tempfile.gettempdir()) / "Dev_Pankaj"
    if tmp_sandbox.exists():
        shutil.rmtree(tmp_sandbox)
    
    print(f"\nExpected sandbox location: {tmp_sandbox}")
    
    print("\nTest 1: Write to 'test_tmp.txt'")
    res = await write_file.fn("test_tmp.txt", "Cloud Compatible Content")
    print(f"Result: {res}")
    
    expected_path = tmp_sandbox / "test_tmp.txt"
    if expected_path.exists():
        print(f"✅ Success: File created at {expected_path}")
        with open(expected_path, 'r') as f:
            content = f.read()
            print(f"   Content: {content}")
    else:
        print(f"❌ Failure: File not found at {expected_path}")
    
    print("\nTest 2: Write to absolute path '/data/test.txt'")
    res = await write_file.fn("/data/test.txt", "Absolute Path Test")
    print(f"Result: {res}")
    
    expected_abs = tmp_sandbox / "data/test.txt"
    if expected_abs.exists():
        print(f"✅ Success: File redirected to {expected_abs}")
    else:
        print(f"❌ Failure: File not found at {expected_abs}")
    
    print(f"\n📁 Sandbox directory contents:")
    if tmp_sandbox.exists():
        for item in tmp_sandbox.rglob("*"):
            print(f"   {item.relative_to(tmp_sandbox)}")

if __name__ == "__main__":
    asyncio.run(test_tmp_path())
