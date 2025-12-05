
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
import uvicorn
from file_utils import (
    read_file_core, write_file_core, append_to_file_core, update_file_core, delete_file_core,
    list_directory_core, find_files_core, create_directory_core, organize_directory_core,
    count_words_core, search_text_core, calculate_core
)
import os
import tempfile
from pathlib import Path

# Print configuration on startup
default_sandbox = os.path.join(tempfile.gettempdir(), "Dev_Pankaj")
sandbox_dir = os.environ.get("SANDBOX_DIR", default_sandbox)
server_url = os.environ.get("SERVER_URL", "https://unmissed-heide-pseudogentlemanly.ngrok-free.dev")

print(f"\n{'='*50}")
print(f"🚀 Server Configuration")
print(f"   SANDBOX_DIR: {sandbox_dir}")
print(f"   Absolute Path: {Path(sandbox_dir).resolve()}")
print(f"   SERVER_URL:  {server_url}")
print(f"{'='*50}\n")

app = FastAPI(
    title="File Management API",
    description="REST API for file management and utilities, compatible with ChatGPT Actions.",
    version="1.0.0",
    servers=[{"url": server_url, "description": "Production Server"}]
)

# ============================================================================
# MODELS
# ============================================================================

class ReadFileRequest(BaseModel):
    path: str = Field(..., description="Path to the file to read")

class WriteFileRequest(BaseModel):
    path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write")
    overwrite: bool = Field(True, description="Overwrite existing file")

class AppendFileRequest(BaseModel):
    path: str = Field(..., description="Path to the file to append to")
    content: str = Field(..., description="Content to append")

class UpdateFileRequest(BaseModel):
    path: str = Field(..., description="Path to the file to update")
    old_text: str = Field(..., description="Text to find")
    new_text: str = Field(..., description="Replacement text")
    count: int = Field(-1, description="Max replacements (-1 for all)")

class DeleteFileRequest(BaseModel):
    path: str = Field(..., description="Path to the file to delete")

class ListDirectoryRequest(BaseModel):
    path: str = Field(".", description="Directory path")
    show_hidden: bool = Field(False, description="Show hidden files")
    detailed: bool = Field(False, description="Show detailed info")

class FindFilesRequest(BaseModel):
    directory: str = Field(".", description="Directory to search")
    pattern: str = Field("*", description="Glob pattern")
    recursive: bool = Field(True, description="Recursive search")
    max_results: int = Field(100, description="Max results")

class CreateDirectoryRequest(BaseModel):
    path: str = Field(..., description="Directory path to create")
    parents: bool = Field(True, description="Create parent directories")

class OrganizeDirectoryRequest(BaseModel):
    directory: str = Field(".", description="Directory to organize")
    by: str = Field("type", description="Method: type, date, size")
    dry_run: bool = Field(False, description="Simulate only")

class CountWordsRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")

class SearchTextRequest(BaseModel):
    text: str = Field(..., description="Text to search in")
    query: str = Field(..., description="Query string")
    case_sensitive: bool = Field(False, description="Case sensitive search")

class CalculateRequest(BaseModel):
    expression: str = Field(..., description="Math expression to evaluate")

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", summary="Root")
async def root():
    return {
        "message": "File Management API is running",
        "docs_url": "/docs",
        "health_url": "/health"
    }

@app.get("/health", summary="Health Check")
async def health():
    return {"status": "healthy"}

@app.get("/debug/config", summary="Debug Config")
async def debug_config():
    import os
    import tempfile
    default_sandbox = os.path.join(tempfile.gettempdir(), "Dev_Pankaj")
    sandbox_dir = os.environ.get("SANDBOX_DIR", default_sandbox)
    return {
        "sandbox_dir": sandbox_dir,
        "absolute_sandbox_path": str(Path(sandbox_dir).resolve())
    }

@app.post("/read_file", summary="Read a file")
async def read_file(request: ReadFileRequest):
    return await read_file_core(request.path)

@app.post("/write_file", summary="Write to a file")
async def write_file(request: WriteFileRequest):
    return await write_file_core(request.path, request.content, request.overwrite)

@app.post("/append_to_file", summary="Append to a file")
async def append_to_file(request: AppendFileRequest):
    return await append_to_file_core(request.path, request.content)

@app.post("/update_file", summary="Update text in a file")
async def update_file(request: UpdateFileRequest):
    return await update_file_core(request.path, request.old_text, request.new_text, request.count)

@app.post("/delete_file", summary="Delete a file")
async def delete_file(request: DeleteFileRequest):
    return await delete_file_core(request.path)

@app.post("/list_directory", summary="List directory contents")
async def list_directory(request: ListDirectoryRequest):
    return await list_directory_core(request.path, request.show_hidden, request.detailed)

@app.post("/find_files", summary="Find files")
async def find_files(request: FindFilesRequest):
    return await find_files_core(request.directory, request.pattern, request.recursive, request.max_results)

@app.post("/create_directory", summary="Create a directory")
async def create_directory(request: CreateDirectoryRequest):
    return await create_directory_core(request.path, request.parents)

@app.post("/organize_directory", summary="Organize a directory")
async def organize_directory(request: OrganizeDirectoryRequest):
    return await organize_directory_core(request.directory, request.by, request.dry_run)

@app.post("/count_words", summary="Count words in text")
async def count_words(request: CountWordsRequest):
    return await count_words_core(request.text)

@app.post("/search_text", summary="Search text")
async def search_text(request: SearchTextRequest):
    return await search_text_core(request.text, request.query, request.case_sensitive)

@app.post("/calculate", summary="Calculate expression")
async def calculate(request: CalculateRequest):
    return await calculate_core(request.expression)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
