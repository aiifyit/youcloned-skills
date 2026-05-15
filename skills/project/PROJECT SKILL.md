---
name: project
description: Tag the current Claude Code tab to a project. Lists every active project from ~/.config/done/projects.json (auto-filters out completed ones), lets Jon pick or create a new one, then writes the tab-to-project tag so /done attributes session value to that project. Trigger on /project, "set project", "what project is this", "tag this tab".
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# /project - Tag this tab to a project

## What this does

When Jon types `/project`, this skill:

1. Reads the live list of active projects from `~/.config/done/projects.json`
2. Filters out anything with `status: completed` so closed projects do not appear
3. Shows Jon a numbered picker
4. Lets him pick an existing project OR create a new one
5. Writes a per-tab tag file at `~/.config/done/tabs/<session_id>.json` so `/done` knows which project this tab belongs to

A project is **active by default** when created. There is no "draft" or "ongoing" or any other state at creation time. Status is either `active` (created and not yet shipped) or `completed` (Jon checked it off). The Build Board's other tabs (in-progress, ready, blocked, someday, waiting) are display labels, not real states.

## Steps

### Step 1: List active projects

Run:
```bash
python3 ~/.claude/skills/project/project_lib.py list-active
```

This returns a JSON array of every project where `status != "completed"`. Each entry has `id`, `name`, `category`, `description`, `actual_hours`, `actual_money_saved`, `session_count`.

### Step 2: Show Jon the picker

Format as a clean numbered list. Show the project name + category + a one-line description hint. Keep it scannable. Append two extra options: a "new" option and a "skip" option.

Example shape:

```
Active projects:
1. SLIDR (Build) - VSL slide editor sold as $29 desktop app
2. The Bridge (Dashboard) - central command dashboard
3. Copy Analyzer (Build) - internal BNSN tool, paste copy and it decodes structure
...

N. + New project
S. Skip (don't tag this tab)

Pick a number, type "new <name>" to create one inline, or S to skip.
```

### Step 3: Handle the answer

**If Jon picks an existing number**: call set-tab with that project's id:
```bash
python3 ~/.claude/skills/project/project_lib.py set-tab <project_id>
```

**If Jon picks "new" or types `new <name>`**: gather these fields conversationally if not provided:
- name (required)
- description (one line, what is it)
- category (Build, Web, Product, Content, Infrastructure, Automation, Pending, Cleanup, Data, Dashboard)

Then create + auto-tag:
```bash
python3 ~/.claude/skills/project/project_lib.py create "<name>" "<description>" "<category>"
# get the new id from the JSON output, then:
python3 ~/.claude/skills/project/project_lib.py set-tab <new_id>
```

**If Jon picks Skip**: do nothing. Tell him the tab is untagged.

### Step 4: Confirm

After tagging, confirm in one line:

```
Tab tagged to <Project Name>. Every /done in this tab will attribute hours and money to that project.
```

If new project was created, also mention:
```
Created new project "<name>" (id: <id>, status: active). Will appear on the Build Board next refresh.
```

## How /done uses this tag

When `/done` runs, it calls:
```bash
python3 ~/.claude/skills/project/project_lib.py get-tab
```

If a project_id comes back, /done attributes that session's hours + money to the project via:
```bash
python3 ~/.claude/skills/project/project_lib.py add-totals <project_id> <hours> <money_saved> --pot-low <N> --pot-high <N>
```

The project's running totals (`actual_hours`, `actual_money_saved`, `actual_potential_low`, `actual_potential_high`, `session_count`) accumulate across every session tagged to it.

If no tag is set, /done runs as before with no project attribution.

## Marking complete

When Jon ships a project (checks the box on the Build Board), that calls:
```bash
python3 ~/.claude/skills/project/project_lib.py mark-completed <project_id>
```

The Build Board's checkbox handler should hit this when a row gets marked complete. Once completed, the project drops from /project's active list automatically.

## Hard rules

- **Active by default.** Never ask Jon to set a status when creating. Just create with `status: active`.
- **No em dashes anywhere** in any output to Jon.
- **Filter completed** before displaying the picker. Jon should never see shipped projects when picking what to work on.
- **One project per tab.** If Jon runs /project again in the same tab, it overwrites the tag (idempotent switch).
- **Sticky tag.** Once tagged, the tab stays attributed to that project across multiple /done runs until Jon /project switches it.
