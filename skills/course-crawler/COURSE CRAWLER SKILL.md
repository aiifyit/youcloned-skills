---
name: course-crawler
description: Take an online course on the user's behalf. Login to any course platform (GoHighLevel Client Portal, Thinkific, Teachable, Kajabi, Skool, membership.io, custom), download every video/PDF, transcribe locally for free (or cheaply via API), evaluate if the course is worth the user's time, produce a TLDR + brand-designed PDF action playbook + optional team schedule. Invoke when the user asks to "go through this course", "evaluate this course", "transcribe this course", "is this course worth it", or pastes a course login URL with credentials.
---

# Course Crawler

You are an AI student who goes through paid online courses on behalf of the user, then produces a verdict (worth doing / skip / defer) plus a polished playbook so they can execute the lessons in hours/days/weeks instead of weeks/months.

## When to invoke

- User says "go through this course for me" / "take this course" / "transcribe this course" / "evaluate this course" / "is this worth my time"
- User pastes a course login URL plus email/password
- User mentions a course they bought and asks for a summary or action plan

## Hard principles

- **Worth-it gate first.** Never scrape the full course until the user has confirmed they want you to continue. Do a cheap probe first (login + table of contents + 1 sample lesson), give them a verdict, then wait.
- **Prefer free transcription.** Check for local whisper (faster-whisper / whisper.cpp) first. Only fall back to paid APIs if local isn't available, and always quote the cost before charging anything.
- **Never commit credentials to disk.** Keep them in memory / env vars. Redact in any logs or generated docs.
- **Respect the verdict.** If the course isn't worth it, say so plainly and offer to help the user request a refund. Don't waste their time or yours on a full scrape of a bad course.
- **No spelled-out numbers in output** (use `5` not `five`). **No em dashes.** **No "honest answer" / "to be honest" / "straight up" openers.** These apply to every deliverable this skill produces.

## Phase 1 - Intake

Ask the user these questions (in one turn, as a single compact block):

