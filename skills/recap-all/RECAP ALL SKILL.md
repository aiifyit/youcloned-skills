---
name: recap-all
description: Cross-tab recap aggregator. Lists every currently-open Claude Code tab (any session with activity in the last 12 hours, across any working directory) and gives ONLY the four-part summary per tab - WHY we're doing it, WHAT YOU LEARNED, SUMMARY, and WHAT'S NEXT. No phase breakdowns. Trigger on /recap-all.
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# /recap-all - Cross-Tab Recap (Open Tabs Only)

## Why this skill exists

`/recap` is per-tab and verbose. When you have 5+ Claude Code tabs open across different projects, you don't want to run `/recap` in each and mentally combine them. You want ONE call that sweeps every open tab and gives you a flight-level summary so you can decide which tab needs attention next.

This is the global "where am I across all current work" view.

## When to invoke

User types `/recap-all` (or says "recap all my tabs", "what's open across everything", "flight-level recap"). Produce the recap immediately. No clarifying questions.

Optional argument: `/recap-all <hours>` to override the default 12-hour activity window. Example: `/recap-all 6` only shows tabs with activity in the last 6 hours.

## What counts as an "open tab"

A tab is considered open if its session JSONL file has been modified in the last N hours (default 12). Claude Code writes to the JSONL on every message, so file mtime = last activity time. Tabs that have been closed for more than N hours are excluded.

This is approximate. Claude Code doesn't expose a true "currently open" flag. But sessions with recent activity ARE the ones you care about.

## Where the data comes from

Claude Code auto-saves every message to a JSONL file at:

```
~/.claude/projects/<sanitized-cwd>/<session_id>.jsonl
```

Each project directory (one per working directory you've used Claude Code in) contains its own JSONL files. To find all open tabs:

```bash
# Find all JSONL files modified in the last N hours (default 12)
HOURS=12
find ~/.claude/projects -name "*.jsonl" -mmin -$((HOURS * 60)) 2>/dev/null
```

Each match is one open tab. The parent directory (with `-` replaced by `/`) is the working dir for that session.

If you've wired sessions to a database (Supabase, Postgres, SQLite), prefer querying that. The JSONL scan is the universal fallback.

## Output format (EXACT structure required)

Lead with a one-line header:

```
# Recap-All · N tabs open · last 12 hours
```

Then for EACH tab, output exactly four sections:

```
## Tab N: <project name or working_dir basename> · <session_id short>

**WHY:** <one sentence - the business outcome, not the tool>

**WHAT YOU LEARNED:**
- <lesson 1 - a rule, a mistake, a principle locked in this session>
- <lesson 2>
- <lesson 3 - keep to 2-5 bullets max>

**SUMMARY:** <3-4 sentences compressing every phase of the tab into one paragraph. Plain English. Name the outcome, not the activity.>

**WHAT'S NEXT:**
- <action 1>
- <action 2>
- <action 3 - keep to 2-5 bullets max>
```

Tab numbering goes by most-recent-activity first (the tab you were just in goes first).

Then end with a cross-tab section:

```
---

## Across all tabs

**Total tabs:** N
**Common themes:** <if 2+ tabs share a theme, name it. Else "no common theme">
**Highest-priority next action:** <pick the single most urgent next step across all tabs, based on what the user has called out as time-sensitive>
```

## Hard rules

- **No em dashes.** Use hyphens, colons, ellipses, or new sentences.
- **No openers signaling the next sentence is real, direct, or candid.** Just state the thing.
- **NEVER expand into phase breakdowns.** That's `/recap`'s job. `/recap-all` is compressed.
- **NEVER include open items inside SUMMARY.** All forward-looking content goes in WHAT'S NEXT.
- **NEVER pad with tabs that had no real activity.** A tab with 3 messages is not an "open tab" - exclude it.
- **WHAT YOU LEARNED is specific lessons, not generic platitudes.** "Read the spec before claiming a feature is missing" beats "be careful." Name the actual rule.
- **SUMMARY is 3-4 sentences MAX.** If you need more, you're treating this like `/recap`. Compress harder.

## Implementation

### Step 1: Find open tabs

```bash
HOURS=12  # or from argument

# Find JSONLs touched within window
mapfile -t TABS < <(find ~/.claude/projects -name "*.jsonl" -mmin -$((HOURS * 60)) 2>/dev/null | sort -r)

echo "Found ${#TABS[@]} open tab candidates"
```

Filter out empty/short sessions (less than ~10 message turns) - those are noise.

### Step 2: For each tab, derive metadata

```python
from pathlib import Path
import json, os

for jsonl_path in tabs:
    path = Path(jsonl_path)
    session_id = path.stem
    # Convert sanitized dir back to real path
    project_dir = path.parent.name.replace('-', '/')
    project_basename = project_dir.split('/')[-1]

    # Count meaningful turns (skip empty / system messages)
    turn_count = sum(1 for line in path.open() if json.loads(line).get('message', {}).get('role') in ('user', 'assistant'))

    if turn_count < 10:
        continue  # noise, skip
```

### Step 3: For each tab, extract WHY / LEARNED / SUMMARY / NEXT

Read the JSONL line by line. The file can be massive. Focus on:

- **First substantive user message** -> seed for WHY
- **Mid-session strategic statements** ("I want X", "the reason we're doing this is...") -> refine WHY
- **Correction moments** ("no, that's wrong", "stop", "you destroyed...") -> seed for WHAT YOU LEARNED
- **Rules locked in** ("never do X again", "from now on Y") -> WHAT YOU LEARNED
- **Activity arc** (build phase, error phase, fix phase) -> SUMMARY
- **Forward statements** ("tomorrow we...", "still need to...") -> WHAT'S NEXT

Compress aggressively. The whole tab gets 4 sections, max ~150 words total.

### Step 4: Cross-tab synthesis

After all tabs are rendered, scan for:

- **Common themes** - if 2+ tabs touch the same system (auth, deploy, copy, infra) or outcome (revenue, retention, scale)
- **Highest-priority next action** - the single most time-sensitive item, ideally something the user flagged as urgent or blocking

### Step 5: Render in the exact format above

Don't ask permission. Render it.

## Why this format works

`/recap` is for deep-diving ONE tab. `/recap-all` is for orienting across ALL tabs without losing context to depth. The four-part shape (WHY / LEARNED / SUMMARY / NEXT) is the minimum viable summary that still captures:

1. **Business outcome** (WHY)
2. **Operating principles** (LEARNED)
3. **Current state** (SUMMARY)
4. **Forward motion** (NEXT)

Read all open tabs in 60 seconds. Decide which one needs attention. Open it. Use `/recap` if you need the depth.

## Optional: cache the per-tab summary

If you have a database wired up, save each tab's four-part summary so subsequent `/recap-all` calls can skip the JSONL re-parse:

```sql
CREATE TABLE IF NOT EXISTS session_recaps (
  session_id TEXT PRIMARY KEY,
  generated_at TIMESTAMPTZ DEFAULT now(),
  why TEXT,
  learned JSONB,
  summary TEXT,
  next_steps JSONB,
  last_activity TIMESTAMPTZ
);
```

On subsequent runs, check `last_activity` against the JSONL mtime. If unchanged, reuse the cached summary. If changed, regenerate.

This is optional. The JSONL scan is fast enough for a handful of tabs.
