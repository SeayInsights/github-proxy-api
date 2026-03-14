import os
import base64
from fastapi import FastAPI, HTTPException
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GitHub Proxy API", description="Read-only proxy for private GitHub repositories")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_DEFAULT_REPO = os.getenv("GITHUB_DEFAULT_REPO", "")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

async def gh_get(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=HEADERS)
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Not found")
    r.raise_for_status()
    return r.json()


@app.get("/repos")
async def list_repos():
    """List all repositories accessible by the configured token."""
    data = await gh_get("https://api.github.com/user/repos?per_page=100&type=all")
    return [{"name": r["name"], "full_name": r["full_name"], "private": r["private"], "url": r["html_url"]} for r in data]


@app.get("/repos/{owner}/{repo}/contents/{path:path}")
async def read_file(owner: str, repo: str, path: str, ref: str = "main"):
    """Read and decode file contents from a repository."""
    data = await gh_get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}")
    if data.get("type") != "file":
        raise HTTPException(status_code=400, detail="Path is not a file")
    content = base64.b64decode(data["content"]).decode("utf-8")
    return {"path": path, "sha": data["sha"], "size": data["size"], "content": content}


@app.get("/repos/{owner}/{repo}/tree/{path:path}")
async def browse_directory(owner: str, repo: str, path: str = "", ref: str = "main"):
    """List files and folders within a repository directory."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    data = await gh_get(url)
    if isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Path is a file, not a directory")
    return [{"name": i["name"], "type": i["type"], "path": i["path"], "size": i.get("size")} for i in data]
