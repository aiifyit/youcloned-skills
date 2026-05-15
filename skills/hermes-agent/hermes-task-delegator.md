---
name: hermes-agent
description: |
  Delegate tasks to Hermes Agent v0.7.0 as a tool. Use when you need a second autonomous agent to run long-horizon tasks, browse the web with the Camofox anti-detection browser, manage cron jobs, handle multi-platform messaging, execute code in sandboxed environments, or run skills from the Hermes skill hub. Trigger phrases: "use Hermes to...", "have Hermes run...", "delegate to Hermes", "run a Hermes agent task". Hermes runs at ~/Projects/hermes-agent.
---

# Hermes Agent v0.7.0 Skill

Hermes Agent is an autonomous AI agent by NousResearch, installed at `~/Projects/hermes-agent`. Use this skill to delegate tasks to Hermes as a sub-agent, run Hermes CLI commands, or manage the Hermes gateway.

**Install location:** `~/Projects/hermes-agent`
**Run via:** `cd ~/Projects/hermes-agent && uv run hermes <command>`
**Version:** v0.7.0 (2026.4.3) — the Resilience release

## Setup (One-Time)

```bash
# Set your Anthropic API key in Hermes
cd ~/Projects/hermes-agent
echo "ANTHROPIC_API_KEY=<key>" >> .env
echo "LLM_MODEL=anthropic/claude-sonnet-4-6" >> .env

# Verify
uv run hermes status
```

## Running a One-Shot Task

```bash
cd ~/Projects/hermes-agent
uv run hermes chat --model anthropic/claude-sonnet-4-6 \
  "Your task here. Be specific."
```

## Delegating a Task from Jane (Programmatic)

```python
import subprocess, json

result = subprocess.run(
    ["uv", "run", "hermes", "chat", "--json",
     "--model", "anthropic/claude-sonnet-4-6",
     task_prompt],
    cwd="/Users/janepellicer/Projects/hermes-agent",
    capture_output=True, text=True, timeout=300
)
output = result.stdout
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `uv run hermes chat "task"` | One-shot task |
| `uv run hermes chat --resume` | Resume last session |
| `uv run hermes status` | Check config/API status |
| `uv run hermes skills list` | List installed skills |
| `uv run hermes skills install <name>` | Install a Hermes skill |
| `uv run hermes gateway start` | Start messaging gateway |
| `uv run hermes cron list` | List cron jobs |
| `uv run hermes sessions list` | List recent sessions |
| `uv run hermes tools list` | List available tools |
| `uv run hermes doctor` | Diagnose config issues |

## v0.7.0 Key Features

- **Camofox anti-detection browser** — stealth browsing with persistent sessions; install with `uv run hermes tools install camoufox`
- **Pluggable memory providers** — Honcho, vector stores, custom DBs via plugin ABC
- **Credential pool rotation** — multiple API keys per provider, auto-rotation on 401
- **Inline diff previews** — file write/patch operations show diffs in tool activity feed
- **API Server session continuity** — resumable sessions across API calls

## Model Config

Hermes supports multiple providers. For Jane, use Anthropic:

```bash
# Set in .env
LLM_MODEL=anthropic/claude-sonnet-4-6
ANTHROPIC_API_KEY=<your-key>

# Or set per-invocation
uv run hermes chat --model anthropic/claude-sonnet-4-6 "task"
```

Available model aliases:
- `anthropic/claude-sonnet-4-6` — fast, default for Jane delegation
- `anthropic/claude-opus-4` — heavy reasoning tasks
- `anthropic/claude-haiku-3-5` — lightweight/fast tasks

## Installing Hermes Browser (Camofox)

```bash
cd ~/Projects/hermes-agent
uv run hermes tools install camoufox
# Then use: uv run hermes chat "browse to X and extract Y"
```

## Jane ↔ Hermes Integration Patterns

### Pattern 1: Jane delegates a web research task
```bash
uv run hermes chat --model anthropic/claude-sonnet-4-6 \
  "Research the top 5 AI agent frameworks released in 2026. For each: name, repo URL, key features, and GitHub stars. Output as JSON."
```

### Pattern 2: Jane delegates a long-running coding task
```bash
uv run hermes chat --model anthropic/claude-sonnet-4-6 --yolo \
  "In ~/Projects/hermes-agent, create a new skill called 'pulse-sales' that..."
```

### Pattern 3: Jane checks Hermes status before delegation
```bash
uv run hermes status && uv run hermes doctor
```

## Security Notes

- Repo is from NousResearch (Hermes model team) — legitimate, well-audited
- Scanner HIGH/CRITICAL findings were all false positives (test fixtures, doc examples)
- `skills/red-teaming/godmode` exists in repo but is NOT auto-loaded — safe
- Store API keys in `.env` only, never in chat
- Use `--yolo` flag only for trusted, non-destructive tasks (skips approval prompts)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Model not set` | Add `LLM_MODEL=anthropic/claude-sonnet-4-6` to `.env` |
| `API key not set` | Add `ANTHROPIC_API_KEY=<key>` to `.env` |
| `uv: command not found` | `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Browser not working | `uv run hermes tools install camoufox` |
| Task times out | Use `--resume` to continue, or break task into smaller steps |
