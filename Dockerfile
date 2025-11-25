FROM python:3.11-slim

# 1. Basic setup
WORKDIR /app

# 2. Copy your server code
COPY main.py /app/main.py

# If you have other modules, copy them too:
# COPY . /app

# 3. Install dependencies (adjust if you have a pyproject/requirements)
RUN pip install --no-cache-dir fastmcp aiofiles

# 4. Create sandbox directory and set permissions
RUN mkdir -p /app/Dev_Pankaj && chmod 777 /app/Dev_Pankaj

# 5. Expose the MCP HTTP port
EXPOSE 8000

# 6. Run the server
CMD ["python", "main.py"]