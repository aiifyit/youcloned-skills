---
name: wealth-library
description: "Joshua and Sarah's curated personal library on wealth — investing, real estate, land, business strategy, and self-improvement from 14 specific foundational books they own. Not general research."
---

# Wealth & Wisdom Library Skill

## Overview

Joshua and Sarah have a curated library of 14 foundational books on wealth, land, business, and philosophy — all ingested into Jane's RAG brain and local SQLite database for instant semantic search and retrieval.

**Database:** `/Users/janepellicer/Projects/jane-books-rag/data/books.db`
**RAG endpoint:** `http://localhost:7437` — use `POST /retrieve {"query": "...", "top_k": 8}`

---

## The Library

### Wealth & Investing

| Book | Author | Key Idea |
|---|---|---|
| *The Richest Man in Babylon* | George S. Clason | Pay yourself first — 10% of everything, always. Parables of compound wealth. |
| *The Science of Getting Rich* | Wallace D. Wattles | Wealth creation is a science. Do things "in a certain way." Fixed supply = land advantage. |
| *How to Invest Money* | George Garr Henry | Practical investment principles, 1910 edition — timeless risk/return logic. |
| *Creating Capital* | Frederick L. Lipman | Money-making as a systematic aim. Capital formation principles. |
| *Profitable Stock Exchange Investments* | Various | Speculation vs. investment distinction — when to hold, when to walk. |
| *Frenzied Finance* | Thomas Lawson | Inside account of Wall Street manipulation — what NOT to do. |
| *Memoirs of Extraordinary Popular Delusions* | Charles Mackay | Tulip Mania, South Sea Bubble, Mississippi Scheme — how bubbles form and burst. CRITICAL reading before any speculative investment. |
| *Fiat Money Inflation in France* | Andrew Dickson White | What happens when governments print money — protect hard assets. |

### Land & Real Estate

| Book | Author | Key Idea |
|---|---|---|
| *Progress and Poverty* | Henry George | Land value is created by the surrounding community, not the owner. Own land; own a stake in regional growth. |
| *The Land Question* | Henry George | Why land ownership is the most durable form of wealth. |
| *Acres of Diamonds* | Russell H. Conwell | Opportunity is always closer than you think. The diamonds were in the backyard. |
| *Three Acres and Liberty* | Bolton Hall | Small farm economics — how modest land produces outsized freedom. |
| *Principles of Mining* | Herbert Hoover | Asset valuation, land appraisal, organization — written by a future U.S. President who was first a mining engineer. |
| *George Washington: Farmer* | Paul Haworth | How Washington built Mount Vernon as an income-producing estate. |
| *The Farm That Won't Wear Out* | Cyril Hopkins | Soil management and long-term agricultural land productivity. |

### Business & Strategy

| Book | Author | Key Idea |
|---|---|---|
| *The Art of Money Getting* | P.T. Barnum | Don't let your money sleep. Advertise. Persevere. Practical and blunt. |
| *The Art of War* | Sun Tzu | Strategy, positioning, knowing your terrain before you fight. |
| *The Age of Big Business* | Burton Hendrick | How the great American fortunes were built — patterns and principles. |
| *Up To Date Business* | Seymour Eaton | Banking, exchange, commercial law — practical business mechanics. |
| *The Wealth of Nations* | Adam Smith | The original — division of labor, markets, value creation. |
| *An Inquiry into the Permanent Causes of the Decline of Wealthy Nations* | William Playfair | Why great wealth eventually collapses — avoid these patterns. |

### Time, Self & Philosophy

| Book | Author | Key Idea |
|---|---|---|
| *How to Live on 24 Hours a Day* | Arnold Bennett | You have 8 free hours daily — use them intentionally or lose the compounding advantage. |
| *Self-Reliance and Other Essays* | Ralph Waldo Emerson | Trust your own mind. The path others haven't taken is where opportunity lives. |
| *The Autobiography of Benjamin Franklin* | Benjamin Franklin | How Franklin built wealth through printing, real estate, and systematic habits. |
| *Poor Richard's Almanack* | Benjamin Franklin | 25 years of compressed wisdom in aphorisms. "An investment in knowledge pays the best interest." |
| *The Law of Success* | Napoleon Hill | Precursor to Think and Grow Rich — the raw framework before it was polished. |

---

## How to Use

### Query RAG for a specific topic
```bash
curl -s -X POST http://localhost:7437/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "how to buy land and build wealth", "top_k": 8}'
```

### Query the SQLite DB directly
```python
import sqlite3
conn = sqlite3.connect('/Users/janepellicer/Projects/jane-books-rag/data/books.db')
c = conn.cursor()
rows = c.execute("""
    SELECT title, author, text FROM chunks
    WHERE lower(text) LIKE '%land%' AND title LIKE '%Poverty%'
    LIMIT 5
""").fetchall()
for r in rows: print(f"[{r[0]}] {r[2][:200]}")
```

---

## Key Insights for Joshua & Sarah

### On Land (TN Property context)
- Henry George: land value is created by the community around it. Buying rural TN now = buying into regional growth
- Acres of Diamonds: the opportunity is already close — you went and found it
- Three Acres and Liberty: small farm + smart management = outsized personal freedom
- Hoover's Principles of Mining: value any land acquisition by its productive capacity, not just current market price

### On Wealth Building
- Richest Man in Babylon: pay yourself first, always, before any other bill
- Science of Getting Rich: it's a method, not luck — replicate what works
- Mackay's Popular Delusions: avoid what everyone is excited about; find what nobody's talking about

### On Time
- Arnold Bennett: 8 free hours daily. The person who uses them compounds. The person who doesn't, doesn't.
- Franklin's Autobiography: Franklin retired at 42 — not from earning more, but from building systems that earned without him

---

## Access for Sarah

Sarah (via Mochi at @SarahLemay_bot) has read access to this library skill and can query any book or ask Jane to pull wisdom on any topic. The library belongs to both Joshua and Sarah.

*Built April 12, 2026 by Jane*
