# WHOOP 5x Daily Check-In Protocol

## Overview

Five automated check-ins per day, driven by WHOOP data and the user's food/workout logs. Each check-in runs `scripts/whoop_check.py` and cross-references the day's logs at `~/Projects/fitness-coach/logs/{date}.json`.

---

## Check-In Schedule

### 1. Morning Check (7:00 AM ET)

**Trigger:** First automated event of the day.

**Actions:**
1. Run `whoop_check.py` — fetch recovery score, HRV, RHR, sleep data
2. Read `user-profile.json` for split rotation and macro targets
3. Determine today's scheduled workout from `split_rotation[current_split_position]`

**Output to user:**
- Recovery score with color (GREEN/YELLOW/RED)
- Sleep hours + efficiency
- HRV and RHR
- Today's scheduled workout (e.g., "Upper A — Horizontal Emphasis")
- Any WHOOP override (e.g., RED = mandatory rest, skip workout)
- Macro targets for today (training day vs rest day)
- Advance `current_split_position` in profile

**Decision rules:**
- GREEN (67-100%): confirm scheduled workout, push volume
- YELLOW (34-66%): confirm workout but note volume/load reductions
- RED (0-33%): override to rest day, switch macro targets to rest day
- 2+ consecutive yellow: insert rest day, don't advance split position
- Any red: mandatory rest, don't advance split position

---

### 2. Post-Workout Check (11:00 AM ET)

**Trigger:** After typical morning training window.

**Actions:**
1. Run `whoop_check.py` — get current strain
2. Read today's food log for running totals
3. Calculate remaining macros

**Output to user:**
- Current day strain vs target (12-16 for training day)
- Estimated calories burned from WHOOP
- Macros consumed so far vs targets
- Remaining protein, carbs, fat for the day
- Post-workout meal suggestion to hit protein window (40-46g protein within 2 hours)

**Silent if:** No workout was logged today (rest day).

---

### 3. Post-Lunch Check (1:30 PM ET)

**Trigger:** After typical lunch window.

**Actions:**
1. Run `whoop_check.py` — current strain
2. Read food log — check carb progress

**Output to user (conditional):**
- ONLY message if carbs are 100g+ behind target
- Suggest a carb-focused snack (rice cakes, fruit, oats)

**Silent if:** Carbs are on track or it's a rest day.

---

### 4. Afternoon Check (4:00 PM ET)

**Trigger:** Pre-dinner planning window.

**Actions:**
1. Run `whoop_check.py` — updated strain
2. Read food log — calculate remaining macros for dinner

**Output to user:**
- Total strain accumulated today
- Remaining macros: exact grams of protein, carbs, fat for dinner
- If strain > 14: add 100 cal from carbs to dinner target
- If strain < 5 (rest day): subtract 100 cal from carbs
- Tomorrow's scheduled workout + any notes

---

### 5. Evening Summary (6:00 PM ET)

**Trigger:** End-of-day wrap-up.

**Actions:**
1. Run `whoop_check.py` — final strain reading
2. Read complete food log
3. Read workout log if training day

**Output to user:**
- Full day strain summary
- Exact dinner macros to hit targets (protein, carbs, fat in grams)
- If training day: workout volume summary (total sets, exercises completed)
- Tomorrow's workout split recommendation
- If high strain (>14): suggest magnesium glycinate before bed
- If protein is short: suggest casein shake or cottage cheese before bed
- Advance split position if workout was completed

---

## WHOOP API Reference (v1)

Base URL: `https://api.prod.whoop.com/developer/v1/`
Auth: OAuth2 Bearer token. Scopes: `read:recovery`, `read:cycles`, `read:workout`, `read:sleep`, `read:profile`, `read:body_measurement`
Script: `~/Projects/whoop-sync/whoop_sync.py` | Tokens: `~/Projects/whoop-sync/.whoop_tokens.json`

### Endpoints

