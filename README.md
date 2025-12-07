<!-- ======================= -->
<!--        BANNER           -->
<!-- ======================= -->
<p align="center">
  <img src="assets/banner_placeholder.png" alt="AI-Powered GitHub Issue Assistant Banner" width="850">
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
11. [Future Enhancements](#-future-enhancements)

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

🧩 Architecture
<p align="center"> <img src="assets/architecture_placeholder.png" alt="Architecture Diagram" width="700"> </p>

✅ Tech Stack

Language: Python 3.11

Backend: FastAPI + httpx + Pydantic

Frontend: Streamlit

AI: Google Gemini 1.5

Hosting Ready: Hugging Face / Render / Deta
