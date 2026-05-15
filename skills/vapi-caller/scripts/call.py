#!/usr/bin/env python3
"""
Jane Outbound Caller — via Vapi

Usage:
  # Call Joshua directly:
  python3 call.py "+18085008025" "task description"

  # Call a third party on Joshua's behalf:
  python3 call.py "+19046694589" "task description" --recipient "Lori"
"""
import sys, json, requests, argparse
from pathlib import Path

import os
VAPI_KEY = os.environ.get("VAPI_API_KEY") or __import__('dotenv', fromlist=['dotenv_values']).dotenv_values(
    __import__('pathlib').Path.home() / ".openclaw/workspace/.env.private"
).get("VAPI_API_KEY", "")
JANE_ASSISTANT_ID = "5844bf1a-19d8-4766-b6b7-62f1603f9949"
PHONE_NUMBER_ID = "0a30f779-63c6-4fe0-9450-07196b413d28"  # Twilio +16317355263

# --- System prompt when calling JOSHUA directly ---
JOSHUA_PROMPT = """You are Jane, the Pellicer family AI CEO. You are calling JOSHUA PELLICER directly.

The person on this call IS Joshua. Address him as Joshua or Josh.

## What You Know
- Age 43, 186 lbs, 5'10" | Body recomp goal
- Upper/Lower 4-day split | WHOOP-guided
- Macros: 186g protein / 255g carbs / 87g fat / 2,700 cal (training day)
- Marrying Sarah Lemay on May 2, 2026 at Kelly Farm Events, St. Augustine FL
- Honeymoon: Italy Sep 15 - Oct 14, 2026
- Owns AIify | Tennessee property project | Cats: Inky and Quill

## Task
{task}

## Style
- Warm, direct, natural — like a smart friend
- No bullet lists or headers in speech
- You have FULL tool access on this call — calendar, WHOOP, macros, email, shell commands, everything
- If he asks you to check something or take action: DO IT NOW using your tools, don't defer
- Be honest if asked if you're an AI
"""

# --- System prompt when calling a THIRD PARTY on Joshua's behalf ---
THIRD_PARTY_PROMPT = """You are Jane, an AI assistant calling on behalf of Joshua Pellicer.

THE PERSON YOU ARE CALLING IS: {recipient_name}
Address them ONLY as {recipient_name}. NEVER say "Joshua" or "Josh" to them.
You are not Joshua. You are Jane, calling FOR Joshua.

## Your Opening
Start with: "Hi {recipient_name}, this is Jane calling on behalf of Joshua Pellicer."

## Task
{task}

## Style
- Warm, friendly, concise
- Address the person as {recipient_name} throughout the call
- NEVER address them as Joshua or Josh — they are not Joshua
- End the call politely when the task is complete
- Be honest if asked if you're an AI
"""

