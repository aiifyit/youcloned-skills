---
name: strategist
description: "Historical and philosophical wisdom from 30,000 classic books — strategic decisions, business philosophy, leadership, and cross-era pattern recognition. Not web search; mined from the historical canon."
---

# Strategist Skill

Retrieves semantically relevant passages from a 30,000-book corpus (philosophy, strategy, science, economics, military theory, psychology, history) and synthesizes the highest-signal principles that apply to Joshua's question.

## Usage

```bash
python3 ~/.openclaw/workspace/skills/strategist/scripts/query.py "your question or situation here"
```

## What it returns

- **Core Principles** — distilled truths from the most relevant sources, with attribution and direct application to the question
- **Convergence Signals** — where multiple thinkers independently arrive at the same principle (strongest signal)
- **Contrarian Insights** — principles that cut against conventional thinking

## Index location

```
~/Projects/jane-books-rag/data/books.faiss    # FAISS vector index
~/Projects/jane-books-rag/data/books.db       # SQLite metadata
```

## Status

Index builds overnight (~14 hours). Check progress:
```bash
sqlite3 ~/Projects/jane-books-rag/data/books.db "SELECT COUNT(*) FROM books;"
```
Full index = 29,945 books. Retrieval works at any point during build — more books = better results.

## When to use

- Strategic decisions (pricing, positioning, hiring, partnerships)
- Negotiation and persuasion
- Leadership and execution challenges
- Philosophy and first-principles thinking
- Business model design
- Any question where "what have the greatest minds said about this" matters
