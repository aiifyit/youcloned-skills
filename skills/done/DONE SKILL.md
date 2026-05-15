---
name: done
description: End-of-session checkpoint for the CURRENT TAB ONLY. Scans this conversation thread and outputs a checkbox list of what was done in this session, plus a Receipts table with hours saved, money saved at the user's per-hour rate, and a defensible potential-earnings range. Does NOT roll up other tabs (use /done-day for that). Trigger on /done.
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# /done - End-of-Session Checkpoint Report (This Tab Only)

## Scope (read this first)

`/done` reports on **THIS TAB / THIS SESSION ONLY**. It does not aggregate other tabs, does not summarize "today" globally, and does not list anything that is still open or pending. The format is: here is what got done in this conversation, and here is what it was worth.

For cross-tab roll-up, use `/done-day` (which reads `~/.config/done/log.jsonl` and combines every tab's entries from today).

## When to invoke

User types `/done` (or says "wrap up this tab" / "what did we get done in this session"). The skill scans the CURRENT conversation thread and produces a clean checkpoint that can be:
- Saved to the per-tab log (`~/.config/done/log.jsonl`) for `/done-day` aggregation
- Forwarded to a manager (Copy Collective team)
- Pasted into Slack, Notion, or email

## Inputs

- **Thread context:** every meaningful task ACCOMPLISHED in this conversation. Not blocked items, not pending items, not future ideas. Only what got done.
- **Config file:** `~/.config/done/config.json` with the schema:
  ```json
  {
    "default_rate_per_hour": 250,
    "users": {
      "<user_slug>": { "rate_per_hour": 250 }
    }
  }
  ```

## First-run flow

1. Try to identify the current user (Jon = `jon_benson`. For Copy Collective team members, derive a slug from their Slack/git handle).
2. If `config.json -> users[<slug>] -> rate_per_hour` exists, use it. Skip the prompt.
3. If it does NOT exist, ASK exactly one question: **"What's your hourly rate? Pick a realistic number for what your time is worth per hour to your business."** Save the answer to `users[<slug>].rate_per_hour`.
4. Don't ask again on subsequent runs unless the user explicitly asks to change the rate.

If the config file is missing entirely, create it with `default_rate_per_hour: 250` plus an empty `users` object, then ask the user as in step 3.

## Rate

Flat per-user hourly rate from `config.json -> users[<slug>].rate_per_hour`. No per-task tier breakdown. `Hours x rate = money saved` for every row in the Receipts table.

## Hours-saved estimation

Estimate accurately. Round to 0.25-hour increments. The question to ask for each task: "If Jon had to do this himself by hand, how long would it have taken him?" NOT how long the AI took. We are measuring his saved time, not the AI's compute time.

For complex multi-step tasks, total the time he would have spent on EACH step including context-switching and lookups.

## Potential earnings

Each task gets a category from `~/.config/done/config.json`'s `potential_earnings_categories` block.

- **revenue_direct:** present as a low-high range. Method: % conversion lift x estimated traffic x price. Always show the assumption ("assumes 0.5% lift on $797 quarterly product, 200 visits/wk").
- **revenue_supporting:** indirect range based on retention. State the assumption.
- **infrastructure:** $0 direct. Flag "saves N hours/year" if reusable.
- **admin:** $0 direct. Money saved IS the earnings (no separate potential).

If you cannot defensibly estimate a range, write "low confidence" and pick a conservative range. Never invent numbers without naming the math.

## Output format

TWO sections, in this order. No "Still open", no "today", no other tabs.

### 1. Done in this session

Clean checkbox bullets. Just the task title.

```
- [x] <task title>
```

### 2. Receipts

A per-task table that anyone can audit. Every Done item appears as a row with columns: Task, Hours saved, Money saved, Potential earnings. Money saved = hours x $rate. Potential earnings is either a defensible $X to $Y range with the assumption named in the cell, or "$0 (infra)" / "$0 (admin)" for non-revenue work.

End the table with a Total row that sums hours and money saved.

```
| Task | Hours saved | Money saved | Potential earnings |
|---|---|---|---|
| <task> | 1.5 | $375 | $X to $Y assumes <assumption> |
| ... | ... | ... | ... |
| **Total** | **N** | **$N** | <range, plus ongoing if relevant> |
```

After the table, one closing line naming the headline potential-earnings assumption so the range is defensible.

## Output example (small case)

```markdown
## Done in this session

- [x] Wired YouTube Data API + uploaded VSL as unlisted
- [x] Built lock-page reusable skill + script
- [x] Bonuses page rewrite with $2,491 stack copy
- [x] Copied PDF to Desktop for Jon

## Receipts

| Task | Hours saved | Money saved | Potential earnings |
|---|---|---|---|
| YouTube Data API + VSL upload | 1.0 | $250 | $0 (infra, one-shot) |
| Lock-page reusable skill + script | 2.5 | $625 | $0 direct (saves ~10 future hrs/year on Circle changes = $2,500/yr) |
| Bonuses page rewrite ($2,491 stack copy) | 1.5 | $375 | $5,000 to $25,000 assumes 1% conv lift on Collective quarterly upgrade flow |
| Copied PDF to Desktop | 0.25 | $63 | $0 (admin) |
| **Total** | **5.25 hrs** | **$1,313** | **$5,000 to $25,000 direct, $2,500/yr ongoing** |

Headline assumption: 1% conversion lift on the Collective quarterly upgrade flow.
```

## Hard rules

- **No em dashes anywhere.** Use hyphens, colons, ellipses, or new sentences.
- **Only list what got DONE in this tab.** No "still open", no "blocked", no "next up". `/done` is past-tense and tab-scoped.
- The hourly rate config is loaded from `~/.config/done/config.json`. If the user updates their rate, edit that file directly. Never hardcode.
- Output should be self-contained markdown that can be copy/pasted into Slack, Notion, or email without further editing.

## Accuracy rule (potential earnings must be defensible)

Every `Potential earnings` cell is a real claim. The user is going to read these numbers and trust them. If you cannot defend a number, write `$0` and say what category it is. Inflated or fictional ranges destroy the value of this skill.

**When potential earnings is $0:**
- Personal or play work (drawing for a kid, journal entry, learning a tool, organizing a folder for fun)
- Pure infrastructure that will not be reused or does not unlock revenue (e.g., a one-off script for a thing the user never does again)
- Admin (file moves, screenshots, unzipping)
- Anything you cannot point to a specific revenue mechanism for

Mark these `$0 (personal)`, `$0 (admin)`, or `$0 (infra, not reused)` so the user sees you considered it.

**When potential earnings is a real range:**
You must be able to point to a specific path: a sales page, a checkout flow, a paid product, an existing customer base. State that path in the cell. Examples that earn a range:
- Rewriting a live sales page with traffic ($X conversion lift x traffic x price)
- Wiring a checkout flow that was broken ($X recovered transactions)
- Building a script that genuinely will be reused 30+ times in a year ($X saved future hours x rate)
- Producing a video, email, or asset that ships to customers

**When potential earnings is `(saves N hrs/yr)`:**
Only include this when the work is reused REGULARLY (weekly, monthly, multiple times a month). A script the user writes once and runs once does not save future hours. Be specific: "saves ~10 hrs/yr on Circle changes" requires the user to actually plan to make Circle changes that often.

**Red flags to catch yourself:**
- Did you write a range because the work felt valuable, or because you can name the revenue path?
- Are you assuming the user will run the script 50 times this year because that makes the math nice?
- Are you double-counting (the script saves hours AND the work it produces drives revenue)?

If in doubt, lower the range or write $0 with a note. The point of this skill is for the user to trust the totals at the bottom of the day. Once.

## Project attribution (run before producing the report)

Before building the report, check whether this tab has been tagged to a project via `/project`:

```bash
python3 ~/.claude/skills/project/project_lib.py get-tab
```

The output is JSON with `project_id` (string or null). If a project_id is present:

1. Compute the session's totals exactly as you would normally (hours_total, money_saved, potential_low, potential_high).
2. Attribute those totals to the project:
   ```bash
   python3 ~/.claude/skills/project/project_lib.py add-totals <project_id> <hours_total> <money_saved> --pot-low <potential_low> --pot-high <potential_high>
   ```
3. In the report, add ONE line below the Receipts table naming the project:
   ```
   Attributed to project: <Project Name> (running total: <X> hrs, <$Y> money saved across <N> sessions).
   ```

If the project_id is null, skip attribution and produce the report as before. Do NOT prompt Jon to set a project mid-/done. He runs /project explicitly when he wants to tag.

## Cross-tab aggregation (always run)

After producing the report, ALWAYS append one line to `~/.config/done/log.jsonl` so `/done-day` and `/board` can roll up multiple tabs. Schema (one JSON per line):

```json
{"ts":"2026-04-26T18:30:00Z","user_slug":"jon_benson","tab_id":"<session_id>","cwd":"<workspace path>","hours_total":12.5,"money_saved":3125,"potential_low":15000,"potential_high":75000,"potential_ongoing_yearly":30000,"items_done":["task 1","task 2"]}
```

Append (don't overwrite). Create the file if missing. **Use the Claude Code session_id as `tab_id`**, not the workspace cwd. Each tab is a separate session with a unique sessionId, and the dashboard needs that granularity to show per-tab financials. To find the sessionId, look at the session jsonl filename (the part before `.jsonl`) inside `~/.claude/projects/<sanitized-cwd>/`. Always also include `cwd` so legacy lookups still work.

This keeps per-tab cost flat (~200 tokens) and the daily roll-up cheap (parses jsonl, no chat history). The `/done-day` skill reads today's lines and combines.

The log entry has NO `items_open` field. `/done` does not track open items.

## When run by Copy Collective team members (not Jon)

If the current Slack/chat user is a Copy Collective member (not Jon), use THEIR hourly rate from `config.json -> users[<user_id>]` if present, otherwise prompt for it on first run and save to that user's slot. Default fallback: $250/hr (admin tier) until they confirm. Same output shape, just personalized to whose time was saved.
