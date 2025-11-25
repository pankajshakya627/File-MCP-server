
import asyncio
import time
from pathlib import Path
import sys

# Add the directory containing local_main_mcp.py to the path
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")

from local_main_mcp import count_words, calculate, search_text

async def test_concurrency():
    print("Starting concurrency test...")
    
    # Create a large text for testing
    large_text = "word " * 1000000
    
    start_time = time.time()
    
    # Run multiple heavy operations concurrently
    tasks = [
        count_words.fn(large_text),
        calculate.fn("sum(range(10000000))"),
        search_text.fn(large_text, "word"),
        asyncio.sleep(0.1) # This should not be blocked
    ]
    
    print("Tasks created, awaiting...")
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Total duration: {duration:.2f} seconds")
    print("Results:")
    for i, result in enumerate(results):
        print(f"Task {i}: {str(result)[:50]}...")

    print("\nTest passed if the total duration is reasonable and all tasks completed.")

if __name__ == "__main__":
    asyncio.run(test_concurrency())
