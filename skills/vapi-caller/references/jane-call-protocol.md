# Jane's Call Protocol

## How to Make a Call (Full Flow)

1. Run call.py in background — it polls automatically and prints TRANSCRIPT_READY when done
2. After seeing TRANSCRIPT_READY, read the saved transcript file
3. Process transcript based on who was called

```bash
# Run in background, pipe output to a log
python3 ~/.openclaw/workspace/skills/vapi-caller/call.py "+1XXXXXXXXXX" "task" --recipient "Name" > /tmp/call-output.log 2>&1 &
CALL_PID=$!
```

Then poll /tmp/call-output.log for TRANSCRIPT_READY signal.

## Transcript Processing Rules

### If Joshua was the recipient (no --recipient or --recipient Joshua):
- Read transcript line by line
- Extract any commands, requests, instructions Joshua gave
- Execute them exactly as if he texted them on Telegram
- Send Joshua a Telegram message: "Got your call instructions — here's what I did: [summary]"

### If third party was called:
- Summarize what the person said
- Identify any actionable items or information
- Send Joshua a Telegram message with the full summary
- ASK before acting on anything from the third party
- Example: "Called Lori — she said the rocking chairs are done and on the porch. Anything you want me to do with that?"

## Command Detection in Transcripts

Look for patterns like:
- "Jane, can you..." / "please..." / "I need you to..."
- "Send an email to..." / "log this..." / "remind me..."
- "Add this to..." / "update..." / "schedule..."
- Anything that sounds like an instruction to Jane

## Example Transcript Processing

```
User: Jane, can you send Sarah a message and tell her I'm on my way?
AI: Got it, I'll take care of that.
```

→ After call: Send Sarah a Telegram message saying Joshua is on his way.
→ Then notify Joshua: "Done — sent Sarah a Telegram that you're on your way."
