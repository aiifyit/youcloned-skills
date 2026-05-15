---
name: research-search
description: "Real-time web research — current events, recent news, live data, and multi-source synthesis from the open web. For peer-reviewed science, use academic-researcher. For historical strategy, use strategist."
---

# Research Search Skill

## How to Use

Three search modes depending on the question type:

### 1. Standard Web Search (default — fast, ~10 sec)
```bash
python3 ~/Projects/jane-search/search.py "your question here"
```
Brave search → Jina.ai scrape → Claude Haiku synthesis

### 2. Academic / Sci-Bot Only (slow — 5–30 min queue)
```bash
python3 ~/Projects/jane-search/search.py --scibot "peer-reviewed question"
```
Routes through sci-bot.ru (Sci-Hub-powered academic AI). Best for: clinical research, pharmacology, genomics, mechanisms of action, anything needing peer-reviewed sources.

### 3. Combined Web + Academic (parallel — returns when both done)
```bash
python3 ~/Projects/jane-search/search.py --all "question needing both"
```
Runs both in parallel. Web result comes back fast; sci-bot streams in when queue clears. Final synthesis combines both into one unified answer.

## When to Use Each Mode

| Question Type | Mode |
|---|---|
| Current events, products, news | default |
| Fitness/nutrition mechanisms | `--all` |
| Drug interactions, clinical data | `--scibot` |
| Genomics, epigenetics, biochem | `--scibot` or `--all` |
| Business research, market data | default |
| Anything needing citations | `--all` |

## Output Format

Returns a synthesized answer with source citations. Present the answer directly — don't dump raw output. For `--all`, note whether academic sources were included.

## Example Queries

- `python3 ~/Projects/jane-search/search.py "what supplements actually help with muscle growth"`
- `python3 ~/Projects/jane-search/search.py --scibot "PPARG and mitochondrial biogenesis mechanisms"`
- `python3 ~/Projects/jane-search/search.py --all "creatine effects on muscle protein synthesis"`
- `python3 ~/Projects/jane-search/search.py "Tennessee real estate market 2026"`

## Script Location

`~/Projects/jane-search/search.py`

## Dependencies

- `anthropic` (pip installed)
- `requests` (pip installed)
- Brave API key: loaded from `~/.openclaw/openclaw.json` (tools.web.search.apiKey)
- Anthropic API key: loaded from `~/.openclaw/workspace/.env.private`
- Jina.ai reader: free, no key needed — `https://r.jina.ai/{url}`

## Use For

- Current events and news
- Product research and comparisons
- Health/fitness questions needing recent data
- Business intelligence
- Real estate markets
- Tech comparisons
- Anything needing synthesis from multiple live web sources

## NOT For

- Questions answerable from Jane's memory (use search_memory)
- Simple factual lookups (just answer directly)
- Confidential or sensitive queries that shouldn't hit external APIs
