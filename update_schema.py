import json
import sys
import os
import argparse

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def update_schema(url):
    # Set environment variable before importing app
    os.environ["SERVER_URL"] = url
    
    # Import app after setting env var
    from rest_api import app
    
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.json")
    with open(output_file, "w") as f:
        json.dump(app.openapi(), f, indent=2)
    
    print(f"✅ openapi.json updated with server URL: {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update openapi.json with a new server URL")
    parser.add_argument("url", help="The new server URL (e.g., https://your-ngrok-url.ngrok-free.dev)")
    args = parser.parse_args()
    
    update_schema(args.url)
