
import asyncio
import sys
import os
from pathlib import Path
import shutil

# Add the directory containing local_main_mcp.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

# Set env var before importing
custom_sandbox = "Custom_Sandbox_Test"
os.environ["SANDBOX_DIR"] = custom_sandbox

from local_main_mcp import write_file

async def test_env_var():
    print(f"Starting verification with SANDBOX_DIR={custom_sandbox}...")
    
    # Clean up if exists
    sandbox_dir = Path(custom_sandbox).resolve()
    if sandbox_dir.exists():
        shutil.rmtree(sandbox_dir)
    
    print("\nTest: Write to 'test_env.txt'")
    res = await write_file.fn("test_env.txt", "Env Var Content")
    print(f"Result: {res}")
    
    expected_path = sandbox_dir / "test_env.txt"
    if expected_path.exists():
        print(f"✅ Success: File created at {expected_path}")
    else:
        print(f"❌ Failure: File not found at {expected_path}")
        # Check if it went to default
        default_path = Path("Dev_Pankaj").resolve() / "test_env.txt"
        if default_path.exists():
             print(f"❌ Failure: File went to default Dev_Pankaj instead: {default_path}")

if __name__ == "__main__":
    asyncio.run(test_env_var())
