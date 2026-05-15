#!/usr/bin/env python3
"""List ElevenLabs voices for the account whose key is in macOS Keychain.

Run:  python3 list_voices.py

Key is read from Keychain entry 'elevenlabs-api'. The key never appears on
stdout, in environment variables, or in any file.
"""
import json, os, subprocess, sys, urllib.error, urllib.request

KEYCHAIN_NAME = "elevenlabs-api"

def get_key() -> str:
    account = os.environ.get("USER") or subprocess.check_output(["whoami"]).decode().strip()
    try:
        out = subprocess.check_output(
            ["security", "find-generic-password", "-s", KEYCHAIN_NAME, "-a", account, "-w"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(
            f"Couldn't read Keychain '{KEYCHAIN_NAME}': {e.output.decode().strip()}\n"
            f"Create it with:\n"
            f"  security add-generic-password -s \"{KEYCHAIN_NAME}\" -a \"$USER\" -w"
        )
    key = out.decode().strip()
    if not key:
        sys.exit("Keychain entry is empty.")
    return key

def fetch(key: str) -> list:
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": key, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r).get("voices", [])
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs returned {e.code}: {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"Couldn't reach api.elevenlabs.io: {e.reason}")

def fmt(labels, *keys, default="—"):
    for k in keys:
        if k in labels and labels[k]:
            return str(labels[k])
    return default

def main():
    voices = fetch(get_key())
    if not voices:
        print("No voices on this account.")
        return
    voices.sort(key=lambda v: (v.get("category",""), v.get("name","")))
    print(f"\n{len(voices)} voices on this account:\n")
    print(f"  {'VOICE ID':<24}  {'NAME':<22}  {'GENDER':<8} {'AGE':<10} {'ACCENT':<14} {'USE CASE':<14} CATEGORY")
    print(f"  {'-'*24}  {'-'*22}  {'-'*8} {'-'*10} {'-'*14} {'-'*14} {'-'*10}")
    for v in voices:
        labels = v.get("labels") or {}
        print(
            f"  {v.get('voice_id',''):<24}  "
            f"{v.get('name',''):<22}  "
            f"{fmt(labels, 'gender'):<8} "
            f"{fmt(labels, 'age'):<10} "
            f"{fmt(labels, 'accent', 'descriptive'):<14} "
            f"{fmt(labels, 'use_case', 'use case'):<14} "
            f"{v.get('category','')}"
        )

if __name__ == "__main__":
    main()
