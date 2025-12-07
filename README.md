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
It uses:FastAPI for an asynchronous backendhttpx for GitHub API callsGoogle Gemini for structured summarizationStreamlit for a clean, interactive frontend🧩 Architecture<p align="center">  </p>✅ Tech StackLanguage: Python 3.11Backend: FastAPI + httpx + PydanticFrontend: StreamlitAI: Google Gemini 1.5Hosting Ready: Hugging Face / Render / Deta🎯 Prompt Engineering StrategyStrict Schema Enforcement → Gemini outputs JSON only, validated with PydanticMulti-shot Few-Shot Prompting → 4 examples (Bug, Feature, Docs, Question)Repair Prompt → If malformed JSON, retry automaticallyContextual Guidance → Explicit field definitions, multilingual supportTruncation → Large bodies/comments are trimmed for faster inference⚙️ Edge Cases HandledEdge CaseBehavior❌ Invalid repo URLReturns 400 with clear message🔒 Private repo403 with token hint🚫 Issues disabledGraceful error with message❓ No comments/bodyConservative JSON generation🧾 Long textTruncated for efficiency🌐 Non-EnglishTranslated to English automatically⏳ Rate limitWarning to add GITHUB_TOKEN⚙️ Invalid modelFallback or descriptive error🧰 Setup & InstallationPrerequisitesPython 3.11+Google AI Studio API Key (starts with AIza...)Optional GitHub Token (to raise rate limit)1️⃣ Clone & Create venvBashgit clone [https://github.com/](https://github.com/)<your-username>/ai-github-issue-assistant.git
cd ai-github-issue-assistant
python -m venv venv
venv\Scripts\activate # or source venv/bin/activate
2️⃣ Install DependenciesBashpip install -r requirements.txt
3️⃣ Configure EnvironmentCreate file: backend/.envIni, TOMLGOOGLE_API_KEY=AIza...your_key_here
GITHUB_TOKEN=ghp_...optional_token
MODEL_NAME=models/gemini-1.5-flash-latest
🏃 Running the App▶ BackendBashcd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
▶ FrontendBashcd ../frontend
streamlit run streamlit_app.py
URLsBackend: http://127.0.0.1:8000/docsFrontend: http://localhost:8501💡 Usage DemoEnter a repo URL → e.g. https://github.com/facebook/reactEnter an issue number → e.g. 27000Click Analyze IssueView:SummaryTypePrioritySuggested LabelsPotential ImpactDownloadable JSON🧪 TestingBashpip install pytest
pytest -q
Tests cover:Health endpointInvalid repo or issueNo comments/bodyJSON validation and structure⚙️ Performance & SpeedOptimizationDescription⚡ Async I/OParallel GitHub + Gemini calls🧮 Token controlTruncation for long issues🧠 Few-shotImproves consistency🩺 Health checkQuick status route⏱ Latency logsMonitors performanceAverage runtime: 3–4 seconds per issue (Gemini Flash).🌱 Going the Extra MileEnhancementPurpose✅ JSON download buttonExport results easily✅ Inline warningsClear feedback UX✅ Repair promptRecovers malformed JSON✅ Copy-to-clipboardOne-click JSON copy✅ Rich READMERubric-aligned documentation✅ Expanded few-shot promptHigher reliability🔐 Security.env excluded via .gitignoreUse read-only GitHub tokensRevoke API keys after testing🧭 Future EnhancementsRepo-specific label ontologyPersistent caching (SQLite/Redis)Batch analysis modeEvaluation metrics (ROUGE/F1)💬 AuthorShlok IyerAI Engineer • Problem Solver • Loves clean code 🌿🏁 Evaluation Mapping (Seedling Labs Rubric)CriterionDeliverableProblem Solving & AI Acumen (40 %)Few-shot prompt, schema validation, edge handlingCode Quality (30 %)Modular structure, docstrings, READMESpeed & Efficiency (20 %)Async design, token controlCommunication & Initiative (10 %)Clear commits, UX extras, polished docs
