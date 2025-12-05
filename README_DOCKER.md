# Running REST API via Docker

This setup allows you to run the `rest_api.py` as a Docker container, exposing it on port 8000. This is useful for exposing the API via ngrok for ChatGPT Actions.

## Prerequisites

- Docker installed
- ngrok installed (optional, for external access)

## Quick Start

1.  **Update Server URL (if needed)**
    If your ngrok URL has changed, update the `openapi.json` schema:
    ```bash
    # Using uv/venv
    ./.venv/bin/python update_schema.py https://your-new-url.ngrok-free.dev
    ```

2.  **Build and Run Docker Container**
    ```bash
    ./docker_run.sh
    ```
    Or manually:
    ```bash
    docker build -t mcp-rest-api .
    docker run -p 8000:8000 --env SERVER_URL="https://your-url.ngrok-free.dev" mcp-rest-api
    ```

3.  **Verify**
    Access `http://localhost:8000/docs` to see the Swagger UI.

## Files

- `Dockerfile`: Configured to run `rest_api.py` with `uvicorn`.
- `rest_api.py`: The FastAPI application.
- `file_utils.py`: Core logic for file operations.
- `update_schema.py`: Script to regenerate `openapi.json`.
- `docker_run.sh`: Helper script to build and run.
