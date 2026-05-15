---
name: autoagent
description: |
  Autonomous agent harness self-improvement using AutoAgent (kevinrgu/autoagent). Use when Joshua wants to create a self-optimizing AI agent for Pulse or AIify, run a benchmark loop to improve an existing agent harness overnight, build a new vertical agent (sales, ops, finance, CS) and let it hill-climb on real task benchmarks, or explore agent engineering without manually rewriting code. Trigger phrases: "build a self-improving agent", "run autoagent", "set up a harness benchmark loop", "improve the Pulse agent", "let it optimize overnight".
---

# AutoAgent Skill

AutoAgent is an autonomous agent harness engineer. You give it a directive; it rewrites `agent.py` (system prompt, tools, orchestration), benchmarks itself, scores the result, keeps improvements, and repeats — overnight, without a human in the loop.

**Repo:** `github.com/kevinrgu/autoagent`
**Core concept:** Meta-agent hill-climbs on benchmark score by iterating on its own harness.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/kevinrgu/autoagent.git
cd autoagent

# 2. Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install deps
uv sync

# 4. Set credentials
echo "OPENAI_API_KEY=YOUR_KEY" > .env

# 5. Build Docker base image (one-time)
docker build -f Dockerfile.base -t autoagent-base .

# 6. Add tasks to tasks/ (see Task Format below)

# 7. Run a single task to verify
rm -rf jobs; mkdir -p jobs && uv run harbor run -p tasks/ --task-name "<task-name>" -l 1 -n 1 --agent-import-path agent:AutoAgent -o jobs --job-name latest > run.log 2>&1

# 8. Run full benchmark
rm -rf jobs; mkdir -p jobs && uv run harbor run -p tasks/ -n 100 --agent-import-path agent:AutoAgent -o jobs --job-name latest > run.log 2>&1

# 9. Kick off the meta-agent loop
# Point your coding agent at the repo and prompt:
# "Read program.md and let's kick off a new experiment!"
```

## Key Files

| File | Purpose | Editable? |
|------|---------|-----------|
| `program.md` | Meta-agent directive — what kind of agent to build | ✅ You write this |
| `agent.py` (above adapter boundary) | System prompt, tools, orchestration — the harness | ✅ Meta-agent edits this |
| `agent.py` (below adapter boundary) | Harbor adapter / trajectory serialization | ❌ Fixed — do not touch |
| `tasks/` | Benchmark tasks with verifiers | ✅ You add these |
| `results.tsv` | Score history across runs | Auto-generated |

## What the Meta-Agent Can Modify in `agent.py`

- `SYSTEM_PROMPT` — Agent instructions
- `MODEL` — Model choice (default: `gpt-5`)
- `MAX_TURNS` — Max reasoning steps
- `create_tools(environment)` — Add/remove/modify tools
- `create_agent(environment)` — Change construction, add handoffs, sub-agents via `agent.as_tool()`
- `run_task(environment, instruction)` — Change orchestration logic

## Writing `program.md` (Your Directive)

This is the only file you write. Tell the meta-agent:
1. What kind of agent to build ("Build a sales qualification agent")
2. What success looks like ("Maximize tasks passed in the benchmark")
3. Any constraints ("Do NOT change the model")

See `references/program-examples.md` for Pulse-specific directives.

## Task Format

Tasks live in `tasks/` and follow [Harbor](https://github.com/laude-institute/harbor) format. Each task has:
- An instruction (natural language task for the agent)
- A verifier (checks correctness of the agent's output)

See `references/task-format.md` for structure and examples.

## Applying to Pulse / AIify

Each Pulse vertical agent gets its own AutoAgent experiment:

| Pulse Agent | Directive Goal | Example Tasks |
|-------------|---------------|---------------|
| Sales | Qualify leads, book meetings | Parse CRM data, draft follow-up |
| Ops | Execute SOPs, route tasks | Classify inbound request, assign team |
| Finance | Reconcile, flag anomalies | Categorize transactions, generate P&L |
| CS | Resolve tickets, escalate edge cases | Classify support query, draft reply |

**Client-specific tuning:** Fork `agent.py` per client, run their task benchmark, let meta-agent tune the harness to their workflow.

## Model Swap (non-OpenAI)

Default harness uses OpenAI Agents SDK. To use Anthropic/Claude:
1. Replace `from agents import Agent, Runner` with Anthropic SDK equivalents
2. Update `create_agent()` to use `anthropic.Anthropic()` client
3. Keep the Harbor adapter boundary untouched
4. See `references/claude-adapter.md` for a drop-in adapter pattern

## Requirements

- Docker
- Python 3.10+
- uv (`pip install uv`)
- OpenAI API key (or adapted model credentials)

## Security Notes

Scanner flags in README are false positives:
- `curl | sh` — standard uv installer, safe
- `rm -rf /var/lib/apt/lists/*` — standard Docker cleanup, safe
- `OPENAI_API_KEY=...` — placeholder only, not a real key

Always store real keys in `.env` (gitignored), never in code.