| Endpoint | Method | Scope | Notes |
|----------|--------|-------|-------|
| `cycle` | GET | read:cycles | Day strain, avg/max HR, kilojoules. Paginated. |
| `cycle/{cycleId}` | GET | read:cycles | Single cycle by ID |
| `cycle/{cycleId}/sleep` | GET | read:sleep | Sleep linked to a specific cycle |
| `cycle/{cycleId}/recovery` | GET | read:recovery | Recovery linked to a specific cycle |
| `recovery` | GET | read:recovery | All recoveries paginated (score, HRV, RHR, SpO2, skin temp) |
| `sleep` | GET | read:sleep | All sleeps paginated (stage summary, efficiency, respiratory rate) |
| `sleep/{sleepId}` | GET | read:sleep | Single sleep by UUID |
| `workout` | GET | read:workout | All workouts paginated. Returns v2 UUIDs. Includes zone_durations. |
| `workout/{workoutId}` | GET | read:workout | Single workout by UUID |
| `user/profile/basic` | GET | read:profile | Name, email, user_id |
| `user/measurement/body` | GET | read:body_measurement | Height, weight, max HR |
| `activity/mapping/{v1Id}` | GET | — | Lookup v2 UUID from v1 integer activity ID |

### Workout `zone_durations` Fields (all in milliseconds)
- `zone_zero_milli` — Very light (< 50% max HR)
- `zone_one_milli` — Light (50–60%)
- `zone_two_milli` — Moderate / aerobic base (60–70%) ← Zone 2 training target
- `zone_three_milli` — Hard (70–80%)
- `zone_four_milli` — Very hard (80–90%)
- `zone_five_milli` — Max effort (>90%)

Divide by 60000 to get minutes.

### Common Query Params (paginated endpoints)
- `limit` — max 25, default 10
- `start` / `end` — ISO-8601 datetime filters
- `nextToken` — pagination cursor from previous response

### Known Issues
- Workout endpoint returns null/empty if `read:workout` scope was not granted at OAuth time. Re-auth with `python3 ~/Projects/whoop-sync/whoop_auth.py` to add scope.
- Recovery/sleep data for the current day may not be available until WHOOP completes scoring (usually after the sleep period ends).

---

## Interpreting WHOOP Output

The `whoop_sync.py` script returns JSON with these fields:

```json
{
  "date": "2026-04-11",
  "recovery": {
    "recovery_score": 72,
    "hrv_rmssd_milli": 24.5,
    "resting_heart_rate": 68,
    "spo2_percentage": 96.2,
    "skin_temp_celsius": 33.7
  },
  "sleep": {
    "sleep_performance_percentage": 88,
    "total_in_bed_hours": 7.2,
    "rem_hours": 1.6,
    "deep_hours": 1.1,
    "respiratory_rate": 15.8
  },
  "strain": {
    "strain": 12.45,
    "kilojoule": 8500,
    "kcal": 2032,
    "average_heart_rate": 77,
    "max_heart_rate": 152
  },
  "workouts": [{
    "sport_name": "running",
    "strain": 8.2,
    "avg_hr": 123,
    "max_hr": 146,
    "kcal": 375,
    "distance_meter": 4800,
    "zone_zero_min": 2,
    "zone_one_min": 5,
    "zone_two_min": 28,
    "zone_three_min": 8,
    "zone_four_min": 2,
    "zone_five_min": 0
  }]
}
```

### Zone 2 Cardio Protocol
- **Target: 40 min Zone 2 per session, 2x per week**
- **Placement: Both Rest days in the 6-day split rotation (positions 3 and 6)**
  - Split: Upper A → Lower A → **Rest+Run** → Upper B → Lower B → **Rest+Run** → repeat
  - Never on lifting days — Zone 2 on rest days aids recovery without competing with strength work
- Zone 2 = zone_two_milli from workout endpoint (60–70% max HR, ~136 bpm for Joshua)
- Morning nudge fires on each rest day to prompt the run
- Daily 4pm check-in reports Zone 2 vs goal on any cardio day
- Zone 2 time logged to Workouts tab in WHOOP Tracking Sheet

### Key Thresholds
- **Recovery:** GREEN >= 67, YELLOW 34-66, RED < 34
- **Strain target:** 12-16 training day, 4-8 rest day, 50-70 weekly
- **HRV baseline (Joshua):** 17-28ms (low for age — recovery is the bottleneck)
- **RHR baseline (Joshua):** 66-71 bpm

### HRV Trend Rules (Weekly)
- Trending UP over 7 days: training load is well-tolerated, can add volume
- Flat: maintaining, keep programming
- Trending DOWN over 7 days: accumulated fatigue, implement deload week (50% volume)