def make_call(to_number: str, task: str, recipient: str = None) -> dict:
    """
    Make an outbound call via Vapi.
    recipient: name of the person being called (if not Joshua)
    """
    from datetime import datetime
    import pytz

    # Always inject the live date so Jane can resolve "this Monday", "tomorrow", etc.
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)
    date_str = now.strftime("%A, %B %-d, %Y")  # e.g. "Sunday, March 22, 2026"
    day_of_week = now.strftime("%A")
    date_context = f"\n## Today's Date\nToday is {date_str} ({day_of_week}). Use this to resolve any relative date references (\"this Monday\", \"tomorrow\", \"next week\", etc.).\n"

    is_third_party = recipient and recipient.lower() not in ("joshua", "josh")

    if is_third_party:
        system_prompt = THIRD_PARTY_PROMPT.replace("{task}", task).replace("{recipient_name}", recipient) + date_context
        first_message = f"Hi {recipient}, this is Jane calling on behalf of Joshua Pellicer."
    else:
        system_prompt = JOSHUA_PROMPT.replace("{task}", task) + date_context
        first_message = "Hey Joshua, it's Jane."

    payload = {
        "assistantId": JANE_ASSISTANT_ID,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {"number": to_number},
        "assistantOverrides": {
            "firstMessage": first_message,
            "firstMessageMode": "assistant-speaks-first",
            "startSpeakingPlan": {
                "waitSeconds": 2
            },
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "messages": [{"role": "system", "content": system_prompt}]
            }
        }
    }

    r = requests.post(
        "https://api.vapi.ai/call",
        headers={"Authorization": f"Bearer {VAPI_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=15
    )
    return r.json()

def get_transcript(call_id: str, max_wait: int = 300) -> dict:
    """Poll Vapi until call ends and return transcript. Max wait in seconds."""
    import time
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = requests.get(
            f"https://api.vapi.ai/call/{call_id}",
            headers={"Authorization": f"Bearer {VAPI_KEY}"},
            timeout=10
        )
        data = r.json()
        status = data.get("status", "")
        if status == "ended":
            return data
        time.sleep(10)
    return {}

def save_transcript(call_id: str, recipient: str, call_data: dict):
    """Save transcript to memory/calls/"""
    import os
    from datetime import datetime
    
    calls_dir = Path.home() / ".openclaw/workspace/memory/calls"
    calls_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    fname = calls_dir / f"{date_str}-{call_id[:8]}.md"
    
    transcript = call_data.get("transcript", "No transcript available")
    ended_reason = call_data.get("endedReason", "unknown")
    
    content = f"""# Call — {recipient} — {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Call ID:** {call_id}
**Recipient:** {recipient}
**Ended Reason:** {ended_reason}

## Transcript
{transcript}

## Actions Taken
(logged separately)
"""
    fname.write_text(content)
    return str(fname)

def process_call_memory(transcript_path: str):
    """Auto-process a saved transcript through the call memory pipeline."""
    import subprocess
    processor = Path.home() / "Projects/jane-call-memory/processor.py"
    if processor.exists():
        # Run processor (it will skip already-processed files, then rebuild index)
        result = subprocess.run(
            ["/opt/homebrew/bin/python3", str(processor)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("🧠 Memory pipeline updated")
        else:
            print(f"⚠️ Memory pipeline warning: {result.stderr[:200]}")
    else:
        print("⚠️ Memory processor not found at ~/Projects/jane-call-memory/processor.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Phone number to call")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--recipient", "-r", default=None, help="Name of the person being called (if not Joshua)")
    parser.add_argument("--no-transcript", action="store_true", help="Skip transcript polling")
    parser.add_argument("--no-memory", action="store_true", help="Skip memory pipeline processing")
    args = parser.parse_args()

    # ── LOCK: only one outbound call at a time ──────────────────────────────
    import fcntl, time
    LOCK_FILE = Path("/tmp/jane_vapi_call.lock")
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("⚠️ A call is already in progress — skipping duplicate call.")
        sys.exit(0)
    # ────────────────────────────────────────────────────────────────────────

    print(f"📞 Calling {args.phone}...")
    print(f"📋 Task: {args.task}")
    if args.recipient:
        print(f"👤 Recipient: {args.recipient}")

    result = make_call(args.phone, args.task, args.recipient)

    call_id = result.get("id", "unknown")
    status = result.get("status", "unknown")
    print(f"✅ Call initiated | ID: {call_id} | Status: {status}")

    if not args.no_transcript and call_id != "unknown":
        recipient_name = args.recipient or "Joshua"
        print(f"⏳ Waiting for call to end (polling)...")
        call_data = get_transcript(call_id)
        if call_data:
            log_path = save_transcript(call_id, recipient_name, call_data)
            transcript = call_data.get("transcript", "")
            print(f"\n📝 TRANSCRIPT SAVED: {log_path}")
            print(f"\n--- TRANSCRIPT ---")
            print(transcript)
            print(f"--- END TRANSCRIPT ---")
            # Auto-process through memory pipeline
            if not args.no_memory:
                print("\n🧠 Running memory pipeline...")
                process_call_memory(log_path)
            # Signal to Jane that transcript is ready for processing
            print(f"\n🔔 TRANSCRIPT_READY|{call_id}|{recipient_name}|{log_path}")
        else:
            print("⚠️ Call did not end within timeout — poll manually")
