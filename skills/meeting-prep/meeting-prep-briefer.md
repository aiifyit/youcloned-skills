---
name: meeting-prep
description: "Pre-meeting preparation briefs for any calendar event — attendee research, talking points, and context. For AIify client meetings specifically, use aiify-intel instead."
---

# Meeting Prep Skill

## What It Does
30 minutes before each calendar event, Jane:
1. Detects the upcoming meeting via Google Calendar (joshua@pellicerlife.com)
2. Researches attendees using Brave Search
3. Pulls relevant context from MEMORY.md
4. Generates a 3-bullet prep brief via Claude Haiku
5. Sends the brief to Joshua on Telegram

## Files
- **Script:** `~/Projects/jane-meeting-prep/prep.py`
- **LaunchAgent:** `~/Library/LaunchAgents/com.jane.meeting-prep.plist`
- **Logs:** `~/Projects/jane-meeting-prep/prep.log`
- **Lock files:** `~/.openclaw/workspace/.meeting-prep-<eventId>.sent`

## Running Manually

```bash
# Check current upcoming events (30-65 min window) and send briefs
python3 ~/Projects/jane-meeting-prep/prep.py

# Test mode: fetch tomorrow's calendar events, generate briefs (no send)
python3 ~/Projects/jane-meeting-prep/prep.py --test

# Test + send: generate for tomorrow's events AND send to Telegram
python3 ~/Projects/jane-meeting-prep/prep.py --test-send

# Demo mode: use known Mar 23 meetings (no calendar needed)
python3 ~/Projects/jane-meeting-prep/prep.py --demo
```

## Cron Schedule
Runs every 5 minutes via launchd (StartCalendarInterval).

Manage with:
```bash
launchctl load ~/Library/LaunchAgents/com.jane.meeting-prep.plist
launchctl unload ~/Library/LaunchAgents/com.jane.meeting-prep.plist
launchctl list | grep meeting-prep
```

## Calendar Note
Currently reads from `joshua@pellicerlife.com` calendar (shared to jane@pellicerlife.com).
If meetings appear in `joshua@aiifyit.com`, add that refresh token to gog-wrapper.sh
and update `CALENDAR_ID` in prep.py.

## Brief Format
```
📋 Meeting Prep — [Title] at [Time]

• [Who you're meeting and their key context]
• [Most important talking point or goal]
• [One concrete action or thing to watch for]
```

## Deduplication
Lock files prevent sending the same brief twice:
`~/.openclaw/workspace/.meeting-prep-<eventId>.sent`

Clean old locks manually or they expire naturally (event IDs are unique per event).