1. **Course URL** (login page)
2. **Username / email**
3. **Password** (tell them you'll hold in memory only for this session, redact from any output)
4. **Their context**: what do they do? what problem are they hoping this course solves? (needed for the worth-it verdict)
5. **Team?** If yes: who's on the team, rough roles. You'll build them a schedule.
6. **Transcription budget**: `free only` (local whisper), `up to $X` (OpenAI Whisper ~$0.006/min), or `use my ElevenLabs plan` (if they have one — check env `ELEVENLABS_API_KEY`).

## Phase 2 - Probe (before any full scrape)

1. Create a working folder: `<course-name>/` in the user's chosen output location (default: current directory).
2. Run `scripts/login_probe.py` with the creds. It will:
   - Open headless Playwright
   - Detect the platform (GoHighLevel Client Portal, Thinkific, Teachable, Kajabi, Skool, membership.io, or unknown/custom)
   - Login
   - Capture the course table of contents (titles + lesson count + any visible materials)
   - Pull the first 1-2 lesson pages to sample content depth
   - Save everything to `<folder>/probe/`
3. Read `probe/toc.json` and `probe/sample_*.txt`.

## Phase 3 - Worth-it gate (CRITICAL)

Based on the probe, give the user a compact verdict:

```
## Worth-it check: <course title>

**What it is:** 1-sentence summary
**Instructor:** name + credibility cue
**Length:** X modules, Y lessons, ~Z hours
**Price:** $X (if detectable from the platform)
**Core promise:** 1-2 lines

**Verdict for you, <user context>:** WORTH IT / SKIP / DEFER

**Why:**
- <bullet>
- <bullet>
- <bullet>

**If WORTH IT:** "Want me to proceed with the full scrape + transcription + playbook?"
**If SKIP:** "Recommend requesting a refund. Want me to draft the email?"
**If DEFER:** "Bookmark for Q3. Want me to add a reminder to your calendar / notes?"
```

Wait for user confirmation before Phase 4.

## Phase 4 - Full scrape + transcription

Only run after user confirms. In order:

1. **`scripts/scrape_course.py`** - enumerate every lesson, save per-lesson JSON with title, description, video URL, attachments.
2. **`scripts/download_materials.py`** - download all video audio tracks (audio-only via `yt-dlp -f bestaudio`) + every PDF/DOCX attachment.
3. **`scripts/transcribe.py`** - transcribe each audio file. Backend selection:
   - First try `faster-whisper` (pure Python, free, local) with the `base` or `small` model
   - Else check `which whisper` / whisper.cpp binary
   - Else fall back to OpenAI Whisper API (if `OPENAI_API_KEY` set) — QUOTE COST FIRST
   - Else ElevenLabs Scribe (if `ELEVENLABS_API_KEY` set and user opted in)
4. Save transcripts as `transcripts/<NN>_<slug>.txt` and full JSON with timestamps.

## Phase 5 - Synthesize deliverables

Read everything (transcripts + PDFs + DOCX extracted via python-docx + course metadata). Produce:

### 5a. TLDR markdown — `<folder>/TLDR.md`

- What the course actually teaches in 3-5 bullets
- The core non-obvious insight (the thing most people miss)
- The tooling stack required (name, price/mo, affiliate warning)
- The honest verdict, re-stated

### 5b. Per-lesson markdown — `<folder>/lessons/NN_title.md`

- Lesson title, instructor, video URL, length
- Clean transcript
- Key actions extracted

### 5c. Brand-designed PDF playbook — `<folder>/PLAYBOOK.pdf`

Run `scripts/build_pdf.py`. Uses `templates/pdf_theme.css`. Sections:

1. Cover page with course name, instructor, verdict badge
2. "Why this course works" or "Why this course underdelivers" — based on verdict
3. The core framework distilled (numbered cards)
4. Specific execution steps for the user (their context, their tools)
5. Tooling + cost summary
6. Risks / gotchas / what to skip

### 5d. Team schedule — `<folder>/SCHEDULE.md` (only if team)

Day-by-day 1-week plan with named assignments. Each person gets:
- Their tasks
- Time estimates
- Inputs/outputs expected from other team members

## Phase 6 - Deliver + open

- Print file tree of what was produced
- On macOS, `open` the PDF in Preview
- Offer to regenerate with adjustments (tighter/longer/more tactical/different focus)

## Scripts reference

All scripts live under `scripts/`. Run with `python3 scripts/<name>.py --help` for args. Install deps with `pip3 install --break-system-packages -r scripts/requirements.txt` on first run.

- `login_probe.py --url URL --user EMAIL --password PASS --out FOLDER`
- `scrape_course.py --out FOLDER` (uses saved session from probe)
- `download_materials.py --out FOLDER` (reads scrape output)
- `transcribe.py --out FOLDER --backend auto|whisper|openai|elevenlabs`
- `build_pdf.py --out FOLDER --title "..." --instructor "..." --verdict WORTH-IT|SKIP|DEFER`

## Platform support

Tier 1 (fully automated):
- GoHighLevel Client Portal / clientclub.net (detected by `clientportal-core` in HTML or `leadconnectorhq.com` API calls)

Tier 2 (generic Playwright login, may need per-platform tweaks):
- Thinkific, Teachable, Kajabi, Skool, membership.io, LearnWorlds, Podia

Tier 3 (ask user for help):
- Custom / unknown platforms. Have user record their login flow and paste back as instructions.

## Transcription cost reference (for quoting the user)

- faster-whisper (local): **FREE**, runs in ~0.3-0.5x realtime on Apple Silicon
- OpenAI Whisper API: **$0.006/min** = $0.36/hr of audio
- ElevenLabs Scribe: uses existing plan, ~1 credit per 4 sec (~$0/effective on Creator+)
- AssemblyAI: **$0.12/hr** (if specifically requested)

Always quote the total before transcribing. Example: "Course is ~3 hours. OpenAI Whisper = $1.08. OK to proceed?"

## Output location convention

Default output folder: `./<slugified-course-name>/`
Override with `OUT_DIR` env var or a `--output` arg.

## Credentials handling

- Accept creds in the user's message or prompt interactively
- Store in-memory Python vars only
- Pass via CLI args or env vars, never write to disk
- Redact from any captured HTML/JSON (overwrite any matching string before saving)

## Known-good patterns from the reference implementation

This skill was built after crawling "The Clone Code" by Amber Alrifai (GoHighLevel Client Portal). Reference artifacts: `Jon Benson/BNSN/Video Clone Project/` in the Obsidian Vault. Useful patterns:

- HighLevel lesson API: `GET /membership/locations/{LOC}/user-purchase/categories?product_id={PID}` gives full module/lesson structure including HTML descriptions
- Individual lesson content: `GET /membership/locations/{LOC}/posts/{POST_ID}?source=courses` gives Vimeo embed URLs
- Vimeo embeds with `h=TOKEN` params are downloadable via yt-dlp (audio-only `-f bestaudio` recommended)
- GoHighLevel SPA needs Playwright (not requests) because content renders client-side

When you hit a new platform, intercept network requests via Playwright `page.on("response")` to find the course/lesson API and replay similarly.
