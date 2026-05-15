---
name: sop-builder
description: "Document repeatable processes as written SOPs, VA instructions, or workflow guides. Not for tracking tasks or scheduling — for capturing how something is done so others can replicate it."
---

# SOP Builder Skill

Every process the user describes or performs should be capturable as a repeatable SOP. Your job is to turn messy, in-their-head knowledge into clear, step-by-step documentation that anyone (or any agent) could follow.

## Before Starting

1. Load `/persona/user-profile.md` for business context
2. Determine who the SOP is for:
   - A human team member or VA → Write for a person, include context and screenshots references
   - The AI agent itself → Write as a skill file (.md) that can be added to OpenClaw
   - Both → Create two versions

## Capturing the Process

If the user is describing a process verbally or through chat:

1. Listen to the full description first — don't interrupt to document
2. Ask clarifying questions:
   - "What triggers this process? When does it start?"
   - "Are there any decision points where different things could happen?"
   - "What tools or systems are involved?"
   - "What does 'done' look like? How do you know it's complete?"
   - "How often does this happen?"
   - "What are the common mistakes or edge cases?"
3. Draft the SOP and present it for review
4. Iterate until the user confirms it's accurate

## SOP Format

```markdown
# [Process Name]

## Overview
- **Purpose**: Why this process exists
- **Trigger**: What kicks it off
- **Frequency**: How often it runs
- **Owner**: Who is responsible
- **Tools needed**: What systems/accounts are required
- **Estimated time**: How long it takes

## Prerequisites
- [ ] What needs to be true before starting
- [ ] What access/permissions are needed
- [ ] What information needs to be gathered first

## Steps

### Step 1: [Action]
Detailed instructions for this step.
- Substep if needed
- Substep if needed
**Expected result**: What should be true after this step

### Step 2: [Action]
...

## Decision Points
- **If [condition]**: Do [action A]
- **If [other condition]**: Do [action B]

## Quality Checklist
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Troubleshooting
- **Common issue 1**: How to fix it
- **Common issue 2**: How to fix it

## Notes
- Any additional context, tips, or warnings
```

## Storage

Save SOPs to `/data/sops/[process-name].md`

Maintain an index at `/data/sops/INDEX.md` listing all SOPs with:
- Process name
- Category (marketing, sales, operations, finance, support, technical)
- Last updated date
- Who it's for (human, agent, or both)

## Converting SOPs to Skills

If an SOP describes something the agent should do automatically:
1. Rewrite it as a SKILL.md file with proper frontmatter
2. Add trigger descriptions so the agent knows when to invoke it
3. Add the skill to the OpenClaw skills directory
4. Test it by walking through the process

## SOP Maintenance

- Flag SOPs for review every 90 days
- When a tool or process changes, update the affected SOPs
- When the user describes doing something differently than an existing SOP, ask: "Your current SOP says to do [X], but you just did [Y]. Should I update the SOP?"
