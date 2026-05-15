#!/usr/bin/env python3
"""
Strategist — Multi-source principle extraction from the book corpus.
Retrieves relevant passages from across 30K books, then synthesizes
the highest-signal principles, not advisor personas.
"""

import os, faiss, sqlite3, numpy as np, sys
from pathlib import Path
from openai import OpenAI

DATA_DIR = Path.home() / "Projects/jane-books-rag/data"

# Load key
for line in (Path.home() / ".openclaw/workspace/.env.private").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        if k.strip() == "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"] = v.strip()

client = OpenAI()

def load_index():
    index = faiss.read_index(str(DATA_DIR / "books.faiss"))
    db = sqlite3.connect(str(DATA_DIR / "books.db"))
    return index, db

def retrieve(query: str, top_k: int = 12, index=None, db=None) -> list[dict]:
    """Retrieve top-k most relevant passages from all books."""
    resp = client.embeddings.create(model="text-embedding-3-small", input=[query])
    vec = np.array([resp.data[0].embedding], dtype=np.float32)
    faiss.normalize_L2(vec)
    scores, ids = index.search(vec, top_k * 6)

    results = []
    seen_books = set()
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0: continue
        row = db.execute(
            "SELECT book_id, title, author, category, subjects, text FROM chunks WHERE rowid=?",
            (int(idx)+1,)
        ).fetchone()
        if not row: continue
        book_id, title, author, category, subjects, text = row
        if book_id in seen_books: continue
        seen_books.add(book_id)
        results.append({
            "score": float(score),
            "title": title,
            "author": author,
            "category": category,
            "text": text,
        })
        if len(results) >= top_k: break
    return results

SYNTHESIS_PROMPT = """\
You are a principle extractor with access to a corpus of {n_sources} source passages \
from across history's most important works on strategy, philosophy, science, economics, \
military theory, psychology, and more.

The user's question or situation is:
{query}

Below are the {n_sources} most semantically relevant passages retrieved from the corpus:

{passages}

Your job:
1. Extract the highest-signal PRINCIPLES that apply to this situation — not summaries, 
   not paraphrases. Core, distilled truths that transfer directly.
2. Ground each principle in the source that best expresses it (quote briefly if the 
   passage supports it).
3. Synthesize across sources — when multiple thinkers converge on the same principle 
   from different angles, that convergence is the signal. Flag it.
4. Be direct and concrete. Apply each principle to the specific situation stated.
5. Surface any principle that CONTRADICTS conventional thinking — these are often the 
   most valuable.

Format:
## Core Principles

**[Principle statement]**
Source: [Author, Work]
Application: [1-2 sentences applying directly to the question]

...

## Convergence Signals
[Where multiple sources agree — list the principle and the sources]

## Contrarian Insights
[Principles that cut against common intuition]
"""

def analyze(query: str, top_k: int = 12) -> str:
    """Full retrieval + synthesis pipeline."""
    index, db = load_index()
    passages = retrieve(query, top_k=top_k, index=index, db=db)

    if not passages:
        return "No relevant passages found. Index may still be building."

    # Format passages for prompt
    formatted = []
    for i, p in enumerate(passages, 1):
        formatted.append(
            f"[{i}] **{p['title']}** — {p['author'][:60]}\n"
            f"Relevance: {p['score']:.3f}\n"
            f"{p['text'][:600]}"
        )
    passages_text = "\n\n---\n\n".join(formatted)

    prompt = SYNTHESIS_PROMPT.format(
        n_sources=len(passages),
        query=query,
        passages=passages_text,
    )

    resp = client.chat.completions.create(
        model="gpt-4o",  # fast + cheap for synthesis
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Query: ")
    print(analyze(query))
