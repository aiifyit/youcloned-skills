---
name: weekly-focus
description: "Weekly business focus diagnostic - asks targeted questions about the business, constraints, current numbers, opportunities, and founder capacity, then recommends the single highest-leverage focus for this week. Does not manage tasks, run analytics, or build the work; it narrows what deserves attention now."
---

# Weekly Focus Skill

Use this skill when the user wants to decide what to work on this week, feels scattered, has too many business options, or asks what the business should prioritize next.

The goal is not to create a long plan. The goal is to ask enough specific questions to find the one focus that is most likely to move the business forward this week.

## Operating Rule

Do not answer with generic advice before asking questions. Run the diagnostic first unless the user already provided enough current business context.

If the user answers briefly, continue with the best available signal instead of forcing a long interview.

## Question Flow

Ask the questions in small batches. Start with the first six. Only ask follow-ups when an answer is missing or unclear.

### 1. Business Snapshot

1. What is the business, offer, or project you are trying to grow right now?
2. Who is the specific customer or buyer?
3. What do you sell, at what price, and how do people buy it?
4. What is the current stage: idea, validation, first sales, repeatable sales, scaling, or cleanup?
5. What is the main business goal for the next 30 days?
6. What would make this week feel like a clear win?

### 2. Current Numbers

7. How many leads, calls, trials, purchases, or active customers came in during the last 7 days?
8. What revenue came in during the last 7 days?
9. What conversion step is weakest right now: attention, lead capture, sales call booking, closing, delivery, retention, or referrals?
10. What metric are you already watching, if any?

### 3. Bottlenecks

11. What is currently blocking growth the most?
12. Where are prospects or customers getting stuck?
13. What have you been avoiding because it feels uncomfortable, tedious, or uncertain?
14. What repeats every week and keeps consuming time?

### 4. Opportunities

15. What opportunity is already warm: a list, audience, partner, client, product, asset, or channel?
16. What could create revenue fastest if handled this week?
17. What would compound if you built or fixed it now?
18. What existing asset is underused?

### 5. Capacity and Constraints

19. How many focused hours do you realistically have this week?
20. What fixed obligations, deadlines, or personal constraints matter this week?
21. What can only you do?
22. What could be delegated, automated, postponed, or ignored?

### 6. Decision Pressure

23. If you did only one business thing this week, what are the top three candidates?
24. Which candidate has the shortest path to cash, proof, or risk reduction?
25. Which candidate would make next week easier?
26. Which candidate would be painful to leave untouched for another week?

## Scoring

After the questions, score each candidate focus from 1 to 5:

- **Revenue proximity:** How directly it can create or protect revenue this week.
- **Bottleneck removal:** How much it unlocks stuck work or stuck buyers.
- **Compounding value:** How much it makes future weeks easier.
- **Founder fit:** How well it matches the user's available hours, energy, and unique role.
- **Risk reduction:** How much uncertainty it removes.

Prefer the focus with the strongest combined score. If scores are close, choose the one with the shortest path to proof or cash.

## Output Format

Return the recommendation in this structure:

```markdown
## This Week's Focus

**Focus:** <one clear priority>

**Why this:** <2-4 sentences tying it to the user's answers>

**What not to focus on:** <1-3 items to consciously ignore this week>

**Success by Friday:** <measurable outcome>

**First action:** <specific next action that can be started today>

**Guardrail:** <constraint that keeps the week from expanding into too many projects>
```

## Rules

- Pick one primary focus, not three.
- Do not create a full task list unless the user asks after the focus is chosen.
- Do not use vague priorities like "marketing" or "sales"; name the exact lever.
- If the business is pre-revenue, favor validation, offers, conversations, and proof over infrastructure.
- If the business has traffic but low sales, favor conversion and offer clarity.
- If the business has sales but delivery is breaking, favor fulfillment, retention, and operational cleanup.
- If the founder has very limited time, choose a smaller focus with a visible finish line.
- If there is no usable data, choose the focus that will create the most useful data this week.
