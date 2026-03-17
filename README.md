# github-proxy-api

A FastAPI proxy that gives org members read-only access to private GitHub repositories — without exposing a Personal Access Token directly.

## What It Does

- **List repositories** — returns all repos accessible by the configured PAT
- **Read file contents** — fetches any file by path, handles base64 decoding automatically
- **Browse directories** — lists files and folders within any repo path
- All endpoints are read-only. No write operations are exposed.

## Why It Exists

Sharing a PAT directly gives anyone who has it full account-level access. This proxy scopes access to specific read operations and can be deployed behind your own auth layer, IP allowlist, or internal network — keeping the token server-side only.

## Stack

- **Python 3.11+**
- **FastAPI** + Uvicorn
- **httpx** for async GitHub API calls
- **python-dotenv** for config

## Setup

```bash
git clone https://github.com/SeayInsights/github-proxy-api
cd github-proxy-api
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_DEFAULT_REPO=your-org/your-repo
```

## Running

```bash
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/repos` | List all accessible repositories |
| `GET` | `/repos/{owner}/{repo}/contents/{path}` | Read file contents (decoded) |
| `GET` | `/repos/{owner}/{repo}/tree/{path}` | Browse directory listing |

## Security Notes

- Never commit `.env` — it's in `.gitignore`
- Rotate your PAT at `github.com/settings/tokens` if compromised
- Consider adding API key auth or IP allowlisting before any public deployment

## License

MIT
