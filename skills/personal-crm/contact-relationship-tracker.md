---
name: personal-crm
description: "Contact relationship management — logging past interactions, tracking relationship history, and setting follow-up reminders for Joshua's network. Not for meeting prep; for ongoing relationship tracking."
---

# Personal CRM Skill

## Database
- **DB file:** `~/Projects/jane-crm/contacts.db`
- **CLI:** `/opt/homebrew/bin/python3 ~/Projects/jane-crm/crm.py`

## Common Commands

```bash
# List all contacts with warmth indicators
python3 ~/Projects/jane-crm/crm.py list

# Search for a contact
python3 ~/Projects/jane-crm/crm.py search "Lori"

# Full relationship brief before a meeting
python3 ~/Projects/jane-crm/crm.py brief "Charles Byrd"

# Pending follow-ups (check daily)
python3 ~/Projects/jane-crm/crm.py followups

# Dormant contacts (not reached in 30+ days)
python3 ~/Projects/jane-crm/crm.py dormant --days 30

# Add a new contact
python3 ~/Projects/jane-crm/crm.py add "Jane Smith" --email jane@example.com --relationship business --notes "Met at conference"

# Log an interaction
python3 ~/Projects/jane-crm/crm.py log "Charles Byrd" --type call --summary "Discussed AI project roadmap" --sentiment positive

# Add a follow-up reminder
python3 ~/Projects/jane-crm/crm.py followup-add "Jon Benson" --due 2026-03-25 "Schedule call re: Entrepreneur opportunity"

# Mark follow-up done
python3 ~/Projects/jane-crm/crm.py done <id>

# Re-import from call transcripts
python3 ~/Projects/jane-crm/crm.py import-calls

# Stats overview
python3 ~/Projects/jane-crm/crm.py stats
```

## Relationship Types
- `family` — Joshua's family members
- `friend` — Personal friends
- `business` — Business contacts, clients, collaborators
- `vendor` — Wedding/honeymoon/service vendors
- `other` — New or uncategorized contacts

## Warmth Scale
- 🔥 Contacted within 7 days — hot
- 🟡 8–30 days — warm
- 🟠 31–90 days — cooling
- ❄️  90+ days or never — cold/dormant

## Auto-Import
Call transcripts in `~/.openclaw/workspace/memory/calls/processed/*.json` are
auto-parsed. Run `import-calls` after new calls are processed.

## Heartbeat Integration
The morning heartbeat checks for:
1. Follow-ups due today
2. Contacts dormant >30 days

## Known Contacts (as of 2026-03-22)
- Sarah Lemay (fiancée) — sarahlemay01@gmail.com
- Gabe Pellicer (family) — pellicer22@gmail.com
- Charles Byrd (business) — charles@charlesbyrd.com, Mon 2:30pm sync
- Jon Benson (business/prospect) — jb@jonbenson.com
- Sami Begg (AIify) — sami@aiifyit.com
- Jim & Jamie Shiels (other) — met Llama Restaurant Mar 18
- Barrett (business) — Tennessee property advisor
- Jason Tesauro (other) — Verona dinner Oct 5 honeymoon
- Lori (family) — +19046694589
- Teeny (friend) — +19045012919
- Joshua Pellicer (primary) — joshua@aiifyit.com
