---
name: done-day
description: Roll-up of every /done run from today across all open Claude Code tabs. Reads ~/.config/done/log.jsonl, filters to today's entries, and produces ONE combined report with totals across tabs. Run at end of day after you have run /done in each individual tab. Trigger on /done-day. Token-cheap because it parses structured json, not chat history.
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# /done-day - End-of-Day Roll-Up

## When to invoke

User types `/done-day` (or "run done day" / "show me everything today"). Triggered after the user has run `/done` in each open tab and now wants a combined day total.

## Inputs

`~/.config/done/log.jsonl` - one JSON object per line, appended by every `/done` run. Schema:

```json
{"ts":"<ISO 8601>","user_slug":"<slug>","tab_id":"<workspace-or-session>","hours_total":N,"money_saved":N,"potential_low":N,"potential_high":N,"potential_ongoing_yearly":N,"items_done":[...],"items_open":[...]}
```

## Steps

1. Read `~/.config/done/log.jsonl`. If file missing or empty: tell the user "No /done entries logged today yet. Run /done in each tab first." and stop.
2. Filter entries to today's date (UTC or local, prefer local if tz info present).
3. Filter to current `user_slug` if multiple users share the log.
4. For each tab entry, render a small block:
   ```
   ### Tab: <tab_id>
   - Hours: <N>
   - Money saved: $<N>
   - Done: <count>, Open: <count>
   ```
5. Then a unified roll-up table:
   ```
   | Tab | Hours | Money saved | Potential earnings |
   |---|---|---|---|
   | <tab1_short> | 12.5 | $3,125 | $X to $Y |
   | <tab2_short> | 4.0 | $1,000 | $A to $B |
   | **Day total** | **N** | **$N** | **$M to $M direct, $K/yr ongoing** |
   ```
6. Then a deduplicated, day-level **All open items** list (across tabs) so the user sees everything still pending in one place.
7. End with one closing line: total hours, total money saved, total potential range, total ongoing yearly.

## Hard rules

- No em dashes anywhere
- Use the same $250/hr (or per-user rate from config) the original /done runs used. Don't recompute.
- If two tabs logged the same task title, dedup the open-items list but NOT the receipts (each tab earned its hours).
- Token-cheap: use Bash + jq, not LLM-parse the jsonl. Read structure, render markdown.

## Quick implementation hint

```bash
TODAY=$(date +%Y-%m-%d)
jq -c "select(.ts | startswith(\"$TODAY\"))" ~/.config/done/log.jsonl
```

That gives you all today's entries. Sum hours_total, money_saved, potential_low, potential_high, potential_ongoing_yearly. Done.
