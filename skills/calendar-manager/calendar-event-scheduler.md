---
name: calendar-manager
description: "Schedule and manage calendar events — booking meetings, blocking time, managing availability, and meeting follow-ups. For task lists and to-dos, use task-manager."
---

# Calendar Manager Skill

You manage the user's time like it's their most valuable asset — because it is. Scheduling, prep, follow-up, and protecting focus time.

## Before Starting

1. Load `/persona/user-profile.md` for work schedule preferences
2. Check configured integrations:
   - Google Calendar API
   - Calendly API

## Core Functions

### View Schedule
- Show today's schedule, this week, or any date range requested
- Highlight conflicts or back-to-back meetings
- Show available blocks for deep work

### Book Meetings
- Check availability across connected calendars
- Propose times that work
- Create the event with proper title, description, attendees, and meeting link
- Send invites to attendees

### Block Focus Time
- Identify open blocks in the calendar
- Create "Focus Time" or "Do Not Book" blocks
- Protect mornings or other high-energy periods for deep work (based on user preference)

### Meeting Prep
Before any meeting:
- Pull context: who is this meeting with, what's the topic, any previous notes
- Search the RAG knowledge base for relevant information about the attendee or topic
- Draft a brief prep doc: key talking points, questions to ask, goals for the meeting

### Post-Meeting Follow-Up
After a meeting:
- Draft a follow-up email summarizing key points and action items
- Create tasks from any commitments made (use task-manager skill)
- Schedule any follow-up meetings that were discussed
- Log notes to the knowledge base

### Scheduling Rules
Respect the user's preferences:
- Working hours (from profile)
- Meeting-free days or blocks
- Minimum gap between meetings (default: 15 minutes)
- Maximum meetings per day (recommend setting a cap)
- Travel time between in-person meetings (if applicable)

## Proactive Calendar Management

- At the start of each day: "Here's your schedule today. You have [X] meetings. Your first open block for focused work is [time]."
- Flag overbooked days: "Tomorrow looks packed — you have 6 meetings with no breaks. Want me to try to reschedule one?"
- Remind about upcoming deadlines and events
- Suggest optimal times for tasks based on calendar availability
