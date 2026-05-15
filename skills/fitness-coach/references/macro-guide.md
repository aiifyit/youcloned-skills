# Macro Calculation Guide

Evidence-based macro targets for body recomposition, with WHOOP-driven adjustments.

---

## Base Formula (by body weight in kg)

| Macro | Formula | All Days? |
|-------|---------|-----------|
| **Protein** | 2.2g x kg | Yes — same every day |
| **Training Carbs** | 4.0g x kg | Training days only |
| **Rest Carbs** | 2.0g x kg | Rest days only |
| **Fat** | Fills remaining calories | Varies by day type |

### Calorie Calculation

```
Training day calories = (protein_g x 4) + (training_carbs_g x 4) + (fat_g x 9)
Rest day calories     = (protein_g x 4) + (rest_carbs_g x 4) + (fat_g x 9)
```

### Fat Calculation (Recomposition)

For recomposition, fat fills the gap between macro calories and target calories:
- Training day target: ~2900 cal → fat_g = (2900 - protein_cal - carb_cal) / 9
- Rest day target: ~2200 cal → fat_g = (2200 - protein_cal - carb_cal) / 9

For other goals, use defaults:
- Training fat: 90g
- Rest fat: 80g

---

## Example: 186 lbs / 84.4 kg (Recomposition)

| | Protein | Carbs | Fat | Calories |
|--|---------|-------|-----|----------|
| **Training Day** | 186g | 338g | ~73g | ~2900 |
| **Rest Day** | 186g | 169g | ~76g | ~2200 |

---

## WHOOP Strain Adjustments

These adjustments are applied on top of the base macros:

| Condition | Adjustment |
|-----------|------------|
| Strain > 14 (high training day) | Add 100 cal from carbs (+25g carbs) |
| Strain < 5 on rest day | Drop 100 cal from carbs (-25g carbs) |
| Strain > 16 (very high) | Add 200 cal from carbs (+50g carbs) |
| RED recovery day | Switch to rest day macros regardless of schedule |

---

## Protein Distribution

Spread total protein across 4-5 meals (~37-46g per meal for 186g target).

**Timing guidelines (PMID: 35019903):**
- Pre-workout: 30-40g protein + carbs, 60-90 min before training
- Post-workout: 40-46g protein within 2 hours
- Before bed: 30-40g casein or cottage cheese (slow-release)
- Never train fasted (cortisol spike, especially at 43)

---

## Carb Timing (Training Days)

Consume ~40% of training-day carbs around the workout:

| Window | % of Daily Carbs | Example (338g total) |
|--------|-----------------|---------------------|
| Pre-workout (60-90 min before) | 15% | ~50g |
| Intra-workout (optional) | 5% | ~17g |
| Post-workout (within 2 hrs) | 20% | ~68g |
| Remaining meals | 60% | ~203g |

---

## When to Adjust Targets

### Scale Weight Stalling (2+ weeks)
- If trying to lose fat: reduce rest day carbs by 25g
- If trying to gain: increase training day carbs by 25g

### WHOOP HRV Trending Down
- Do NOT cut calories further
- May need to increase carbs for recovery
- Prioritize sleep over deficit

### Body Recomposition Phase
- Expect slow scale changes (gaining muscle, losing fat simultaneously)
- Track progress by: waist measurement, progress photos, strength numbers
- Typical rate: 0.5-1 lb fat loss per week while maintaining/gaining strength

---

## Supplements

| Supplement | Dose | Timing | Evidence |
|-----------|------|--------|----------|
| Creatine monohydrate | 5g daily | Any time | PMID: 37432300 — small but real hypertrophy benefit |
| Magnesium glycinate | 400mg | Before bed | Sleep quality + recovery, especially on high-strain days |
| Vitamin D3 | 2000-5000 IU | With fat-containing meal | Most adults are deficient |
| Omega-3 (EPA/DHA) | 2-3g combined | With meals | Anti-inflammatory, joint health |

---

## Meal Logging

Use `scripts/log_meal.py` to track meals:

```bash
python3 scripts/log_meal.py "grilled chicken, rice, broccoli" \
  --cal 650 --protein 45 --carbs 70 --fat 12 --meal lunch --time 12:30
```

The script:
1. Adds the meal to today's log at `~/Projects/fitness-coach/logs/{date}.json`
2. Updates running daily totals
3. Shows remaining macros vs targets
4. Flags if any macro is significantly behind pace

---

## Quick Macro Estimates (Common Foods)

| Food | Serving | Cal | Protein | Carbs | Fat |
|------|---------|-----|---------|-------|-----|
| Chicken breast (grilled) | 6 oz | 280 | 52g | 0g | 6g |
| White rice (cooked) | 1 cup | 205 | 4g | 45g | 0g |
| Eggs (whole) | 2 large | 140 | 12g | 1g | 10g |
| Greek yogurt (2%) | 1 cup | 150 | 20g | 8g | 4g |
| Sweet potato | 1 medium | 115 | 2g | 27g | 0g |
| Salmon fillet | 6 oz | 350 | 40g | 0g | 20g |
| Oatmeal (dry) | 1/2 cup | 150 | 5g | 27g | 3g |
| Whey protein | 1 scoop | 120 | 24g | 3g | 1g |
| Banana | 1 medium | 105 | 1g | 27g | 0g |
| Almonds | 1 oz (23) | 164 | 6g | 6g | 14g |
