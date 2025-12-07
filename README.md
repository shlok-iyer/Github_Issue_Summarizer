<p align="center">
  </p>

# 🪴 AI-Powered GitHub Issue Assistant

An intelligent tool that reads any **GitHub issue** and automatically classifies it into a structured JSON summary — identifying the issue **type**, **priority**, **labels**, and **potential impact** — using **Google’s Gemini API** and **live GitHub data**.

> 🎯 **Built for the Seedling Labs Engineering Craft Case**
> Focus: AI-assisted problem solving, clean system design, and thoughtful engineering.

---

## 🌍 Table of Contents
1. [Overview](#-overview)
2. [Architecture](#-architecture)
3. [Prompt Engineering Strategy](#-prompt-engineering-strategy)
4. [Edge Cases Handled](#-edge-cases-handled)
5. [Setup & Installation](#️-setup--installation)
6. [Running the App](#-running-the-app)
7. [Usage Demo](#-usage-demo)
8. [Testing](#-testing)
9. [Performance & Speed](#-performance--speed)
10. [Going the Extra Mile](#-going-the-extra-mile)
11. [Security](#-security)
12. [Future Enhancements](#-future-enhancements)
13. [Author](#-author)
14. [Evaluation Mapping](#-evaluation-mapping)

---

## 🧠 Overview

The **AI-Powered GitHub Issue Assistant** analyzes issues directly from any public GitHub repository and produces a compact, well-structured JSON output.

Each analysis includes:
```json
{
  "summary": "Short plain-English summary",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "N - brief justification",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "Concise impact statement"
}
```
🤖 AI GitHub Issue Assistant
Overview

This project uses:

FastAPI — for an asynchronous backend

httpx — for GitHub API calls

Google Gemini — for structured summarization

Streamlit — for a clean, interactive frontend

##🧩 Architecture
<p align="center"></p>
✅ Tech Stack
Category	Technology
Language	Python 3.11
Backend	FastAPI + httpx + Pydantic
Frontend	Streamlit
AI	Google Gemini 1.5
Hosting Ready	Hugging Face / Render / Deta
## 🎯 Prompt Engineering Strategy

Strict Schema Enforcement → Gemini outputs JSON only, validated with Pydantic

Multi-shot Few-Shot Prompting → 4 examples (Bug, Feature, Docs, Question)

Repair Prompt → If malformed JSON, retry automatically

Contextual Guidance → Explicit field definitions, multilingual support

Truncation → Large bodies/comments are trimmed for faster inference

## ⚙️ Edge Cases Handled
Edge Case	Behavior
❌ Invalid repo URL	Returns 400 with clear message
🔒 Private repo	403 with token hint
🚫 Issues disabled	Graceful error with message
❓ No comments/body	Conservative JSON generation
🧾 Long text	Truncated for efficiency
🌐 Non-English	Translated to English automatically
⏳ Rate limit	Warning to add GITHUB_TOKEN
⚙️ Invalid model	Fallback or descriptive error
## 🧰 Setup & Installation
Prerequisites

Python 3.11+

Google AI Studio API Key (starts with AIza...)

Optional GitHub Token (to raise rate limit)

1️⃣ Clone & Create Virtual Environment
git clone https://github.com/<your-username>/ai-github-issue-assistant.git
cd ai-github-issue-assistant
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment

Create file: backend/.env

GOOGLE_API_KEY=AIza...your_key_here
GITHUB_TOKEN=ghp_...optional_token
MODEL_NAME=models/gemini-1.5-flash-latest

🏃 Running the App
▶ Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

▶ Frontend
cd ../frontend
streamlit run streamlit_app.py

URLs

Backend: http://127.0.0.1:8000/docs

Frontend: http://localhost:8501

💡 Usage Demo

Enter a repo URL → e.g. https://github.com/facebook/react

Enter an issue number → e.g. 27000

Click Analyze Issue

Output Includes:

Summary

Type

Priority

Suggested Labels

Potential Impact

Downloadable JSON

🧪 Testing
pip install pytest
pytest -q

Tests cover:

Health endpoint

Invalid repo or issue

No comments/body

JSON validation and structure

⚙️ Performance & Speed
Optimization	Description
⚡ Async I/O	Parallel GitHub + Gemini calls
🧮 Token control	Truncation for long issues
🧠 Few-shot	Improves consistency
🩺 Health check	Quick status route
⏱ Latency logs	Monitors performance

Average runtime: 3–4 seconds per issue (Gemini Flash)

🌱 Going the Extra Mile
Enhancement	Purpose
✅ JSON download button	Export results easily
✅ Inline warnings	Clear feedback UX
✅ Repair prompt	Recovers malformed JSON
✅ Copy-to-clipboard	One-click JSON copy
✅ Rich README	Rubric-aligned documentation
✅ Expanded few-shot prompt	Higher reliability
🔐 Security

.env excluded via .gitignore

Use read-only GitHub tokens

Revoke API keys after testing

🧭 Future Enhancements

Repo-specific label ontology

Persistent caching (SQLite / Redis)

Batch analysis mode

Evaluation metrics (ROUGE / F1)

💬 Author

Shlok Iyer
AI Engineer • Problem Solver • Loves clean code 🌿

🏁 Evaluation Mapping (Seedling Labs Rubric)
Criterion	Deliverable
Problem Solving & AI Acumen (40%)	Few-shot prompt, schema validation, edge handling
Code Quality (30%)	Modular structure, docstrings, README
Speed & Efficiency (20%)	Async design, token control
Communication & Initiative (10%)	Clear commits, UX extras, polished docs
