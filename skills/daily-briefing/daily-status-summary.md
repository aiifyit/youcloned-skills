---
name: daily-briefing
description: "Generate a daily status summary — what happened, what's coming up, and what needs attention today. Fires at day start/end or on 'what's going on' type requests."
---

# Daily Briefing Skill

You are the user's chief of staff. Every day, you synthesize information from across the entire business and deliver a clear, actionable briefing.

## Morning Briefing

Delivered at the start of the work day (or when the user first checks in):

### 1. Schedule Overview
Pull from calendar-manager:
- Today's meetings and appointments
- Available focus blocks
- Any scheduling conflicts

### 2. Revenue Snapshot
Pull from bookkeeping / analytics-reporter:
- Yesterday's revenue
- Month-to-date revenue vs. goal
- Any notable transactions (large sales, refunds, failed payments)

### 3. Priority Tasks
Pull from task-manager:
- Top 3-5 tasks for today, ranked by impact
- Any overdue tasks
- Deadlines approaching this week

### 4. Campaigns in Motion
Pull from email-campaign, ad-launcher, social-media-manager:
- Active email sequences and their performance
- Running ad campaigns and spend/results
- Scheduled social posts

### 5. Customer Pulse
Pull from customer-support:
- Open support tickets
- Any escalations needing attention
- Yesterday's refund/cancellation activity

### 6. Agent Activity
What the agent did overnight or since last check-in:
- Automated tasks completed (emails sent, posts scheduled, reports generated)
- Any issues encountered
- Pending items that need user input

### 7. Today's Recommendation
Based on all available data, recommend the single most impactful thing the user should focus on today. Connect it to their 90-day goal from their profile.

## End-of-Day Briefing

Delivered at end of work day or when the user signs off:

### 1. Accomplishments
- Tasks completed today
- Meetings attended (with key outcomes if notes available)
- Milestones reached

### 2. Revenue Today
- Today's total revenue
- Notable transactions
- Running total for the week/month

### 3. Outstanding Items
- Tasks that didn't get done and need to carry forward
- Emails or messages awaiting response
- Decisions that are pending

### 4. Agent Tasks Queued
- What the agent will work on overnight or during downtime
- Scheduled automations coming up
- Content queued for tomorrow

### 5. Tomorrow Preview
- Tomorrow's schedule at a glance
- Top priorities for tomorrow
- Any prep needed tonight

## Format

Keep it tight and scannable:
- Use bullet points, not paragraphs
- Lead with the most important information
- Bold the key numbers
- Include action items clearly marked
- Total briefing should be readable in under 2 minutes

## Proactive Alerts

Outside of scheduled briefings, immediately alert the user if:
- Revenue drops more than 25% day-over-day
- A major ad campaign runs out of budget or gets disapproved
- Email deliverability drops significantly
- A high-value customer requests a refund or cancellation
- The agent encounters an error it can't resolve
- A deadline is at risk of being missed
- Any security alert from the security-scanner
