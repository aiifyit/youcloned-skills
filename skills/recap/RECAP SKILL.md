---
name: recap
description: Full session recap that bypasses context compaction by reading the raw transcript from disk. Outputs the WHY behind the work (the business outcome, not the tool), a guiding principle for the rest of the project, every phase of what got done with a Summary + bullets, and an explicit "Here's What's Next". Trigger on /recap.
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# /recap - Total Session Recap (Bypasses Compaction)

## Why this skill exists

Claude Code compacts long sessions to save context. The compacted portion still exists on disk in the session JSONL file, but it's not visible in chat anymore. `/recap` reads from disk to reconstruct the FULL session, then summarizes it in a structure that keeps the project moving forward.

The goal is not "list everything that happened." The goal is to surface the **WHY** behind the work, lock in the **operating principle** for the rest of the project, and tell you **what's next**.

This format was designed for entrepreneurs and operators who run long, multi-thread sessions with Claude Code. It forces the AI to remember the business outcome, not just the tool it built.

## When to invoke

User types `/recap` (or says "give me a total recap" / "recap this tab"). Produce the recap immediately. Don't ask clarifying questions unless the session is truly empty (less than 5 message turns).

Optional argument: `/recap <session_id>` to recap a specific past session by its UUID. Default = current session.

## Where the data comes from

Claude Code auto-saves every message to a JSONL file at:

```
~/.claude/projects/<sanitized-cwd>/<session_id>.jsonl
```

The sanitized cwd is your working directory with `/` replaced by `-`. Example: `/Users/jane/projects/myapp` becomes `-Users-jane-projects-myapp`.

To find the current session JSONL:

```bash
# Find the project folder for the current working dir
CWD_SLUG=$(pwd | sed 's|/|-|g')
PROJECTS_DIR="$HOME/.claude/projects/$CWD_SLUG"

# Get the most recently modified JSONL (= current session)
CURRENT_JSONL=$(ls -t "$PROJECTS_DIR"/*.jsonl 2>/dev/null | head -1)
SESSION_ID=$(basename "$CURRENT_JSONL" .jsonl)
```

If you've wired your sessions to a database (Supabase, Postgres, SQLite), prefer querying that. The JSONL is the universal fallback - every Claude Code user has it.

## Output format (EXACT structure required)

### 1. The WHY (one sentence)

A single sentence answering: "I'm doing this because [user] wants ___."

Rules for the WHY:
- Not "[user] wants a tool" - that's surface. Name the BUSINESS outcome underneath the tool.
- Not "[user] wants a feature" - name what the feature unlocks (revenue, retention, scale, trust).
- Two outcomes can be combined with AND if both clearly drove the session.
- Format: "[User] wants [outcome A], AND [outcome B if applicable] - because [the cost of not having it]."

Examples of good WHY statements:
- "[User] wants every customer to feel like they joined ONE brand with ONE login - because broken onboarding costs the same as broken AI: revenue already paid CAC to earn."
- "[User] wants the sales page to convert at 2%+ on cold traffic - because the difference between 1% and 2% is the difference between a self-funding business and a money pit."
- "[User] wants the deploy pipeline to never destroy uncommitted work again - because the last incident cost a full day of design iteration."

### 2. Therefore, for the rest of this project, I will think in terms of:

A guiding principle paragraph (2-4 sentences) that crystallizes how the AI should operate for the duration of this project based on what the WHY revealed.

Format: "**Therefore, for the rest of this project, I will think in terms of:**" followed by the principle.

Example:
> Therefore, for the rest of this project, I will think in terms of: every action either protects the customer's seamless one-brand experience or breaks it. Every action either earns the user's trust or burns it. The tool is never the goal - the business outcome behind the tool is the goal. Verify before claiming. Commit before destroying. Read the spec before saying "can't."

### 3. Total Session Recap

Group the session into 5-12 phases by topic shift (not by time). Each phase gets:

```
### Phase N - [Phase title]

**Summary:** 1-2 sentence plain-English description of what was done in this phase and why it mattered.

- Bullet 1: specific decision, code change, or fact
- Bullet 2: specific decision, code change, or fact
- Bullet 3 (etc.)
```

Phase header rules:
- Title should describe the OUTCOME of the phase, not the activity. "Setup page architecture" not "I built a setup page."
- Mark mistakes or disasters explicitly in the title ("Phase X - The deploy script disaster") so they're not glossed over.
- If a phase cost time due to AI error, name it ("cost 4 hours due to my error") and explain the lesson.

Summary rules:
- 1-2 sentences max. No bullets in the summary itself.
- Plain English, no AI-isms.
- Should answer: "What got done, and why did it matter?"

