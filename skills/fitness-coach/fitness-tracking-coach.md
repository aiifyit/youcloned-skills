---
name: fitness-coach
description: "Fitness tracking and coaching — WHOOP recovery data, macro logging, workout programming, and personalized fitness planning for Joshua."
---

# Fitness Coach

AI-powered fitness coaching with live WHOOP biometric integration, evidence-based workout programming, dynamic macro tracking, and 5x daily automated check-ins.

## First-Time Setup

When the skill is first triggered or user says "set up fitness tracking":

1. **Interview:** Run `scripts/interview.py` — collects name, age, weight, height, goals, equipment access, WHOOP status, training history. Saves profile to `~/Projects/fitness-coach/user-profile.json`.

2. **Research:** Run `scripts/research_goals.py <goal>` — searches PubMed (via NCBI E-utilities: esearch + efetch) for evidence-based protocols matching the user's specific goals. Saves results to `~/Projects/fitness-coach/research/`.

3. **WHOOP setup:** Run `scripts/setup_whoop.py` — installs whoopy, runs OAuth browser flow, verifies connection. Falls back to existing credentials at `~/Projects/whoop-sync/` if available.

4. **Generate plan:** Using the interview data + research results + `references/workout-splits.md` + `references/macro-guide.md`, generate personalized macro targets (training vs rest day), workout split, and weekly schedule. Save to `user-profile.json`.

5. **Crons:** Run `scripts/setup_crons.py` — registers 5 daily automated WHOOP check-ins in OpenClaw.

```bash
# Full setup sequence
python3 scripts/interview.py
python3 scripts/research_goals.py recomposition
python3 scripts/setup_whoop.py
python3 scripts/setup_crons.py
```

## ⭐ WHOOP Auto-Sync Rule (MANDATORY)

**Before answering ANY health, fitness, nutrition, recovery, or macro question — always run a WHOOP sync first:**

```bash
/opt/homebrew/bin/python3 ~/Projects/whoop-sync/whoop_sync.py
```

This applies to: meal logging, macro questions, workout questions, recovery checks, "what should I eat", "should I train today", WHOOP data requests, and any question touching Joshua's body or health. No exceptions.

