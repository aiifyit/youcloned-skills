#!/usr/bin/env python3
"""First-time user interview for fitness-coach skill."""
import json
from pathlib import Path


def interview():
    print("=== Fitness Coach Setup ===\n")
    profile = {}
    profile["name"] = input("Your name: ").strip()
    profile["age"] = int(input("Age: ").strip())
    profile["weight_lbs"] = float(input("Weight (lbs): ").strip())
    profile["height_inches"] = float(
        input("Height (inches, e.g. 70 for 5'10\"): ").strip()
    )
    profile["weight_kg"] = round(profile["weight_lbs"] / 2.205, 1)

    print(
        "\nGoal options: recomposition / fat_loss / muscle_gain / performance / general_health"
    )
    profile["primary_goal"] = input("Primary goal: ").strip()
    profile["secondary_goal"] = input(
        "Secondary goal (or press Enter to skip): "
    ).strip()

    profile["equipment"] = input(
        "Equipment access (full_gym / home_gym / bodyweight): "
    ).strip()
    profile["training_history"] = input(
        "Training history (beginner / intermediate / advanced): "
    ).strip()
    profile["whoop_connected"] = (
        input("Do you have a WHOOP? (yes/no): ").strip().lower() == "yes"
    )
    profile["days_per_week"] = int(input("Training days per week (3-5): ").strip())

    # Calculate macro targets
    kg = profile["weight_kg"]
    protein_g = round(2.2 * kg)
    training_carbs_g = round(4.0 * kg)
    rest_carbs_g = round(2.0 * kg)

    if profile["primary_goal"] == "recomposition":
        training_fat_g = round(
            ((protein_g * 4 + training_carbs_g * 4) - 2900) / -9
        )
        rest_fat_g = round(((protein_g * 4 + rest_carbs_g * 4) - 2200) / -9)
    else:
        training_fat_g = 90
        rest_fat_g = 80

    profile["macro_targets"] = {
        "protein_g": protein_g,
        "training_day": {
            "calories": protein_g * 4 + training_carbs_g * 4 + training_fat_g * 9,
            "carbs_g": training_carbs_g,
            "fat_g": training_fat_g,
        },
        "rest_day": {
            "calories": protein_g * 4 + rest_carbs_g * 4 + rest_fat_g * 9,
            "carbs_g": rest_carbs_g,
            "fat_g": rest_fat_g,
        },
    }

    profile["split_rotation"] = [
        "Upper A",
        "Lower A",
        "Rest",
        "Upper B",
        "Lower B",
        "Rest",
    ]
    profile["current_split_position"] = 0
    profile["working_weights"] = {}

    out_dir = Path.home() / "Projects/fitness-coach"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "user-profile.json"
    out_path.write_text(json.dumps(profile, indent=2))

    print(f"\nProfile saved to {out_path}")
    print(f"\nMacro targets:")
    print(f"  Protein: {protein_g}g/day")
    print(
        f"  Training day: {profile['macro_targets']['training_day']['calories']} cal"
        f" | {training_carbs_g}g carbs | {training_fat_g}g fat"
    )
    print(
        f"  Rest day: {profile['macro_targets']['rest_day']['calories']} cal"
        f" | {rest_carbs_g}g carbs | {rest_fat_g}g fat"
    )
    return profile


if __name__ == "__main__":
    interview()
