FROM python:3.11-slim

# 1. Basic setup
WORKDIR /app

# 2. Copy your server code
COPY rest_api.py /app/rest_api.py
COPY file_utils.py /app/file_utils.py

# 3. Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic aiofiles

# 4. Create sandbox directory and set permissions
RUN mkdir -p /app/Dev_Pankaj && chmod 777 /app/Dev_Pankaj

# 5. Expose the HTTP port
EXPOSE 8011

# 6. Run the server
CMD ["uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "8011"]