---
name: skill-router
description: "Multi-skill coordination hub — use only when a request clearly spans multiple business areas or the correct skill is genuinely ambiguous after reviewing the skill list."
---

# Skill Router

## How to Route

### Step 1 — Haiku Skill Selection (always first)

Before doing anything else, spawn a one-shot Haiku call whose only job is to identify which skill(s) apply. It does not decide complexity, execution strategy, or whether to spawn — that's handled downstream by the routing logic below.

```
sessions_spawn(
  runtime="subagent",
  mode="run",
  model="haiku",
  task="""
You are a skill selector. Given the user request, identify which skill(s) apply and score the complexity.
Output ONLY valid JSON — no explanation, no markdown, nothing else.

{
  "skill_needed": true | false,
  "primary": "skill-name or null",
  "sequence": ["skill-1", "skill-2"] or [],
  "complexity_score": <integer 1-100>
}

Complexity scale:
  1–20   = simple enough to handle inline (lookup, single file, short draft)
  21–100 = needs Claude Code (anything multi-step, multi-file, research, builds, API work, debugging)

Available skills: copywriting, page-builder, funnel-architect, email-campaign, ad-launcher,
social-media-manager, content-repurposer, affiliate-manager, sales-conversion, customer-onboarding,
customer-support, bookkeeping, analytics-reporter, calendar-manager, task-manager, sop-builder,
legal-doc-generator, offer-architect, lead-magnet-creator, rag-knowledge-manager, daily-briefing,
launch-coordinator, split-test-manager, voice-and-brand, self-repair, content-delivery,
api-vault, security-scanner, gym-workout-logger

User request: {user_request}
"""
)
```

### Step 2 — Apply routing logic based on Haiku's output

| skill_needed | complexity_score | Action |
|---|---|---|
| false | any | Respond inline, no skill needed |
| true | 1–20 | Read skill file, handle inline |
| true | 21–100 | Read skill file, spawn Claude Code (`runtime="acp"`) |

### Step 3 — Pass context forward

When handing off to the next skill in a sequence, include what the previous skill produced. The receiving skill should never have to ask "what came before me."

---

## Routing Logic

### Single-Skill Requests
Most requests map to one skill. Route directly:

| Request Pattern | Route To |
|---|---|
| Write copy, VSL, sales page text | copywriting |
| Build/design a web page | page-builder |
| Plan a funnel flow | funnel-architect |
| Email sequence, broadcast, list management | email-campaign |
| Run ads, ad creative, ad budget | ad-launcher |
| Social media posting, content calendar | social-media-manager |
| Break down long-form content | content-repurposer |
| Affiliate program, swipe files, commissions | affiliate-manager |
| Close deals, checkout, upsells, CRM | sales-conversion |
| New customer experience after purchase | customer-onboarding |
| Customer questions, refunds, tickets | customer-support |
| Revenue, expenses, invoices, taxes | bookkeeping |
| Metrics, KPIs, dashboards, performance | analytics-reporter |
| Schedule, meetings, calendar | calendar-manager |
| Tasks, to-dos, projects, deadlines | task-manager |
| Document a process, create instructions | sop-builder |
| Legal documents, TOS, privacy policy | legal-doc-generator |
| New product, pricing, offer structure | offer-architect |
| Free opt-in, lead magnet, checklist | lead-magnet-creator |
| Knowledge base, upload docs, second brain | rag-knowledge-manager |
| Daily status, morning briefing | daily-briefing |
| Product launch coordination | launch-coordinator |
| A/B test, split test | split-test-manager |
| Brand voice, tone adjustment | voice-and-brand |
| Something's broken, fix this | self-repair |
| Course content, membership, delivery | content-delivery |
| API keys, credentials, secrets | api-vault |
| Install something, download, new package | security-scanner |

### Multi-Skill Workflows
Some requests require a chain of skills. Common sequences:

**"Create a complete funnel for my new product"**
1. offer-architect → Define the offer
2. funnel-architect → Design the funnel flow
3. copywriting → Write all the copy
4. page-builder → Build all the pages
5. email-campaign → Create the email sequences
6. sales-conversion → Set up checkout and upsells

**"Launch my new course"**
1. launch-coordinator → Create the launch plan (this skill then coordinates the rest)
2. All other skills as directed by the launch plan

**"I recorded a podcast, get it everywhere"**
1. content-repurposer → Break into multiple content pieces
2. social-media-manager → Schedule social posts
3. email-campaign → Send newsletter about the episode

**"Help me start my business from scratch"**
1. offer-architect → Define what to sell
2. lead-magnet-creator → Create the free entry point
3. funnel-architect → Design the funnel
4. copywriting + page-builder → Build it out
5. email-campaign → Set up welcome and nurture sequences
6. Everything else follows

**"I need to improve my conversion rate"**
1. analytics-reporter → Diagnose where the leak is
2. split-test-manager → Set up tests on the weak point
3. copywriting or page-builder → Create variants
4. analytics-reporter → Monitor results

### Ambiguous Requests
When it's unclear which skill should handle something:

1. Check the user profile for context (what are they working on currently?)
2. Ask a brief clarifying question if necessary — but try to route intelligently based on context before asking
3. When in doubt, route to the skill that handles the highest-level version of the request (e.g., "help with my marketing" → start with analytics-reporter to diagnose, then route to specific skills based on findings)

## Priority Rules

When multiple skills could trigger simultaneously:
1. **Security scanner** ALWAYS runs first if an installation or download is involved
2. **API vault** ALWAYS runs if credentials are detected
3. **Self-repair** takes priority if something is broken
4. For everything else, route to the most specific skill, not the most general one

## Model Policy

| Step | Model | Why |
|---|---|---|
| Routing / classification | Haiku | Classification is not reasoning — keep it cheap and fast |
| Simple skill execution (inline) | Sonnet 4.6 (session default) | Already in context, no spawn needed |
| Complex skill execution (subagent) | Sonnet 4.6 | Full reasoning power for real work |

Never use Sonnet just to decide which skill to invoke. Never use Haiku to do the actual work.

## Context Awareness

Maintain awareness of what the user has been working on in this session. If they've been building a funnel and say "now do the emails," you know to route to email-campaign with the funnel context, not ask "what emails?"

Pass relevant context between skills when handing off — the receiving skill should know what happened before it was invoked.
