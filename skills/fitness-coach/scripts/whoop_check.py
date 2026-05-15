#!/usr/bin/env python3
"""Pull live WHOOP data and return structured JSON with recommendations."""
import json
import sys
from pathlib import Path
from datetime import date, datetime, timezone


def get_data():
    try:
        from whoopy import WhoopClient
    except ImportError:
        print(json.dumps({"error": "whoopy not installed -- run setup_whoop.py"}))
        sys.exit(1)

    creds_path = Path.home() / "Projects/fitness-coach/.whoop_credentials.json"
    token_path = Path.home() / "Projects/fitness-coach/.whoop_tokens.json"

    if not creds_path.exists():
        # Fall back to whoop-sync directory
        creds_path = Path.home() / "Projects/whoop-sync/.whoop_credentials.json"
        token_path = Path.home() / "Projects/whoop-sync/.whoop_tokens_v2.json"

    if not creds_path.exists():
        print(json.dumps({"error": "No WHOOP credentials found. Run setup_whoop.py first."}))
        sys.exit(1)

    creds = json.loads(creds_path.read_text())

    client = WhoopClient(
        client_id=creds["clientId"],
        client_secret=creds["clientSecret"],
        token_file=str(token_path),
    )

    today = date.today().isoformat()
    start = f"{today}T00:00:00.000Z"
    end = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Fetch recovery, sleep, cycle
    recovery = None
    sleep_data = None
    cycle = None

    try:
        recoveries = client.recovery.get_collection(start=start, end=end)
        if recoveries.records:
            r = recoveries.records[-1]
            recovery = {
                "score": r.score.recovery_score if r.score else None,
                "hrv_ms": r.score.hrv_rmssd_milli if r.score else None,
                "rhr": r.score.resting_heart_rate if r.score else None,
            }
    except Exception as e:
        recovery = {"error": str(e)}

    try:
        sleeps = client.sleep.get_collection(start=start, end=end)
        if sleeps.records:
            s = sleeps.records[-1]
            if s.score:
                ss = s.score.stage_summary
                total_min = (ss.total_in_bed_time_milli or 0) / 60000
                sleep_data = {
                    "hours_in_bed": round(total_min / 60, 1),
                    "efficiency_pct": round(
                        s.score.sleep_efficiency_percentage or 0, 1
                    ),
                }
    except Exception as e:
        sleep_data = {"error": str(e)}

    try:
        cycles = client.cycle.get_collection(start=start, end=end)
        if cycles.records:
            c = cycles.records[-1]
            cycle = {
                "strain": round(c.score.strain if c.score else 0, 2),
                "kilojoules": round(c.score.kilojoule if c.score else 0, 1),
                "cal_burned": (
                    round((c.score.kilojoule or 0) * 0.239, 0) if c.score else 0
                ),
            }
    except Exception as e:
        cycle = {"error": str(e)}

    # Get recommendation
    rec_score = recovery.get("score") if recovery else None
    if rec_score is None:
        intensity = "unknown"
        rec_text = "No recovery data yet -- treat as yellow"
    elif rec_score >= 67:
        intensity = "full"
        rec_text = f"GREEN {rec_score}% -- full session, push volume, good day for PRs"
    elif rec_score >= 34:
        intensity = "moderate"
        rec_text = f"YELLOW {rec_score}% -- train but -20% volume, -10% load, no failure"
    else:
        intensity = "rest"
        rec_text = f"RED {rec_score}% -- rest or active recovery only"

    output = {
        "date": today,
        "recovery": recovery,
        "sleep": sleep_data,
        "cycle": cycle,
        "recommendation": {"intensity": intensity, "text": rec_text},
    }

    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    get_data()
