#!/usr/bin/env python3
"""Log workout sets and track progressive overload."""
import json
import argparse
from pathlib import Path
from datetime import date


def log(exercise, weight, reps, set_num=None, notes=None):
    today = date.today().isoformat()
    log_dir = Path.home() / "Projects/fitness-coach/logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{today}.json"

    data = (
        json.loads(log_path.read_text())
        if log_path.exists()
        else {
            "date": today,
            "meals": [],
            "daily_totals": {
                "calories": 0,
                "protein_g": 0,
                "carbs_g": 0,
                "fat_g": 0,
            },
            "workout": {"exercises": [], "sets": []},
        }
    )

    if "workout" not in data:
        data["workout"] = {"exercises": [], "sets": []}

    entry = {
        "exercise": exercise,
        "weight_lbs": weight,
        "reps": reps,
        "notes": notes,
    }
    if set_num:
        entry["set"] = set_num
    data["workout"]["sets"].append(entry)

    log_path.write_text(json.dumps(data, indent=2))

    # Check progressive overload
    profile_path = Path.home() / "Projects/fitness-coach/user-profile.json"
    if profile_path.exists():
        profile = json.loads(profile_path.read_text())
        working = profile.get("working_weights", {})
        ex_key = exercise.lower().replace(" ", "_")
        prev = working.get(ex_key, {})

        if weight > prev.get("weight", 0):
            profile["working_weights"][ex_key] = {
                "weight": weight,
                "best_reps": reps,
                "date": today,
            }
            profile_path.write_text(json.dumps(profile, indent=2))
            print(f"New working weight: {exercise} {weight}lbs x {reps}")
        elif reps >= 8 and weight == prev.get("weight"):
            is_upper = any(
                kw in ex_key
                for kw in ["press", "curl", "lateral", "fly", "raise", "pushdown", "extension"]
            )
            next_weight = weight + (5 if is_upper else 10)
            print(
                f"{exercise} {weight}x{reps} logged. "
                f"Hit 8 reps -- next session try {next_weight}lbs"
            )
        else:
            print(f"{exercise} {weight}x{reps} logged")
    else:
        print(f"{exercise} {weight}x{reps} logged")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Log a workout set")
    p.add_argument("exercise", help="Exercise name")
    p.add_argument("weight", type=float, help="Weight in lbs")
    p.add_argument("reps", type=int, help="Number of reps")
    p.add_argument("--set", type=int, dest="set_num", default=None, help="Set number")
    p.add_argument("--notes", default=None, help="Notes for this set")
    args = p.parse_args()
    log(args.exercise, args.weight, args.reps, args.set_num, args.notes)
