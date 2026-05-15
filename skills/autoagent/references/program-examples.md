# program.md Examples for Pulse / AIify

Copy and adapt these directives into `program.md` for each AutoAgent experiment.

---

## General Capable Agent (Baseline)

```markdown
# autoagent

Autonomous agent engineering. You are a professional agent harness engineer and
a meta-agent that improves an AI agent harness.

## Directive

Build a generally capable autonomous coding and terminal agent.

The agent receives a natural-language task instruction, works inside a sandboxed
environment, and must produce the correct final artifact or system state.

Do NOT change the model from `gpt-5` unless explicitly asked.

## Goal

Maximize the number of passed tasks.
```

---

## Pulse Sales Agent

```markdown
# autoagent — Pulse Sales

## Directive

Build a sales qualification and follow-up agent for SMB businesses.

The agent receives inbound lead data (name, company, notes from a form or CRM)
and must:
1. Score the lead (hot / warm / cold) with reasoning
2. Draft a personalized outreach email
3. Suggest a next action (call, demo, nurture sequence)

Evaluation: task-specific verifiers check lead score accuracy and email quality rubric.

Do NOT change the model unless explicitly asked.

## Goal

Maximize passed tasks. Prioritize lead scoring accuracy over email verbosity.
```

---

## Pulse Ops Agent

```markdown
# autoagent — Pulse Ops

## Directive

Build an operations routing and SOP execution agent for SMB businesses.

The agent receives inbound requests (support tickets, internal requests, task descriptions)
and must:
1. Classify the request type
2. Assign it to the correct team/role
3. Output the first 3 steps of the relevant SOP

Evaluation: verifiers check classification accuracy and SOP step correctness.

Do NOT change the model unless explicitly asked.

## Goal

Maximize passed tasks. Prioritize correct routing over verbose SOP output.
```

---

## Pulse Finance Agent

```markdown
# autoagent — Pulse Finance

## Directive

Build a financial reconciliation and anomaly detection agent for SMB businesses.

The agent receives transaction data (CSV or JSON) and must:
1. Categorize each transaction
2. Flag anomalies (duplicate charges, unusual amounts, uncategorized items)
3. Produce a summary P&L by category

Evaluation: verifiers check categorization accuracy and anomaly detection recall.

## Goal

Maximize passed tasks. Prioritize anomaly recall (don't miss flags) over precision.
```

---

## Pulse Customer Success Agent

```markdown
# autoagent — Pulse CS

## Directive

Build a customer support triage and response agent for SMB businesses.

The agent receives support tickets (text) and must:
1. Classify urgency (critical / high / normal / low)
2. Identify the issue category
3. Draft a response or escalation note

Evaluation: verifiers check urgency classification and response relevance.

## Goal

Maximize passed tasks. Never misclassify a critical ticket as lower urgency.
```