If sync returns `None` for recovery (WHOOP hasn't processed yet), note it and answer based on available strain data. Never skip the sync step.

## ⭐ Gym Workout Flow (MANDATORY when Joshua is at the gym or asks for his workout)

This is the complete end-to-end protocol. Execute all steps every time. Do not skip the UI step.

**Full sequence:**
1. Sync WHOOP → get today's recovery data
2. Read the training rotation → determine today's split
3. Read the training log → pull last logged entry for today's split (with weights/reps)
4. Calculate today's workout (progressive overload applied)
5. Ensure gym app is running → send Joshua the link to `https://gym.janeslinks.com`

Steps 1–3 run in parallel via the swarm below. Steps 4–5 execute after all agents return.

---

## ⭐ Workout Query Swarm (MANDATORY for workout questions)

**When Joshua asks about today's workout, what he should lift, or anything about his training session — spawn 3 parallel sub-agents and yield for results before presenting the workout.**

### Step 1 — Spawn all 3 agents in parallel

Use `sessions_spawn` with `runtime="subagent"` and `mode="run"` for each:

---

**Agent 1 — WHOOP Agent**

Task: Run the WHOOP sync script and return recovery data.

```
Run: /opt/homebrew/bin/python3 ~/Projects/whoop-sync/whoop_sync.py
Return: recovery %, HRV, RHR, strain, status (GREEN/YELLOW/RED), and guidance text.

When done, call home:
  curl -s -X POST http://127.0.0.1:18789/tools/invoke \
    -H "Content-Type: application/json" \
    -d '{"tool":"message","args":{"action":"send","channel":"telegram","target":"297140858","message":"whoop-agent done: [recovery%, HRV, RHR, strain, status]"}}'
```

---

**Agent 2 — Rotation Agent**

Task: Read the training rotation file and return the next session.

```
Read: ~/Projects/jane-health/training/rotation.json
Return: next_session name, current_index, last_completed date and split type.

When done, call home:
  curl -s -X POST http://127.0.0.1:18789/tools/invoke \
    -H "Content-Type: application/json" \
    -d '{"tool":"message","args":{"action":"send","channel":"telegram","target":"297140858","message":"rotation-agent done: [next_session, current_index, last_completed]"}}'
```

---

**Agent 3 — Last Session Agent**

Task: Read the training log and return the most recent session matching today's split type.

```
Read: ~/Projects/jane-health/training-log.json
Find: the most recent entry matching today's split type (from rotation.json).
Return: all exercises with logged weights and reps from that session.

When done, call home:
  curl -s -X POST http://127.0.0.1:18789/tools/invoke \
    -H "Content-Type: application/json" \
    -d '{"tool":"message","args":{"action":"send","channel":"telegram","target":"297140858","message":"last-session-agent done: [exercise list with weights/reps]"}}'
```

---

### Step 2 — Yield for results

After spawning all 3 agents, call `sessions_yield` to wait for all agents to complete before proceeding.

### Step 3 — Synthesize and present

Once all 3 agents have returned results, present:

- **Split** — correct session type from rotation (e.g., Upper A, Lower B)
- **WHOOP status** — GREEN/YELLOW/RED with recovery %, HRV, RHR, strain
- **Volume adjustment** — based on WHOOP decision tree (GREEN = full, YELLOW = -20% volume / -10% load, RED = rest/active recovery)
- **Full exercise list** — last logged weights pre-filled for each movement
- **Suggested weights** — progressive overload recommendations (+5 lbs upper / +10 lbs lower if rep target was hit twice; -10% if rep floor was missed)
- **Macro guidance** — training vs rest day targets based on recovery status

### Step 4 — Ensure gym app is running

After synthesizing, check if the gym app is live and start it if needed:

```bash
# Check if running
lsof -i :7455 | grep LISTEN

# Start if not running
cd ~/Projects/jane-health/workout-ui && /opt/homebrew/bin/python3 app.py > ~/.cloudflared/workout-ui.log 2>&1 &
sleep 2 && lsof -i :7455 | grep LISTEN
```

### Step 5 — Send Joshua the gym UI link

Once the app is confirmed running, send Joshua the link:

```
https://gym.janeslinks.com
```

The page auto-generates his workout from:
- Today's rotation (reads `rotation.json` live)
- Last session weights/reps (reads `training-log.json` live)
- WHOOP recovery cache (reads today's WHOOP data file)
- Progressive overload logic built into the app

Joshua enters his sets/reps/weights on-page during the session. On submission:
- Data saves to `training-log.json`
- Rotation advances to next session
- WHOOP strain target updates
- Post-workout macro protocol triggers

> **Note:** If the gym app is down or the tunnel is broken, fall back to presenting the workout card inline in Telegram and log sets manually via `scripts/log_workout.py`.

---

## Daily Operations

### Morning Check (first message of day or 7am cron)

1. Run `scripts/whoop_check.py` — returns recovery, sleep, strain as JSON
2. Read `~/Projects/fitness-coach/user-profile.json` for targets and split position
3. Apply decision tree from `references/whoop-decision-tree.md`
4. Output: recovery score (GREEN/YELLOW/RED), sleep summary, today's workout (split day + WHOOP override if needed), macro targets for training vs rest day

### Workout Logging

When user sends exercise data (e.g., "bench press 185x8", "squat 275x5"):

```bash
python3 scripts/log_workout.py "Bench Press" 185 8 --set 1
```

**Progressive overload tracking:** If same weight hits rep target (e.g., 3x8) twice, suggest +5 lbs upper / +10 lbs lower next session. If can't hit bottom of rep range, suggest -10% and rebuild.

**Timestamps:** Every set logged to the Google Sheet must include a timestamp in column K (header: "Timestamp"), format `YYYY-MM-DD HH:MM EDT`. Use the actual Telegram message timestamp from session metadata. Never log without timestamps.

### Meal Logging

When user sends food description or photo:

```bash
python3 scripts/log_meal.py "grilled chicken with rice" --cal 650 --protein 45 --carbs 70 --fat 12 --meal lunch --time 12:30
```

Estimate macros from description, update daily totals, show remaining vs targets.

**⭐ REAL-TIME LOG UPDATE RULE:**
Update `~/Projects/jane-health/nutrition/meals/YYYY-MM-DD.json` IMMEDIATELY every time a new meal or food item is logged — do not wait until end of day or until asked. Every addition, correction, or update must be written to the file right away. Recalculate and overwrite `totals` and `remaining` fields each time. Never leave the file stale.

### Scheduled Check-Ins (via crons)

| Time | Check | Action |
|------|-------|--------|
| **7:00 AM** | Morning | Recovery score, today's workout, macro targets |
| **11:00 AM** | Post-workout | Strain vs target, calories burned, remaining macros, meal suggestion |
| **1:30 PM** | Post-lunch | Silent unless carbs 100g+ behind target |
| **4:00 PM** | Afternoon | Day strain, dinner macro targets, tomorrow's workout |
| **6:00 PM** | Evening | Full day summary, exact dinner macros, tomorrow recommendation |

## WHOOP Recovery Decision Tree

```
GREEN (67-100%): Full session — push volume, good day for PRs
YELLOW (34-66%): Train but -20% volume, -10% load, no failure
RED (0-33%): Rest or active recovery only
2+ consecutive YELLOW: Insert rest day
Any RED: Mandatory rest, don't advance split
```

See `references/whoop-decision-tree.md` for full decision tree with volume adjustments.

## Workout Program

**Split rotation:** Upper A -> Lower A -> Rest -> Upper B -> Lower B -> Rest -> repeat

See `references/workout-splits.md` for complete exercise lists with sets, reps, and rest times.

**Key rules:**
- Compounds first (Big 6: squat, deadlift, bench, OHP, row, chin-up)
- 10-16 hard sets per muscle per week across 2 sessions
- RIR 1-3 on most sets, failure only on last set of isolations
- Sessions under 65 minutes
- Don't train fasted

## Macro Calculation

See `references/macro-guide.md` for full calculation details.

**Base formula (per kg body weight):**
- Protein: 2.2g x kg (every day)
- Training carbs: 4.0g x kg
- Rest carbs: 2.0g x kg
- Fat: fills remaining calories

**WHOOP adjustments:**
- Strain > 14: add 100 cal from carbs
- Strain < 5 on rest day: drop 100 cal from carbs
- RED recovery: switch to rest day macros regardless of schedule

## WHOOP Token Management

- whoopy handles automatic token refresh — no manual re-auth needed
- Tokens stored at `~/Projects/fitness-coach/.whoop_tokens.json`
- Falls back to `~/Projects/whoop-sync/.whoop_tokens_v2.json`
- Credentials at `~/Projects/fitness-coach/.whoop_credentials.json` or `~/Projects/whoop-sync/.whoop_credentials.json`
- If 401 error: silently re-run `python3 scripts/setup_whoop.py --reauth`

## Data Locations

| Data | Path |
|------|------|
| User profile | `~/Projects/fitness-coach/user-profile.json` |
| Daily logs (meals + workouts) | `~/Projects/fitness-coach/logs/{date}.json` |
| PubMed research | `~/Projects/fitness-coach/research/` |
| WHOOP credentials | `~/Projects/fitness-coach/.whoop_credentials.json` |
| WHOOP tokens | `~/Projects/fitness-coach/.whoop_tokens.json` |

## Reference Files

- `references/whoop-protocol.md` — 5x daily check-in protocol, what each check does
- `references/workout-splits.md` — Full Upper A/B Lower A/B split with exercises, sets, reps, rest
- `references/macro-guide.md` — Macro calculation, WHOOP strain adjustments, timing guidelines
- `references/whoop-decision-tree.md` — Recovery % -> training intensity decision tree with volume tables
