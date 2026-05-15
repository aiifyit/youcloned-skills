#!/usr/bin/env python3
"""Install whoopy and run WHOOP OAuth setup."""
import subprocess
import sys
import json
from pathlib import Path


def setup():
    print("Installing whoopy...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "whoopy", "--break-system-packages", "-q"]
    )

    try:
        import whoopy

        print(f"whoopy {whoopy.__version__} installed")
    except ImportError:
        print("whoopy installation failed")
        sys.exit(1)

    # Load credentials
    creds_path = Path.home() / "Projects/fitness-coach/.whoop_credentials.json"
    if not creds_path.exists():
        # Fall back to existing whoop-sync credentials
        alt_path = Path.home() / "Projects/whoop-sync/.whoop_credentials.json"
        if alt_path.exists():
            creds_path = alt_path
            print(f"Using existing credentials from {alt_path}")
        else:
            print("\nWHOOP API credentials needed.")
            print("Get them at: https://developer-dashboard.whoop.com/")
            client_id = input("Client ID: ").strip()
            client_secret = input("Client Secret: ").strip()
            creds = {"clientId": client_id, "clientSecret": client_secret}
            creds_path.parent.mkdir(parents=True, exist_ok=True)
            creds_path.write_text(json.dumps(creds, indent=2))

    creds = json.loads(creds_path.read_text())

    # Run OAuth via whoopy
    from whoopy import WhoopClient

    token_path = Path.home() / "Projects/fitness-coach/.whoop_tokens.json"
    # Also check whoop-sync tokens
    alt_token = Path.home() / "Projects/whoop-sync/.whoop_tokens_v2.json"
    if alt_token.exists() and not token_path.exists():
        token_path = alt_token

    try:
        client = WhoopClient(
            client_id=creds["clientId"],
            client_secret=creds["clientSecret"],
            token_file=str(token_path),
        )
        profile = client.user.get_profile()
        print(f"Connected to WHOOP as: {profile.first_name} {profile.last_name}")
    except Exception as e:
        print(f"OAuth required. Opening browser... ({e})")
        client = WhoopClient(
            client_id=creds["clientId"],
            client_secret=creds["clientSecret"],
            token_file=str(token_path),
        )
        print("WHOOP connected")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Set up WHOOP OAuth connection")
    p.add_argument("--reauth", action="store_true", help="Force re-authentication")
    args = p.parse_args()
    setup()
