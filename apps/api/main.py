from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpcore import request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import json
import numpy as np
from pathlib import Path

app = FastAPI(title="Lunim KMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path("data/chunks_with_embeddings.json")
model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class SearchRequest(BaseModel):
    query: str
    session: str | None = None
    category: str | None = None
    meaningful_only: bool = False
    top_k: int = 5


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search(request: SearchRequest):
    if not DATA_PATH.exists():
        return {"results": [], "error": "chunks_with_embeddings.json not found"}

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    query_embedding = model.encode(request.query).tolist()
    scored_chunks = []

    for chunk in chunks:
        meta = chunk.get("metadata", {})

        if request.session and meta.get("session") != request.session:
            continue

        if request.category and request.category not in meta.get("category", []):
            continue

        if request.meaningful_only and not meta.get("has_meaningful_content", False):
            continue

        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    MIN_SCORE = 0.35  # adjust after testing

    filtered_chunks = [
    (score, chunk)
        for score, chunk in scored_chunks
        if score >= MIN_SCORE
    ]

    results = []
    for score, chunk in filtered_chunks[: request.top_k]:
        preview = chunk["text"][:300].replace("\n", " ")
        results.append({
            "score": round(score, 4),
            "title": chunk["title"],
            "preview": preview,
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "files": chunk.get("files", []),
        })

    if not results:
        return {
            "results": [],
            "message": "No sufficiently relevant results found for this query."
        }

    return {
        "results": results,
        "message": None
    }