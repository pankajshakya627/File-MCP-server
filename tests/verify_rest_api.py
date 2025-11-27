
import requests
import time
import subprocess
import sys
import os

def verify_rest_api():
    print("Starting REST API verification...")
    
    # Start the server in the background
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "rest_api:app", "--port", "8000"],
        cwd="/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        base_url = "http://localhost:8000"
        
        # 1. Test Health/Docs (implicit check if server is up)
        try:
            resp = requests.get(f"{base_url}/docs")
            if resp.status_code == 200:
                print("✅ Server is running (Docs accessible)")
            else:
                print(f"❌ Server returned {resp.status_code} for /docs")
                return
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server")
            return

        # 2. Test Create Directory
        print("\nTesting create_directory...")
        resp = requests.post(f"{base_url}/create_directory", json={"path": "api_test_dir"})
        print(f"Response: {resp.json()}")
        if resp.status_code == 200 and "Created directory" in resp.json():
            print("✅ create_directory success")
        else:
            print("❌ create_directory failed")

        # 3. Test Write File
        print("\nTesting write_file...")
        resp = requests.post(f"{base_url}/write_file", json={
            "path": "api_test_dir/test.txt",
            "content": "Hello from REST API!"
        })
        print(f"Response: {resp.json()}")
        if resp.status_code == 200 and "Successfully wrote" in resp.json():
            print("✅ write_file success")
        else:
            print("❌ write_file failed")

        # 4. Test Read File
        print("\nTesting read_file...")
        resp = requests.post(f"{base_url}/read_file", json={"path": "api_test_dir/test.txt"})
        print(f"Response: {resp.json()}")
        if resp.status_code == 200 and "Hello from REST API!" in resp.json():
            print("✅ read_file success")
        else:
            print("❌ read_file failed")
            
    finally:
        print("\nStopping server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    verify_rest_api()
