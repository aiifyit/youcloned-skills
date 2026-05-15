#!/usr/bin/env python3
"""Log a meal and update daily totals."""
import json
import argparse
from pathlib import Path
from datetime import date


def log(description, cal, protein, carbs, fat, meal_name=None, time=None):
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
            "supplements": [],
            "daily_totals": {
                "calories": 0,
                "protein_g": 0,
                "carbs_g": 0,
                "fat_g": 0,
            },
        }
    )

    meal = {
        "meal": meal_name or f"meal_{len(data['meals']) + 1}",
        "time": time or "unknown",
        "description": description,
        "totals": {
            "cal": cal,
            "protein_g": protein,
            "carbs_g": carbs,
            "fat_g": fat,
        },
    }
    data["meals"].append(meal)

    data["daily_totals"]["calories"] += cal
    data["daily_totals"]["protein_g"] += protein
    data["daily_totals"]["carbs_g"] += carbs
    data["daily_totals"]["fat_g"] += fat

    log_path.write_text(json.dumps(data, indent=2))

    # Load profile for targets
    profile_path = Path.home() / "Projects/fitness-coach/user-profile.json"
    if profile_path.exists():
        profile = json.loads(profile_path.read_text())
        targets = profile["macro_targets"]
        print(f"Logged: {description}")
        print(f"  {cal} cal | {protein}g protein | {carbs}g carbs | {fat}g fat")
        print(f"\nRunning totals:")
        print(
            f"  Calories: {data['daily_totals']['calories']}"
            f" / {targets['training_day']['calories']}"
        )
        print(
            f"  Protein:  {data['daily_totals']['protein_g']}g"
            f" / {targets['protein_g']}g"
        )
        print(
            f"  Carbs:    {data['daily_totals']['carbs_g']}g"
            f" / {targets['training_day']['carbs_g']}g"
        )
        print(
            f"  Fat:      {data['daily_totals']['fat_g']}g"
            f" / {targets['training_day']['fat_g']}g"
        )
    else:
        print(f"Logged: {description}")
        print(f"  {cal} cal | {protein}g protein | {carbs}g carbs | {fat}g fat")
        print("  (No profile found -- run interview.py first for target tracking)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Log a meal with macro breakdown")
    p.add_argument("description", help="Meal description")
    p.add_argument("--cal", type=int, required=True, help="Total calories")
    p.add_argument("--protein", type=float, required=True, help="Protein in grams")
    p.add_argument("--carbs", type=float, required=True, help="Carbs in grams")
    p.add_argument("--fat", type=float, required=True, help="Fat in grams")
    p.add_argument("--meal", default=None, help="Meal name (breakfast, lunch, etc.)")
    p.add_argument("--time", default=None, help="Time of meal (HH:MM)")
    args = p.parse_args()
    log(args.description, args.cal, args.protein, args.carbs, args.fat, args.meal, args.time)
