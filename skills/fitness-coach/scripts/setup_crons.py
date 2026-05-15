#!/usr/bin/env python3
"""Register 5x daily WHOOP check-in crons in OpenClaw."""
import subprocess

CRONS = [
    {
        "name": "whoop-morning",
        "cron": "0 7 * * *",
        "message": (
            "WHOOP morning check: run scripts/whoop_check.py in fitness-coach skill. "
            "Read user-profile.json for targets. Send user: recovery score, "
            "today's workout recommendation (split day + override if recovery is low), "
            "macro targets for training vs rest day, sleep summary."
        ),
    },
    {
        "name": "whoop-post-workout",
        "cron": "0 11 * * *",
        "message": (
            "WHOOP post-workout check: run scripts/whoop_check.py in fitness-coach skill. "
            "Check today food log. Send user: current strain vs target, calories burned, "
            "macros remaining, post-workout meal suggestion."
        ),
    },
    {
        "name": "whoop-post-lunch",
        "cron": "30 13 * * *",
        "message": (
            "WHOOP post-lunch check: run whoop_check.py. Check food log. "
            "If carbs 100g+ behind target, message user with snack suggestion. "
            "Otherwise stay quiet."
        ),
    },
    {
        "name": "whoop-afternoon",
        "cron": "0 16 * * *",
        "message": (
            "WHOOP afternoon check: run whoop_check.py. Message user: total strain today, "
            "remaining macros for dinner, tomorrow workout recommendation."
        ),
    },
    {
        "name": "whoop-evening",
        "cron": "0 18 * * *",
        "message": (
            "WHOOP evening check: run whoop_check.py, read food log. Message user: "
            "full day strain, exact dinner macros to hit targets, tomorrow workout "
            "split recommendation. If high strain, suggest magnesium glycinate."
        ),
    },
]


def setup():
    for c in CRONS:
        result = subprocess.run(
            [
                "openclaw", "cron", "add",
                "--name", c["name"],
                "--cron", c["cron"],
                "--tz", "America/New_York",
                "--system-event", c["message"],
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"{c['name']} cron registered")
        else:
            print(f"  {c['name']}: {result.stderr[:100]}")

    print("\nCron setup complete.")


if __name__ == "__main__":
    setup()
