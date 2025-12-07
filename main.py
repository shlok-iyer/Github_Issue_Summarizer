import os
import re
import asyncio
from typing import Dict, Any, List

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import ValidationError
from models import AnalyzeRequest, AnalyzeResponse, AnalysisJSON
from prompt import SYSTEM_INSTRUCTIONS, FEW_SHOT_EXAMPLE

import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing. Put it in backend/.env")

genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI(title="AI-Powered GitHub Issue Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

GITHUB_API = "https://api.github.com"

def parse_repo(repo_url: str) -> str:
    """
    Accepts e.g. https://github.com/facebook/react and returns 'facebook/react'.
    """
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url.rstrip("/"))
    if not m:
        raise ValueError("Invalid GitHub repo URL")
    return f"{m.group(1)}/{m.group(2)}"

async def fetch_issue(owner_repo: str, issue_number: int) -> Dict[str, Any]:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=30) as client:
        issue_resp = await client.get(f"{GITHUB_API}/repos/{owner_repo}/issues/{issue_number}", headers=headers)
        if issue_resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Issue not found")
        issue_resp.raise_for_status()
        issue = issue_resp.json()

        # Comments (paginate, up to ~200 to stay snappy)
        comments: List[Dict[str, Any]] = []
        page = 1
        while True:
            c = await client.get(
                f"{GITHUB_API}/repos/{owner_repo}/issues/{issue_number}/comments",
                params={"per_page": 100, "page": page},
                headers=headers
            )
            c.raise_for_status()
            batch = c.json()
            comments.extend(batch)
            if len(batch) < 100 or len(comments) >= 200:
                break
            page += 1

        return {"issue": issue, "comments": comments}

def build_llm_input(payload: Dict[str, Any]) -> str:
    issue = payload["issue"]
    comments = payload["comments"]

    title = issue.get("title", "")
    body = issue.get("body", "") or "(no body)"
    issue_url = issue.get("html_url", "")
    ctexts = [c.get("body", "") for c in comments if c.get("body")]
    if not ctexts:
        ctexts = ["(no comments)"]

    # Soft truncate to keep prompt small (Gemini 1.5 has large context, but we stay safe)
    def truncate(txt: str, limit: int) -> str:
        return (txt[:limit] + "…") if len(txt) > limit else txt

    body = truncate(body, 8000)
    joined_comments = truncate("\n---\n".join(ctexts), 8000)

    return f"""
{SYSTEM_INSTRUCTIONS}

{FEW_SHOT_EXAMPLE}

Issue URL: {issue_url}

Title:
{title}

Body:
{body}

Comments:
{joined_comments}
"""

async def call_gemini(prompt_text: str) -> Dict[str, Any]:
    model = genai.GenerativeModel(MODEL_NAME)
    # We’ll strongly nudge pure-JSON output:
    response = await asyncio.to_thread(
        model.generate_content,
        [{"role": "user", "parts": [prompt_text]}],
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            top_p=0.9,
            max_output_tokens=1024,
            response_mime_type="application/json",  # helps enforce JSON-only output
        ),
        safety_settings=None,
    )
    text = response.text
    # Basic guard: ensure we got JSON-looking content
    if not text.strip().startswith("{"):
        # Try to extract JSON block if model added prose
        import json, re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
        else:
            raise HTTPException(status_code=500, detail="LLM did not return JSON")

    import json
    try:
        return json.loads(text)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON from LLM")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    try:
        owner_repo = parse_repo(str(req.repo_url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    fetched = await fetch_issue(owner_repo, req.issue_number)
    llm_input = build_llm_input(fetched)
    llm_json = await call_gemini(llm_input)

    # Validate/shape into our schema
    try:
        analysis = AnalysisJSON(**llm_json)
    except ValidationError:
        # try to coerce minimal shape
        raise HTTPException(status_code=500, detail="LLM JSON missing required fields")

    return AnalyzeResponse(
        repo=owner_repo,
        issue_number=req.issue_number,
        issue_url=f"https://github.com/{owner_repo}/issues/{req.issue_number}",
        analysis=analysis
    )

# Run:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
