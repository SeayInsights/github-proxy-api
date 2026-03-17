# GitHub Proxy API

> **Portfolio Reference** — A FastAPI reverse proxy that exposes scoped, read-only access to private GitHub repositories without surfacing a Personal Access Token to clients. Demonstrates API security design, async Python, and the principle of least privilege applied to internal tooling.

---

## What This Demonstrates

- **API security design** — PAT stays server-side; clients get read-only access via a controlled proxy layer, not raw token access
- **Async FastAPI** — `httpx` async client for non-blocking GitHub API calls; production-ready with Uvicorn
- **Principle of least privilege** — only three read operations exposed (list repos, read file, browse directory) — no write surface
- **Deployable internal tooling** — designed to sit behind an auth layer, IP allowlist, or internal network; drop-in for team or client environments

---

## Why It Exists

Sharing a PAT directly gives anyone who has it full account-level write access. This proxy scopes exposure to specific read operations. Use cases: giving a client read access to a delivery repo, exposing repo contents to an internal tool or dashboard, or feeding a CI/CD step without PAT sprawl.

---

## Stack

- **Python 3.11+** · FastAPI · Uvicorn
- **httpx** — async GitHub API calls
- **python-dotenv** — config management

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/repos` | List all accessible repositories |
| `GET` | `/repos/{owner}/{repo}/contents/{path}` | Read file contents (base64 decoded) |
| `GET` | `/repos/{owner}/{repo}/tree/{path}` | Browse directory listing |

All endpoints are read-only. No write operations exposed.

---

## Setup

```bash
git clone https://github.com/SeayInsights/github-proxy-api
cd github-proxy-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set GITHUB_TOKEN and GITHUB_DEFAULT_REPO in .env
uvicorn main:app --reload
```

API docs at `http://localhost:8000/docs`

---

## Security Notes

- Never commit `.env` — gitignored by default
- Add API key auth or IP allowlisting before any public deployment
- Rotate your PAT at `github.com/settings/tokens` if compromised

---

Built by [SeayInsights](https://github.com/SeayInsights) · FastAPI · Python · API security design
