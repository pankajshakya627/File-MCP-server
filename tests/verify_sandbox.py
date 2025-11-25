
import asyncio
import sys
from pathlib import Path
import shutil

# Add the directory containing local_main_mcp.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

from local_main_mcp import write_file, read_file

async def test_sandbox():
    print("Starting sandbox verification...")
    
    # Clean up Dev_Pankaj if it exists
    sandbox_dir = Path("Dev_Pankaj").resolve()
    if sandbox_dir.exists():
        shutil.rmtree(sandbox_dir)
    
    # Test 1: Write to relative path
    print("\nTest 1: Write to relative path 'test.txt'")
    res = await write_file.fn("test.txt", "Hello Sandbox")
    print(f"Result: {res}")
    
    expected_path = sandbox_dir / "test.txt"
    if expected_path.exists():
        print(f"✅ Success: File created at {expected_path}")
    else:
        print(f"❌ Failure: File not found at {expected_path}")

    # Test 2: Write to an absolute path
    print("\nTest 2: Write to absolute path '/tmp/should_be_sandboxed.txt'")
    res = await write_file.fn("/tmp/should_be_sandboxed.txt", "Sandboxed Content")
    print(f"Result: {res}")
    
    expected_abs_path = sandbox_dir / "tmp/should_be_sandboxed.txt"
    if expected_abs_path.exists():
        print(f"✅ Success: File redirected to {expected_abs_path}")
    else:
        print(f"❌ Failure: File not found at {expected_abs_path}")
        
    # Test 3: Attempt to escape sandbox
    print("\nTest 3: Attempt to escape via '..'")
    res = await write_file.fn("../outside_sandbox.txt", "Trying to escape")
    print(f"Result: {res}")
    
    # Check if it was blocked or sandboxed
    if "Access denied" in res or "Error" in res:
         print(f"✅ Success: Escape attempt blocked/handled: {res}")
    else:
         # If it succeeded, check where it went
         expected_escape_path = sandbox_dir / "outside_sandbox.txt"
         if expected_escape_path.exists():
             print(f"✅ Success: '..' path contained in {expected_escape_path}")
         else:
             print(f"❌ Failure: Operation succeeded but file location unknown or unsafe")

    print("\nTest 4: Explicit escape attempt")
    res = await write_file.fn("../truly_outside.txt", "Escape")
    print(f"Result: {res}")
    if "Access denied" in res:
        print(f"✅ Success: Escape attempt blocked as expected")
    else:
        print(f"❌ Failure: Escape attempt NOT blocked")

if __name__ == "__main__":
    asyncio.run(test_sandbox())
