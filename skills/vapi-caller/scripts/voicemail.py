#!/usr/bin/env python3
"""
Jane Voicemail Drop — via Twilio AMD
Calls a number, detects voicemail, plays TTS message, hangs up cleanly.
Phone never rings on recipient's end if voicemail picks up first.

Usage:
  python3 voicemail.py "+15551234567" "Hey it's Jane, just wanted to say..."
  python3 voicemail.py "+19046694589" "Hey Lori, it's Jane calling for Joshua..."
"""
import sys, json, time, argparse, requests, urllib.parse
from pathlib import Path

# Load creds
env = Path.home() / ".openclaw/workspace/.env.private"
ACCOUNT_SID = AUTH_TOKEN = ""
for line in env.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        if k.strip() == "TWILIO_ACCOUNT_SID": ACCOUNT_SID = v.strip()
        if k.strip() == "TWILIO_AUTH_TOKEN": AUTH_TOKEN = v.strip()

FROM_NUMBER = "+16317355263"
TUNNEL_URL = "https://career-focal-urw-performances.trycloudflare.com"  # updated per session

def drop_voicemail(to_number: str, message: str) -> dict:
    """
    Call with AMD. When voicemail detected, voice server plays the message.
    """
    encoded_msg = urllib.parse.quote(message)
    twiml_url = f"{TUNNEL_URL}/voicemail?msg={encoded_msg}&voice=Google.en-US-Neural2-F"

    resp = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Calls.json",
        auth=(ACCOUNT_SID, AUTH_TOKEN),
        data={
            "To": to_number,
            "From": FROM_NUMBER,
            "Url": twiml_url,
            "MachineDetection": "DetectMessageEnd",
            "MachineDetectionTimeout": "30",
            "AsyncAmdStatusCallbackMethod": "POST",
        }
    )
    return resp.json()

def poll_call(sid: str, max_wait: int = 60) -> dict:
    """Poll until call ends."""
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = requests.get(
            f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Calls/{sid}.json",
            auth=(ACCOUNT_SID, AUTH_TOKEN)
        )
        d = r.json()
        if d.get("status") in ("completed", "failed", "busy", "no-answer"):
            return d
        time.sleep(5)
    return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phone", help="Phone number (E.164 format: +15551234567)")
    parser.add_argument("message", help="Message to leave on voicemail")
    parser.add_argument("--wait", action="store_true", help="Wait for call to complete")
    args = parser.parse_args()

    print(f"📱 Dropping voicemail to {args.phone}...")
    print(f"💬 Message: {args.message[:80]}...")

    result = drop_voicemail(args.phone, args.message)

    if "code" in result:
        print(f"❌ Error: {result.get('message')}")
        sys.exit(1)

    sid = result.get("sid", "?")
    status = result.get("status", "?")
    print(f"✅ Call initiated | SID: {sid} | Status: {status}")
    print(f"   AMD active — message will play when voicemail detects")

    if args.wait:
        print("⏳ Waiting for completion...")
        final = poll_call(sid)
        print(f"📊 Final status: {final.get('status')} | Duration: {final.get('duration')}s")
        answered_by = final.get("answered_by", "unknown")
        print(f"   Answered by: {answered_by}")
