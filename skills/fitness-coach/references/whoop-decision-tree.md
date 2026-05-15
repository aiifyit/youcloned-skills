# WHOOP Recovery → Training Intensity Decision Tree

Use this tree for every training decision. Recovery score from `scripts/whoop_check.py` determines the day's approach.

---

## Primary Decision Tree

```
WHOOP Recovery Score
│
├── GREEN (67-100%): FULL SEND
│   ├── Train as prescribed from workout-splits.md
│   ├── Push volume to UPPER end of rep ranges
│   ├── This is your day for PRs and heavy singles/doubles
│   ├── OK to train to failure on last set of isolation work
│   ├── Prioritize heaviest compound lift this session
│   ├── Use training day macros
│   └── Strain target: 12-16
│
├── YELLOW (34-66%): MODERATE — ADJUST, DON'T SKIP
│   ├── Train, but reduce load by 5-10%
│   ├── Drop volume by ~20% (cut 1 set from each exercise)
│   ├── Extend rest periods by 30 seconds
│   ├── Stay at RIR 2-3, NO failure work
│   ├── Favor machines/cables over heavy barbell work
│   ├── Use training day macros (still training)
│   ├── Strain target: 10-13
│   │
│   └── IF 2+ consecutive yellow days:
│       ├── Insert mandatory rest day
│       ├── Do NOT advance split rotation position
│       ├── Switch to rest day macros
│       └── Consider: sleep quality? caloric deficit too steep? life stress?
│
├── RED (0-33%): ACTIVE RECOVERY ONLY
│   ├── NO resistance training
│   ├── 20-30 min light walk, yoga, or mobility work
│   ├── Switch to rest day macros
│   ├── Do NOT advance split rotation position
│   ├── Prioritize: sleep, hydration, nutrition
│   ├── Strain target: 4-8
│   │
│   └── IF 2+ consecutive red days:
│       ├── Evaluate: sleep debt? overtraining? illness? extreme stress?
│       ├── Consider increasing calories (especially carbs)
│       ├── Check: is caloric deficit too aggressive?
│       └── May need full deload week
│
└── NO DATA / UNKNOWN
    ├── Treat as YELLOW (moderate approach)
    ├── Train but conservative intensity
    └── Monitor subjective feel
```

---

## WHOOP Override Rules

These rules override the scheduled workout regardless of what the split rotation says:

| Condition | Action | Macro Switch |
|-----------|--------|-------------|
| RED recovery (<34%) | Rest day — no weights | Rest day macros |
| 2+ consecutive YELLOW | Insert rest day | Rest day macros |
| 3+ consecutive YELLOW | Full deload week | Rest day macros all week |
| Any RED after training day | Next day is mandatory rest | Rest day macros |
| GREEN after inserted rest | Resume split where you left off | Training day macros |

---

## Volume Adjustments by Recovery Zone

| Parameter | GREEN (67-100%) | YELLOW (34-66%) | RED (0-33%) |
|-----------|----------------|-----------------|-------------|
| **Load** | As prescribed | -5 to -10% | No lifting |
| **Volume (sets)** | Full prescribed | -20% (cut 1 set/exercise) | 0 |
| **Rep range** | Push upper end | Stay in middle | N/A |
| **Rest periods** | As prescribed | +30 sec each | N/A |
| **Failure training** | Last set isolations OK | Never | Never |
| **Exercise selection** | Free weights primary | Machines/cables OK | Walk/yoga/mobility |
| **Session length** | 55-65 min | 45-55 min | 20-30 min activity |
| **RPE cap** | 8-9 | 7 | 3-4 |

---

## Strain Targets

| Day Type | Target Strain | Warning If |
|----------|--------------|------------|
| Heavy training (GREEN) | 12-16 | > 18 (overreaching) |
| Moderate training (YELLOW) | 10-13 | > 14 (too much for recovery) |
| Rest / Active recovery | 4-8 | > 10 (not recovering) |
| Weekly total | 50-70 | > 80 (overtraining risk) |

---

## HRV Trend Analysis (Weekly)

More important than any single day's score:

```
HRV 7-Day Trend
│
├── TRENDING UP:
│   ├── Training load is well-tolerated
│   ├── Can add volume or intensity next week
│   └── Good sign — keep current approach
│
├── FLAT:
│   ├── Maintaining — no action needed
│   └── Keep current programming
│
└── TRENDING DOWN:
    ├── Accumulated fatigue
    ├── Implement deload week:
    │   ├── Same exercises, same frequency
    │   ├── 50% volume (half the sets)
    │   ├── Same intensity (don't drop weight)
    │   └── Focus on form and mind-muscle connection
    └── If still declining after deload: evaluate sleep/stress/nutrition
```

---

## Joshua's Specific Context

- **HRV baseline:** 17-28ms (low for age 43)
- **RHR baseline:** 66-71 bpm
- **Implication:** Narrower recovery window than average
- **Priority:** Sleep quality is disproportionately important
- **Sensitivities:** Alcohol, poor sleep, and high life stress show up faster in HRV
- **Recommendations:** Magnesium glycinate before bed, strict 7-8hr sleep window, limit caffeine after noon

---

## Auto-Deload Triggers

Implement a deload week (50% volume, maintain intensity) when ANY of these occur:

1. 3+ consecutive yellow recovery days
2. Any red recovery day
3. Weekly HRV average drops >15% from baseline
4. Stalled on multiple lifts for 2+ consecutive sessions
5. Subjective fatigue persists despite adequate sleep/nutrition

After deload: resume split rotation where you left off. WHOOP recovery should climb during deload — if it doesn't, investigate sleep, stress, or nutrition.
