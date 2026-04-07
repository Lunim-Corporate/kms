# 🧠 Lunim Knowledge Intelligence System (KMS)

> An AI-ready semantic search and intelligence layer for organisational knowledge.

This system transforms fragmented internal data into **searchable, structured, and traceable intelligence** using a RAG-ready pipeline.

---

## ✨ What This Solves

Organisations struggle with:
- scattered documents (Notion, Slack, interviews, reports)
- poor search (keyword-based, not semantic)
- lack of insight extraction
- no traceability of decisions

👉 This system enables:
- natural language querying
- insight discovery
- source traceability

---

## 🧠 System Overview
Raw Data (Notion / Docs / Interviews)
↓
Cleaning & Normalisation
↓
Canonical Documents
↓
Chunking
↓
Embeddings (MiniLM)
↓
Vector Search
↓
Ranked Results + Metadata
↓
Frontend (Insight UI)

---

## 🏗️ Architecture

### 🔹 Backend (FastAPI)
- Search API (`/query`)
- Embedding pipeline
- Data transformation scripts

### 🔹 Frontend (React + Vite)
- ChatGPT-style UI
- Filterable search
- Insight-focused results

### 🔹 ML Layer
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Cosine similarity search

---

## 📂 Project Structure
apps/
api/        → FastAPI backend
web/        → React frontend

scripts/
clean_documents.py
build_canonical_documents.py
chunk_documents.py
embed_chunks.py
search_chunks.py

data/
clean_documents.json
canonical_documents.json
chunks.json
chunks_with_embeddings.json

---

## ⚙️ Setup Guide

### 1. Clone Repository
```bash
git clone <repo-url>
cd lunim_kms


🔧 Backend Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run server:
python -m uvicorn apps.api.main:app --reload --port 8000

👉 API: http://localhost:8000



🎨 Frontend Setup

cd apps/web
npm install
npm run dev

👉 UI: http://localhost:5173



🔄 Data Pipeline (Critical)

Run in order:
python -m scripts.clean_documents
python -m scripts.build_canonical_documents
python -m scripts.chunk_documents
python -m scripts.embed_chunks



🔎 Search API

Endpoint:
POST /query

Example:
{
  "query": "What onboarding issues did users face?",
  "top_k": 5,
  "session": null,
  "category": null,
  "meaningful_only": true
}




🖥️ UI Experience

Design Philosophy

Users don’t want:
❌ raw chunks
They want:
✅ answers
✅ insights
✅ traceability

⸻

Features
	•	ChatGPT-style search interaction
	•	Bottom search bar (persistent)
	•	Fixed filter sidebar:
	•	Session
	•	Category
	•	Meaningful content toggle
	•	AI Insight block (top summary)
	•	Result cards:
	•	Title
	•	Preview
	•	Metadata (session, category, score)

⸻

📸 Demo Screenshots

Add screenshots here for best impact

🔹 Search Interface
🔹 Results View


⚠️ Current Limitations
	•	No true LLM-generated answers (UI summary is static)
	•	No reranker (pure embedding similarity)
	•	Weak relevance threshold (may return noisy results)
	•	No authentication / multi-user support

⸻

🚀 Next Roadmap

🧠 Intelligence Layer
	•	AI-generated answers (RAG)
	•	Context summarisation
	•	Evidence grounding

🔍 Retrieval Improvements
	•	Hybrid search (keyword + vector)
	•	Reranking (cross-encoder)
	•	Dynamic filtering

🖥️ UX Enhancements
	•	Expandable source view
	•	Highlight matched text
	•	Conversation mode (chat history)

⸻

🧠 Tech Stack

Backend
	•	FastAPI
	•	Python
	•	NumPy

ML
	•	Sentence Transformers
	•	FAISS-ready architecture

Frontend
	•	React (Vite)
	•	Tailwind CSS

⸻

💡 Key Highlights
	•	End-to-end RAG pipeline (data → embeddings → search → UI)
	•	Production-style architecture
	•	UX focused on insights, not raw data
	•	Scalable design (connectors + pipelines ready)

⸻

👨‍💻 Author

Adarsh Thakur
MSc Advanced Computer Science – University of Leeds

⸻

📌 Final Note

This project is not just a search tool —
it is the foundation of an organisational intelligence layer.


---




