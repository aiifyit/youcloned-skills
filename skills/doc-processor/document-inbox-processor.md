---
name: doc-processor
description: "Process documents dropped into the inbox folder — PDFs, receipts, contracts. Extracts key info, files it, and flags action items."
---

# Document Processor Skill

## Paths
- **Inbox:** `~/Documents/Jane Inbox/` — Joshua drops files here
- **Archive:** `~/Documents/Jane Archive/{category}/` — filed after processing
- **Script:** `~/Projects/jane-docs/run.sh` (uses venv with pdfplumber + anthropic)
- **Log:** `~/Projects/jane-docs/processed.json` — full history of all processed docs

## Categories
`finance` | `legal` | `health` | `business` | `personal` | `other`

## Supported File Types
- PDF (text-based, uses pdfplumber)
- TXT, MD, CSV (read directly)
- Other binary files (flagged by filename only)

## How to Run

### Process inbox manually
```bash
cd ~/Projects/jane-docs && ./run.sh
```

### Check for files in inbox (heartbeat)
```bash
ls ~/Documents/Jane\ Inbox/ | grep -v '^\.' | wc -l
```

### View processed log
```bash
cat ~/Projects/jane-docs/processed.json | python3 -m json.tool | tail -50
```

## When Called by Jane

1. Check if any files exist in `~/Documents/Jane Inbox/`
2. If yes, run: `cd ~/Projects/jane-docs && ./run.sh`
3. Parse results and report to Joshua:
   - How many processed
   - Type and summary of each
   - ⚠️ Any action items (with priority and due dates)
4. If action items found and Joshua is reachable, send Telegram alert

## Example Output
```
Processing: invoice-march2026.txt
  → [invoice] Invoice from Coastal Web Design LLC for $1,321.45
  → Filed: ~/Documents/Jane Archive/finance/invoice-march2026.txt
  ⚠️  ACTION (medium): Pay $1,321.45 by April 5 via Zelle to avoid late fees
```
