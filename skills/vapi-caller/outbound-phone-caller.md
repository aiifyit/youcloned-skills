---
name: vapi-caller
description: "Make outbound phone calls via Vapi and Twilio. Fires when Joshua asks to call someone or relay a message by phone."
---

# Vapi Caller Skill

## Infrastructure
- **Script:** `~/.openclaw/workspace/skills/vapi-caller/scripts/call.py`
- **Vapi assistant ID:** `5844bf1a-19d8-4766-b6b7-62f1603f9949`
- **Twilio number:** `+16317355263` (SID: PN84cdffabd905def5bcc99cf9db785e0c)
- **Vapi phone number ID:** `0a30f779-63c6-4fe0-9450-07196b413d28`
- **API key:** in `~/.openclaw/workspace/.env.private` as `VAPI_API_KEY`

## Making a Call

### Call Joshua directly:
```bash
python3 ~/.openclaw/workspace/skills/vapi-caller/scripts/call.py "+18085008025" "task or topic"
```

### Call a third party on Joshua's behalf:
```bash
python3 ~/.openclaw/workspace/skills/vapi-caller/scripts/call.py "+1XXXXXXXXXX" "task description" --recipient "Name"
```

Always pass `--recipient "Name"` when calling anyone other than Joshua. This switches to the third-party prompt and hardcodes the correct greeting ("Hi [Name], this is Jane calling on behalf of Joshua Pellicer.").

## After Every Call — Mandatory Transcript Processing

Wait ~2 minutes after initiating a call, then poll:

```bash
curl -s "https://api.vapi.ai/call/{CALL_ID}" \
  -H "Authorization: Bearer {VAPI_KEY}"
```

Check `status` field. If `ended`, read the `transcript` field.

### If Joshua was called:
1. Parse transcript for any commands, instructions, or requests Joshua gave during the call
2. Execute them immediately — treat them exactly like Telegram messages from Joshua
3. Log the transcript to `~/.openclaw/workspace/memory/calls/YYYY-MM-DD-{call_id}.md`
4. Send Joshua a Telegram confirmation of what was done

### If a third party was called:
1. Parse transcript for key information, answers, or anything notable
2. Send Joshua a Telegram summary: who was called, what was said, anything actionable
3. If the third party gave instructions or requests — ask Joshua first before acting
4. Log the transcript to `~/.openclaw/workspace/memory/calls/YYYY-MM-DD-{call_id}.md`

## Call Logging

Save every transcript to: `~/.openclaw/workspace/memory/calls/YYYY-MM-DD-{call_id}.md`

Format:
```markdown
# Call — {Name} — {Date} {Time}
**Call ID:** {id}
**Direction:** Outbound
**Recipient:** {name or "Joshua"}
**Status:** {ended reason}

## Transcript
{full transcript}

## Actions Taken
{list of commands executed or summary sent}
```

## Known Contacts
- **Joshua Pellicer:** +18085008025
- **Lori:** +19046694589
- **Teeny:** +19045012919

## Vapi Behavior Notes
- 2-second wait before speaking is set at assistant level (startSpeakingPlan.waitSeconds: 2)
- Two separate system prompts: one for Joshua calls, one for third-party calls
- `firstMessage` is hardcoded per call type — never defaults to "Hey Joshua" for third parties
- See `references/prompts.md` for the full system prompts used

## Common Issues
- **"Hey Joshua" to third party:** Always pass `--recipient` flag — this is what switches the prompt
- **No transcript yet:** Call may still be in progress — wait 2 min and poll again
- **startSpeakingPlan not working via override:** Set at assistant level via PATCH `/assistant/{id}`, not in call overrides
