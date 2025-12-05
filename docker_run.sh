#!/bin/bash

# Build the image
echo "🔨 Building Docker image..."
docker build --no-cache -t mcp-rest-api /Volumes/CrucialX9_MAC/Local_MCPs/mcp-local

# Run the container
echo "🚀 Running Docker container on port 8000..."
docker run -p 8000:8000 --env SERVER_URL="${SERVER_URL:-https://unmissed-heide-pseudogentlemanly.ngrok-free.dev}" mcp-rest-api uvicorn rest_api:app --host 0.0.0.0 --port 8000