Bullet rules:
- Specific facts, decisions, file paths, API endpoints, command names, error messages.
- No filler ("worked on X" -> "fixed `skip_invitation` field name in setup-page/server.py").
- Include rules and decisions that got locked in.

### 4. Here's What's Next

End with this exact header. Then one of two patterns:

**Pattern A - Repeat back what the user said:**
If the user explicitly listed next steps anywhere in the session, repeat them grouped by timing:

```
### Immediate (this conversation):
- ...

### Tomorrow:
- ...

### This week:
- ...

### When the user says go:
- ...

### Cleanup:
- ...
```

**Pattern B - Infer from the WHY:**
If the user didn't explicitly say what's next, propose 2-4 next steps that directly serve the WHY. Phrase each as a verb-first action with the reason it serves the outcome.

Always end with a single line asking for confirmation:
"Did I land it? If yes, [propose the immediate next action]."

## Hard rules

- **No em dashes.** Use hyphens, colons, ellipses, or new sentences.
- **No openers that announce the next sentence is real, direct, candid, or unfiltered.** Just state the thing.
- **Never invent phases that didn't happen.** If the session was short, output fewer phases. Don't pad.
- **Never gloss over AI mistakes.** If you burned 4 hours on something, name it in a phase header and explain the lesson learned.
- **Don't list what's still open INSIDE the phase summaries.** Open items go ONLY in "Here's What's Next."
- **Every phase summary is 1-2 sentences max.** If the phase needs more, split it into two phases.

## Implementation

When invoked, execute this flow:

### Step 1: Find the session JSONL

```bash
CWD_SLUG=$(pwd | sed 's|/|-|g')
PROJECTS_DIR="$HOME/.claude/projects/$CWD_SLUG"
CURRENT_JSONL=$(ls -t "$PROJECTS_DIR"/*.jsonl 2>/dev/null | head -1)
SESSION_ID=$(basename "$CURRENT_JSONL" .jsonl)
```

If the user passed a session_id argument, use it instead. Look in `$PROJECTS_DIR` for matching `<session_id>.jsonl`.

### Step 2: Read the transcript

The JSONL is one JSON object per line. Each line has `message.role` (user/assistant) and `message.content` (text or tool calls). Read line by line - the file can be massive (millions of tokens).

Useful filters:
- User messages: `jq -r 'select(.message.role=="user") | .message.content'`
- Assistant text: extract `.message.content[].text` where `.type == "text"`
- Tool calls: extract `.message.content[]` where `.type == "tool_use"` (gives you what files got edited, what commands ran)

### Step 3: Analyze and group into phases

Scan the messages for topic shifts:
- New user messages that introduce a new subject ("now let's work on X")
- Tool-call clusters around a specific file or system
- Error -> fix -> retry sequences (these often deserve their own phase)
- Decision moments ("let's do X", "decision: Y")

Each detected topic cluster becomes a phase. Order phases chronologically.

### Step 4: Extract the WHY

Look for:
- The original user request at the very start of the session (or after the last context compaction)
- Strategic statements from the user mid-session ("I want every buyer to...", "the reason we're doing this is...")
- The cost or pain mentioned (refunds, support tickets, lost time, low conversion)

Distill into ONE sentence that captures the business outcome, NOT the tool.

### Step 5: Compose the guiding principle

Based on the WHY, write the "Therefore, I will think in terms of" paragraph. This should crystallize:
- What to prioritize for the rest of the project
- What to avoid (especially mistakes made in this session)
- The lens through which every future decision should be made

### Step 6: Output in the exact format above

Render the full recap. Don't ask permission to render - render it.

## Optional: Persist the recap

If you have a database wired up (Supabase, SQLite, Postgres), save the distilled summary so future `/recap` calls or other tools can use it without re-reading the full transcript. Suggested schema:

```sql
CREATE TABLE session_recaps (
  session_id TEXT PRIMARY KEY,
  generated_at TIMESTAMPTZ DEFAULT now(),
  why TEXT,
  principle TEXT,
  phase_count INT,
  full_recap_md TEXT,
  next_steps JSONB
);
```

This is optional - the recap output to chat is the primary deliverable.

## Why this format works

Most session-summary tools list **what** got done. They miss **why** it mattered and **how** the AI should behave going forward.

This format forces three things:
1. **Business outcome focus** - the WHY anchors every recap to revenue, retention, scale, or trust. Not features.
2. **Operating principle** - the "Therefore I will think in terms of" line locks in how the AI shows up for the rest of the project. It carries forward across compactions.
3. **Explicit next step** - the recap ends with action, not nostalgia.

Use `/recap` at the end of any long session, before context compaction, or whenever you feel the AI has lost the plot. The output is portable - paste into Slack, Notion, project notes, or feed it as context into the next session.
