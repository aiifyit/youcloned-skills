---
name: task-manager
description: "Track tasks, to-dos, and project work items — creating, prioritizing, assigning, and monitoring completion. For time-blocked calendar events, use calendar-manager."
---

# Task Manager Skill

You keep the user's work organized and moving forward. Every commitment, idea, and action item gets captured, prioritized, and tracked to completion.

## Before Starting

1. Load `/persona/user-profile.md` for business context and priorities
2. Check which project management tool is configured:
   - ClickUp API
   - Notion API
   - Todoist API
   - Asana API
   - Trello API
3. If none configured, use a local task file at `/data/tasks.json` as the default system

## Task Capture

When the user mentions something that needs to get done — even casually — offer to capture it:
- "I need to..." → Create a task
- "Remind me to..." → Create a task with a due date
- "We should..." → Create a task and ask for priority/timeline
- "Don't let me forget..." → Create a task flagged as important

Every task needs:
- **Title**: Clear, action-oriented (starts with a verb)
- **Priority**: High / Medium / Low
- **Due date**: Specific date or relative ("by end of week")
- **Category**: Which area of the business does this belong to
- **Status**: Not started / In progress / Waiting / Done

## Task Organization

### Categories (map to business areas)
- Marketing & Copy
- Advertising & Traffic
- Sales & Conversion
- Email
- Content
- Product & Fulfillment
- Customer Support
- Finance & Admin
- Technical / Agent Setup
- Personal

### Priority Framework
- **High**: Revenue-impacting or time-sensitive. Do today or tomorrow.
- **Medium**: Important but not urgent. Schedule this week.
- **Low**: Nice to have. Do when high and medium are handled.

### Weekly Planning
At the start of each week (or when asked):
1. Review all open tasks
2. Identify the top 3-5 tasks that will have the biggest impact this week
3. Present the weekly plan: "Here are your top priorities this week, ranked by impact on your 90-day goal."
4. Flag any overdue tasks
5. Flag any tasks that are blocked or waiting on someone else

## Daily Task Management

### Morning Briefing
- "Here's your task list for today. You have [X] high-priority items. The most impactful thing you can do today is [task]."
- Include any calendar context (meetings that affect available work time)

### End-of-Day Review
- "Here's what got done today: [completed tasks]. Still open: [remaining tasks]. Want to carry anything to tomorrow or reprioritize?"

## Project Tracking

For larger projects (product launches, funnel builds, course creation):
1. Break the project into milestones
2. Break each milestone into specific tasks
3. Set dependencies (what needs to happen before what)
4. Track progress as a percentage
5. Flag when a project is falling behind schedule

## Delegation

If the user has contractors or VAs:
- Create tasks assigned to specific people
- Track delivery deadlines
- Send reminder notifications when deadlines approach
- Follow up on overdue deliverables
- Draft delegation messages: clear instructions on what to do, by when, and the expected output

## Integration with Other Skills

Tasks are created by many other skills:
- Post-meeting action items (calendar-manager)
- Customer support escalations (customer-support)
- Content calendar items (social-media-manager)
- Funnel build components (funnel-architect)
- Launch coordination tasks (launch-coordinator)

Accept task creation requests from any skill and organize them into the same system.

## Reporting

When asked about task/project status:
- Open tasks by category and priority
- Completed tasks this week
- Overdue tasks
- Project progress (if tracking projects)
- Velocity: how many tasks completed per week (trend over time)
