---
name: jon-benson-voice-hacks
description: Jon BNSN's ElevenLabs Voice Hacks. The complete method for getting ElevenLabs to read your script in a real human voice instead of robotic TTS. Covers the 3-script architecture (on-screen Text vs Phonetic vs Tagged), the full v3 audio-tag dictionary, phonetic rewriting rules for acronyms and brand names, tag stacks mapped to VSL story beats, voice-setting tuning recipes (Punchy / Authority / Educational / Storyteller / Conversational), model compatibility (v3 vs v2 vs Flash), SSML break conversion, the pre-send sanitizer, FFmpeg post-processing filters, atempo pacing guidance for cloned voices, HeyGen-specific rules, and a full troubleshooting table. Triggers on /jon-benson-voice-hacks or "render this with ElevenLabs", "make this VO sound human", "fix the pacing", "phonetic version", "tagged version", "ElevenLabs script", "voice script", or any request to turn written copy into spoken voice that actually sells.
---

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

# Jon BNSN's ElevenLabs Voice Hacks

> The complete script-to-voice method as used by Jon Benson, inventor of the VSL and BNSN. Built for AI Collective members and anyone serious about turning written copy into voice that sells.

## When this skill fires - run this workflow

1. **Greet briefly. Ask for the script.**
   - "Drop your script and I'll prep it for ElevenLabs. I'll scan for pronunciation traps first, then render."
   - Accept paste, file path, or "use what's in this chat."

2. **Run the Phonetic Scan (see section below).** Surface every issue. Wait for confirmation before applying.

3. **Apply preprocessing in order:**
   - sanitizeForVO (strip TM/R/C symbols, ellipses)
   - Apply confirmed phonetic conversions
   - Inject inter-sentence breaks (`<break time="0.25s"/>` after every sentence)
   - Apply energy ramp on close (auto-detect + MAX PUNCH on final 3 lines)
   - Convert any `[pause]` markers to `<break time="0.4s"/>` (never 0.8s)

4. **Render via ElevenLabs API.**
   - API key from `$ELEVENLABS_API_KEY` env var
   - Voice ID from `$ELEVENLABS_VOICE_ID` env var
   - If either missing, instruct the user how to set them (see "Set up your voice profile" below)
   - Use locked v2 settings unless user overrides

5. **Save MP3 to user's desktop.** Filename: `{project-slug}-voice.mp3` (or `-v2`, `-v3` if iterating).

6. **Apply FFmpeg post-processing** if available (mono→stereo + trailing silence trim).

7. **Report back:** file path, duration, character cost, any phonetic conversions applied.

## Locked voice settings (tested defaults)

These settings work for most cloned voices. Tune for your voice if needed.

- **modelId:** `eleven_multilingual_v2` (v3 NOT YET supported for most PVCs - see "Pro Voice Clone limitation" below)
- **API key:** read from `$ELEVENLABS_API_KEY` env var. Never hardcode.
- **Voice ID:** read from `$ELEVENLABS_VOICE_ID` env var.

```json
{
  "stability": 0.22,
  "similarity_boost": 0.85,
  "style": 0.55,
  "use_speaker_boost": true
}
```

Stability locked at 0.22 on 2026-05-11 after M7 audio testing. Old 0.30 felt flat (Jon's word). 0.22 gives his voice the dynamic swing his ear actually wants. Never pass a `speed` param: v2 with speed != 1.0 compresses dynamics and flattens energy. Single SLIDR source of truth: `Jon Benson/SLIDR/render/jon-voice-profile.mjs` (all pipelines import from it).

## Phonetic Scan (run before every render)

The model can't tell which words are acronyms, brand names, or homographs - it guesses. Wrong guesses ruin a take. Scan first, fix, then render.

**What to detect:**

1. **Acronyms (ALL-CAPS strings, 2+ letters, not single 'A' or 'I'):**
   - Pattern: `\b[A-Z]{2,}\b`
   - For each: ask the user "letter-by-letter (V-S-L) or pronounce as a word (NASA)?"
   - Default suggestion: hyphenate (it's the safer fail mode)

2. **Invented brand names / capitalized non-dictionary words:**
   - Pattern: capitalized word not in standard dictionary, OR known invented-brand pattern (mixed-case like "BNSN", "TLDR", made-up combos like "FastlyX")
   - For each: ask "how should this sound?" with options:
     - Hyphenate (B-N-S-N)
     - Pronounce as a word ("Benson" - if BNSN should rhyme with "Benson")
     - Native (let the model handle it - works for NotebookLM, ChatGPT, GitHub)
     - Custom phonetic spelling

3. **Homographs (word has 2+ valid pronunciations):**
   - Watch list: `lead, read, wind, tear, bow, polish, dove, refuse, content, present, object, lives, contract, desert, sow, bass, wound, close`
   - For each occurrence: ask which pronunciation, force phonetically (e.g., "lead" → "led" if metal)

4. **Numbers (digits, dollar amounts, percentages):**
   - For VO: spell out (`$797` → `seven hundred ninety-seven dollars`)
   - For VSL Text on screen: leave as-is
   - Auto-convert with confirmation

**Output format for the scan:**

```
PHONETIC SCAN of your script:

Acronyms found (3):
  • "VSL" x4 → suggest: V-S-L  [confirm/word/custom]
  • "AI" x12 → suggest: A-I    [confirm/word/custom]
  • "TLDR" x2 → suggest: T-L-D-R  [confirm/word/custom]

Invented brand names (2):
  • "BNSN" x6 → how should this sound? [hyphenate/word/native/custom]
  • "Acmecorp" x3 → how should this sound? [hyphenate/word/native/custom]

Homographs (1):
  • "lead" x1 ("...he was a lead developer...") → present tense verb? Force "leed" or leave?

Numbers (8):
  • $797 → seven hundred ninety-seven dollars (auto-convert? y/n)
  • 25% → twenty-five percent (auto-convert? y/n)

Ready to apply. Confirm with 'go' or paste corrections.
```

After the user confirms, apply all conversions to produce the VO Phonetic version. Then proceed to render.

## About this document

**Compiled and curated by Jon Benson.** Some of what's in here is original, some is the best of what the community has figured out. Both pieces matter. Here's the split.

**Original to this method (Jon's):**
- The 3-script architecture (VSL Text / VO Phonetic / VO Tagged)
- The phonetic rewriting rules for branded vocabulary (BNSN, SLIDR, VSL, etc.)
- The Tag Stacks Mapped To VSL Story Beats section (avoidance modality, open loops, pattern interrupts, reveals, CTAs, P.S.) tying audio-tag stacks to VSL frameworks
- The two voice-settings tuning recipes (Punchy VSL vs. Educational)
- The HeyGen-specific phonetic-strip rule and the ElevenLabs-as-audio-source upgrade path
- The pre-send sanitizer pattern (sanitizeForVO)
- The FFmpeg post-processing filter chain (mono-to-stereo + silence trim)

**Compiled from community + official sources (credited at bottom):**
- The full ElevenLabs v3 audio tag dictionary (emotion, delivery, pacing, reactions, sound effects, accents, character voices, experimental)
- Tag stacking patterns table
- Punctuation as a voice tool
- Model compatibility matrix (v3 vs v2 vs Flash vs English v1)
- Troubleshooting table including the PVC vs IVC discovery from community testing
- SSML phoneme tag compatibility notes

The value here is the curation: pulling scattered community knowledge into one usable dictionary, then mapping it onto a VSL framework that actually drives conversion. Sources credited at the bottom.

---

Spoken text needs different rules than written text. Cloned voices on ElevenLabs sound robotic by default: rushed pacing, flat emphasis, uptalk on short fragments, dead air on badly-placed break tags. This skill encodes a working recipe for natural, energetic delivery, tested across hundreds of renders.

---

## The shortcut nobody talks about

The tools are good enough now that the gap between "AI voice" and "real voice" is no longer the model. It's the script. Three scripts, actually.

## Why three scripts (not one)

Most people send the same text to the screen, the avatar, and the voice engine. Then they wonder why it sounds robotic, says "Vee Ess Ell" instead of "V-S-L," or pronounces BNSN like "binson."

The fix is small in concept, big in result: separate what the audience READS from what the engine SAYS from what the engine PERFORMS.

- **VSL Text** is for the eye. Letter-perfect. Brand spelling intact. This is what shows on screen, lives in the PDF, gets pasted in the email.
- **VO Phonetic** is for the engine that has to pronounce it. Acronyms hyphenated. Brand names spelled the way they sound. No tags, because some engines (HeyGen) read tags out loud.
- **VO Tagged** is for ElevenLabs v3, where you direct the performance with bracket tags: emotion, pace, breath, emphasis.

Three scripts means you stop fighting the tools. Each one gets exactly what it expects.

---

## How to use this skill (interactive build mode)

When this skill fires, run a three-question interview before producing anything. Ask one question at a time, wait for the answer, then move on. Friendly, fast, no fluff.

### Q1. Where's the script?

> "Got a video script? Paste it here, or want me to pull from what's already in this chat? Pasting is safer. I won't miss anything."

If they paste, use that exact text as the source. If they say "use what's here," scan the recent chat context for the most recent script-shaped block (paragraph form, sentences meant to be spoken, not Q&A or lists). Confirm the source before continuing: "Pulling this: [first sentence]... [last sentence]. Right one?"

### Q2. Where's it going?

> "Sending this to ElevenLabs, HeyGen, or both?"

Map the answer to which deliverables you produce:

| Answer | Produce |
|---|---|
| ElevenLabs only | VSL Text + VO Tagged |
| HeyGen only | VSL Text + VO Phonetic |
| Both | VSL Text + VO Phonetic + VO Tagged |

VSL Text is always produced. It's what the audience reads on screen.

### Q3. Which voice style?

> "Pick one of these five, or describe your own:
> 1. **Hard Pitch**: high energy, fast, aggressive sales close
> 2. **Authority**: calm, deliberate, confident (Tucker / Huberman / Joe Rogan tone)
> 3. **Excited Teacher**: building tension, friendly, lively
> 4. **Storyteller**: slower, dramatic, emotional pauses
> 5. **Conversational Friend**: casual, peer-to-peer, lighthearted
> 6. **Custom**: describe it in your own words"

Map their choice to the matching style profile below. The profile drives:
- Which tag palette dominates the VO Tagged version
- Which ElevenLabs voice settings to recommend
- Which HeyGen avatar archetype to suggest

### Style profiles

**1. Hard Pitch**
- Dominant tags: `[excited]`, `[emphasized]`, `[stress on next word]`, `[loudly]`, `[rapid-fire]`
- ElevenLabs settings: stability 0.30, similarity 0.85, style 0.50, speed 1.0
- HeyGen avatar suggestion: confident upper-body avatar, business casual, direct gaze
- Pace: fast. Punctuation: short sentences, lots of periods.

**2. Authority**
- Dominant tags: `[serious tone]`, `[deliberate]`, `[conversational tone]`, `[matter-of-fact]`, `[confident]`
- ElevenLabs settings: stability 0.55, similarity 0.85, style 0.25, speed 1.0
- HeyGen avatar suggestion: seated professional avatar, neutral background
- Pace: measured. Punctuation: full sentences, occasional pauses.

**3. Excited Teacher**
- Dominant tags: `[excited]`, `[cheerfully]`, `[curious]`, `[continues after a beat]`, `[playfully]`
- ElevenLabs settings: stability 0.40, similarity 0.85, style 0.40, speed 1.0
- HeyGen avatar suggestion: friendly avatar, slight movement, warm expression
- Pace: lively but clear. Punctuation: enthusiastic but not screaming.

**4. Storyteller**
- Dominant tags: `[reflective]`, `[drawn out]`, `[long pause]`, `[wistful]`, `[dramatic tone]`
- ElevenLabs settings: stability 0.50, similarity 0.90, style 0.45, speed 1.0
- HeyGen avatar suggestion: standing or seated narrator avatar, cinematic feel
- Pace: slow. Punctuation: deliberate pauses, ellipses, sentence fragments.

**5. Conversational Friend**
- Dominant tags: `[conversational tone]`, `[lighthearted]`, `[playfully]`, `[casual]`, `[continues softly]`
- ElevenLabs settings: stability 0.50, similarity 0.85, style 0.30, speed 1.0
- HeyGen avatar suggestion: relaxed seated avatar, natural lighting
- Pace: easy. Punctuation: contractions, sentence fragments, "you know" beats.

**6. Custom**
- Ask the user to describe the feel in their own words ("aggressive ESL," "thoughtful indie filmmaker," "late-night radio host," etc.)
- Pick 3-5 tags that match their description from the Audio Tag Dictionary section
- Suggest stability/style settings based on whether their description leans expressive (low stability) or steady (high stability)

### Output format

After all three answers, produce the deliverables as **copy-paste-ready blocks** with clear labels.

```
=== VSL TEXT (on screen) ===
[the on-screen letter-perfect version]

=== VO PHONETIC (paste into HeyGen input_text) ===
[the phonetic-only version, no tags]

=== VO TAGGED (paste into ElevenLabs v3) ===
[the tagged version with audio cues]

=== Voice settings for ElevenLabs ===
- Model: eleven_v3 (or eleven_multilingual_v2 if your voice is a PVC, see Model Matrix)
- Stability: 0.40
- Similarity boost: 0.85
- Style: 0.40
- Speed: 1.0

=== HeyGen avatar suggestion ===
[avatar archetype, e.g., "friendly upper-body presenter"]
```

The user copy-pastes each block into the right tool.

### When to skip the interview

If the user is clearly mid-flow (already deep in a project, or they paste a script with explicit instructions like "make this Hard Pitch for ElevenLabs only"), skip the questions and produce immediately. Use judgment. The interview is for cold starts.

---

## How this layers with on-screen copy rules

Most copy rules (no wide-dash characters on screen, no spelled-out numbers, no "it's not X it's Y" framework, no rhetorical-question openers) apply to **VSL Text only** - the on-screen, written-deliverable version.

In the **VO scripts**, you can break some on-screen rules because they're directives to the TTS engine, never seen by the audience:

- The wide-dash character can cue strong pause beats in v3 (use sparingly; the audience never sees it)
- Spelled-out numbers ("one billion") may read more naturally than "$1B" depending on voice
- ALL CAPS for emphasis is a TTS instruction, not a stylistic choice

The rule: ban what the AUDIENCE sees. Direct what the AUDIENCE hears.

---

## The 3-script architecture

For any project where a script gets BOTH displayed on screen AND spoken aloud (VSLs, training modules, podcast hosts), maintain three versions of the same line.

### 1. VSL TEXT (on-screen, letter-perfect)
- Used for closed captions, on-screen text, written deliverables (PDFs, blog posts, emails).
- Brand names, acronyms, technical terms spelled correctly. "BNSN", "SLIDR", "VSL".
- No emphasis tags, no phonetic rewrites. This is the source of truth for what the audience READS.

### 2. VO PHONETIC (HeyGen and any TTS without tag support)
- Same text as VSL Text, but acronyms and brand names rewritten phonetically.
- "BNSN" becomes "Benson" or "B-N-S-N" depending on how it should sound.
- "SLIDR" becomes "Slider".
- "VSL" becomes "V-S-L" (so the TTS reads each letter, not "vissle").
- HeyGen's TTS strips ElevenLabs-style audio tags. Use this version for HeyGen.

### 3. VO TAGGED (ElevenLabs v3 only)
- VO Phonetic version PLUS audio tags for emphasis, pauses, emotion.
- Send only to ElevenLabs v3. Do not send to v2 or Flash; tags get read aloud as text.
- Example: `[excited]With Benson and Slider combined you'll get [strong]a fantastic V-S-L.`

---

## Phonetic rewriting rules

### Acronyms
| Pronounced as letters | Pronounced as a word |
|---|---|
| VSL becomes "V-S-L" | NASA becomes "NASA" or "Nasa" |
| AI becomes "A-I" | LASER becomes "laser" |
| CEO becomes "C-E-O" | SCUBA becomes "scuba" |
| API becomes "A-P-I" | RADAR becomes "radar" |

Test with the actual voice. Some acronyms read better one way for a specific voice. Always use hyphens between letters when you want letter-by-letter delivery.

### Brand names
- BNSN becomes "Benson" (intended pronunciation, not "binson")
- SLIDR becomes "Slider"
- BNSN.ai becomes "Benson dot A-I"
- jonbenson.com becomes "Jon Benson dot com"
- Mailvio becomes "Mail Vee Oh" if not pronounced consistently
- Always pre-test new brand names; phonetic spelling may shift per voice

### Numbers
- $1B becomes "one billion dollars" if you want it spoken in full
- $1B becomes "one B" if you want shorthand
- 2026 becomes "twenty twenty-six"
- 50% becomes "fifty percent"
- Never spell numbers in VSL Text. Phonetic rewrite is for VO only.

### Names
- Foreign or unusual names: write the phonetic spelling
- "Andrej Karpathy" becomes "Ahn-dray Kar-PAH-thee"
- Test with the voice. Adjust syllable breaks until it lands.

### Homograph trap (auto-scan recommended)

Words that have 2 valid pronunciations: lead, read, wind, tear, bow, polish, dove, refuse, content, present, object, lives, contract, desert, sow, bass. v2 and v3 sometimes pick the wrong one based on context. If a word in your script is a homograph, force the pronunciation phonetically:
- `lead` (metal) becomes `led`
- `read` (past tense) becomes `red`
- `wind` (to coil) becomes `wynd`

One mispronounced word can blow the entire voiceover. Scan before rendering.

---

## ElevenLabs v3 audio tag dictionary

These tags ONLY work with the `eleven_v3` model. On v2 / Flash / English v1, they get read aloud as text. Always confirm model before using.

### Emotion tags
`[excited]` `[happy]` `[happily]` `[cheerfully]` `[sad]` `[sorrowful]` `[angry]` `[frustrated]` `[annoyed]` `[nervous]` `[anxious]` `[afraid]` `[hesitant]` `[timidly]` `[tired]` `[exhausted]` `[deadpan]` `[flatly]` `[calm]` `[resigned tone]` `[sarcastic]` `[playfully]` `[mischievously]` `[curious]` `[awe]` `[regretful]` `[flustered]` `[lighthearted]` `[reflective]` `[wistful]` `[serious tone]` `[dramatic tone]` `[matter-of-fact]` `[conversational tone]` `[confident]`

### Delivery / volume tags
`[whispers]` `[whispering]` `[speaking softly]` `[quietly]` `[understated]` `[loudly]` `[shouts]` `[shouting]` `[emphasized]` `[stress on next word]` `[strong]` `[dramatic]`

### Pacing tags
`[pause]` `[short pause]` `[long pause]` `[continues after a beat]` `[continues softly]` `[rushed]` `[rapid-fire]` `[slows down]` `[drawn out]` `[deliberate]` `[stammers]` `[repeats]`

### Reaction / non-verbal tags
`[laughs]` `[laughs softly]` `[laughs harder]` `[starts laughing]` `[giggle]` `[giggles]` `[light chuckle]` `[snorts]` `[wheezing]` `[sighs]` `[exhales]` `[breathes]` `[gasps]` `[gulps]` `[clears throat]` `[crying]` `[sniffling]` `[yawning]` `[coughing lightly]` `[hiccuping]`

### Multi-voice dialogue
`[interrupting]` `[overlapping]` `[cuts in]`

### Sound effects
`[applause]` `[clapping]` `[gunshot]` `[explosion]` `[door creaks]` `[footsteps]` `[telephone rings]` `[drumroll]` `[bird chirping]` `[woo]`

### Accent tags
Use `[strong X accent]` where X is the language or region. Examples: `[strong French accent]`, `[strong British accent]`, `[Southern US accent]`, `[Irish accent]`, `[Australian accent]`, `[strong Russian accent]`. Accent results vary; test with each voice.

### Character voice tags (experimental)
`[pirate voice]` `[evil scientist voice]` `[deep voice]` `[robotic tone]` `[fantasy narrator]` `[sci-fi AI voice]`

### Special / experimental
`[sings]` `[singing]` `[robotic]` `[woo]`

### Tag rules
- No closing tags. Effects fade or end at the next contradicting tag, end of sentence, or end of line.
- Tags are case-insensitive but lowercase is conventional.
- Tags can sit anywhere in a line: at the start, mid-sentence, before a specific word.
- Stacking is allowed: `[excited][whispers]` produces excited whispering.
- Match tag to voice. A meditative voice cannot convincingly `[shout]`.
- Audio tags are still officially experimental. Some may be ignored, others may be read aloud. Always test the output, do not ship blind.

---

## Tag stacks mapped to VSL story beats

Most v3 guides treat audio tags as decoration. They're not. Map them to the beats of a VSL and they become a performance director.

### Avoidance modality beat (loss / fear / cost)
The reader is about to lose something. Voice should slow, drop, get tighter.
- `[serious tone][slows down]` for setup ("Most people are about to lose...")
- `[regretful][quietly]` for the cost ("...and they don't even know it.")
- `[pause]` before the next line to let it land

### Open loop beat (curiosity gap)
You drop a hook. The voice should rise into it, then cut.
- `[curious][stress on next word]` on the hook word
- `[short pause]` after the loop opens
- `[continues softly]` to keep the reader leaning in

### Pattern interrupt beat
Reader's mind is wandering. Hit them with a sudden voice shift.
- `[loudly][excited]` on a single short fragment
- `[pause]` to reset
- `[conversational tone]` returns

### Reveal beat (the payoff)
The voice has been building. Now release.
- `[dramatic][slows down]` for the buildup
- `[long pause]`
- `[confident][emphasized]` on the reveal

### CTA beat (close)
Authority + warmth. Direct, not pushy.
- `[deliberate][confident]` for the call
- `[stress on next word]` on the verb ("Click. Now.")
- Avoid `[excited]` here. Excited reads as desperate at the close.

### P.S. beat (the second subject line)
P.S. lines work in audio too, especially in podcasts and audio ads.
- `[conversational tone][lighthearted]` so it feels like an aside
- `[continues after a beat]` to suggest the speaker thought of one more thing

---

## Stacking patterns that work

| Goal | Stack |
|---|---|
| Conspiratorial whisper | `[whispering][pause]` |
| Conflicted delivery | `[hesitant][regretful]` |
| Layered character | `[dramatic][French accent]` |
| Frustrated accent | `[British accent][exasperated]` |
| Excited applause | `[excited][clapping]` |
| Tired sigh | `[sighs][tired]` |
| Angry laugh | `[angry][laughing]` |
| Sad whisper | `[sad][whispers]` |
| Nervous whisper | `[nervously][whispers]` |
| Enthusiastic shout | `[happily][shouts]` |

---

## Punctuation as a voice tool

Outside of bracket tags, ElevenLabs reads punctuation as performance cues. Works on v2 and Flash too, not just v3.

| Punctuation | Effect |
|---|---|
| `.` (period) | Full stop, breath beat |
| `,` (comma) | Short rhythm break |
| `;` (semicolon) | Slightly longer than comma |
| `:` (colon) | Setup pause before payoff |
| `...` (ellipsis) | Hesitation, drawn-out drift |
| Long dash (the wider one) | Strong abrupt break (only in VO scripts, never on-screen) |
| `?` | Rising inflection |
| `!` | Punch, raised energy |
| ALL CAPS | Stronger emphasis on that word, often louder |

### CAPS for emphasis
Capitalizing a single word makes it land harder. "I want this to WORK." outperforms "I want this to **work**." Bold formatting does not transfer through TTS. Caps do.

**Avoid CAPS on acronyms you need read letter-by-letter.** Use spaces or hyphens instead: write `T L D R` or `T-L-D-R`, not `TLDR`.

### Ellipsis vs. pause tag
- `...` produces a short hesitation, organic drift
- `[pause]` produces a deliberate beat (v3 only; convert to SSML `<break>` for v2)
- `[long pause]` produces dramatic silence

Use ellipsis when the speaker is thinking or trailing off. Use pause tags when you want a clean beat.

---

## Set up your voice profile

You'll need:

- **Your voice ID** from ElevenLabs (Voices tab > pick your clone > copy the ID)
- **Your API key** from ElevenLabs settings
- **A target model** (see Model Compatibility Matrix below for which model your voice supports)

Stash the voice ID and key in environment variables. Don't hardcode them.

```bash
export ELEVENLABS_API_KEY="..."
export ELEVENLABS_VOICE_ID="..."
```

### Voice settings (per-voice tuning)

These live in the ElevenLabs API call (`voice_settings` object).

| Setting | Range | Effect | Starting point for natural VSL |
|---|---|---|---|
| `stability` | 0.0 to 1.0 | Lower = more emotional variety, higher = consistent monotone | 0.30 to 0.50 |
| `similarity_boost` | 0.0 to 1.0 | How closely to match cloned voice timbre | 0.75 to 0.90 |
| `style` | 0.0 to 1.0 | Style exaggeration; amplifies emotion tags | 0.20 to 0.50 |
| `use_speaker_boost` | bool | Adds clarity, slight processing | true |
| `speed` | 0.5 to 2.0 | Playback speed | 1.0 |

**Tune these for YOUR voice.** Generic recipes below are starting points. Render a 30-second sample, listen, adjust one setting at a time. Most clones land in this range:

- **Stability 0.30 to 0.50** - lower for emotional VSL reads, higher for steady educational reads
- **Similarity 0.85** - good default for most cloned voices
- **Style 0.30 to 0.50** - drives expressiveness on punch words

### Tuning recipe for punchy VSL reads
- stability: 0.35
- similarity_boost: 0.85
- style: 0.40
- speaker_boost: true
- speed: 1.0

### Tuning recipe for calm educational reads
- stability: 0.55
- similarity_boost: 0.85
- style: 0.20
- speaker_boost: true
- speed: 1.0

### Set as default on your voice (optional)

Persist them to the ElevenLabs account so every future generation uses them by default:

```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/$ELEVENLABS_VOICE_ID/settings/edit" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"stability": 0.35, "similarity_boost": 0.85, "style": 0.40, "use_speaker_boost": true}'
```

---

## Pre-send text sanitization

Run this on ALL text before sending to ElevenLabs. Confirmed footguns from production:

```javascript
// Strip commas from numbers (1,200 -> 1200, 1,000,000 -> 1000000).
// ElevenLabs v2 mispronounces comma-separated numbers (says "one
// comma two hundred" or sounds out digits). Plain numerals it speaks
// correctly as "one thousand two hundred".
function stripNumberCommas(text) {
  let out = String(text);
  let prev;
  do {
    prev = out;
    out = out.replace(/(\d),(\d{3})(?!\d)/g, '$1$2');
  } while (out !== prev);
  return out;
}

function sanitizeForVO(text) {
  return stripNumberCommas(String(text)
    .replace(/™/g, '')   // spoken aloud as "trademark"
    .replace(/®/g, '')   // spoken aloud as "registered"
    .replace(/©/g, '')   // spoken aloud as "copyright"
    .replace(/…/g, ' ')  // unicode ellipsis becomes a space (see ellipsis rule below)
    .replace(/\.{2,}/g, ' ') // ascii multi-dot becomes a space
    .replace(/\s+/g, ' ')
    .trim());
}
```

**Ellipsis rule (for VSL scripts):** Raw ellipses (`...`) in scripts often signal a NEW IDEA, not a pause. Converting ellipses to SSML breaks creates 1-2 second gaps. Strip them to a space; paragraph breaks provide rhythm. (If you want a hesitation beat, use `[pause]` on v3 or `<break time="0.4s"/>` on v2 instead.)

**Bracket pause tags ARE intentional.** `[pause]` and `[pause long]` in scripts are deliberate delivery cues and must be converted to SSML `<break>` (not stripped) when sending to v2.

---

## Markup rules (v2 vs v3)

### If you're on v3
- Bracket audio tags work natively. Use the full dictionary above.
- `[pause]`, `[short pause]`, `[long pause]` work natively.
- SSML `<break>` does NOT work on v3. If you need exact-duration pauses, use Flash v2 with SSML break tags instead.
- ALL CAPS for one-word emphasis works.
- Punctuation drives micro-pacing.

### If you're on v2 / Flash / English v1
1. **Strip bracket audio tags** before sending. v2 will read `[excited]` aloud as the word "excited."
2. **Convert `[pause]` markers to SSML `<break>`** before sending:
   ```javascript
   text.replace(/\[pause\]/g, '<break time="0.4s"/>');
   ```
   Note: `<break time="0.8s"/>` ("long pause") sounds forever and breaks immersion. Tested and rejected. Cap at 0.4s even at major punch beats.
3. **Inject inter-sentence breaks (REQUIRED for natural rhythm).** v2 collapses pauses between sentences without explicit breaks. The voice rushes through and runs sentences together. Inject breaks automatically after every sentence boundary - see preprocessor below. The old "1 break per 150 words MAX" rule is wrong for v2; you actually want one between every sentence at ~0.25s.
4. **Trust punctuation for micro-pacing.** Commas, ellipses give v2 organic rhythm within a sentence.
5. **ALL CAPS for one-word emphasis.** v2 honors caps as a stress cue. Use sparingly in opening/middle, ramp up in close.
6. **Phonetic spell-out for acronyms** read letter-by-letter (V-S-L, A-I, T-L-D-R, A-P-I, etc.).

### Inter-sentence break injection (run on every v2 script)

The model collapses pauses between sentences. Paragraph breaks alone are not enough. Run this preprocessor on every script before sending to v2:

```python
import re

def inject_inter_sentence_breaks(text):
    # 0.25s after period/question + space + capital letter
    text = re.sub(r'\. ([A-Z])', r'.<break time="0.25s"/> \1', text)
    text = re.sub(r'\? ([A-Z])', r'?<break time="0.25s"/> \1', text)
    # 0.2s after exclamation (shorter to preserve urgency)
    text = re.sub(r'! ([A-Z])', r'!<break time="0.2s"/> \1', text)
    # 0.3s between paragraphs
    text = re.sub(r'\.\n\n', r'.<break time="0.3s"/>\n\n', text)
    text = re.sub(r'!\n\n', r'!<break time="0.25s"/>\n\n', text)
    return text
```

For an 8K-character VSL, expect ~140 break tags. That sounds like a lot, but it's what produces natural human-speech rhythm on v2. It's the missing default.

### Critical: render the full script as ONE call

Rendering each beat or paragraph separately and stitching with silence produces fragmented delivery. Always render the full script as one continuous ElevenLabs call. The model needs the full context to flow naturally between sections.

If your script is over 10,000 characters (single-call cap), split at paragraph boundaries into ~8,000-char chunks and render each chunk continuously. Crossfade or hard-cut between chunks in post.

---

## Avoiding uptalk (California accent)

ElevenLabs pitches up on short sentence fragments. If you hear uptalk:
- Merge fragments into flowing sentences with commas
- Bad: `Every role in your business. Cloned from you. Working 24/7.`
- Good: `Every role in your business, cloned from you, working 24/7 while you sleep.`

Default to full sentences. Fragments are a punch tool, not the default.

---

## Energy ramp on the close (CTA)

v2 has a flat default delivery. Without explicit markup, the close lands monotone and the final CTA reads boring. Voice settings can't save flat copy - the markup has to drive the rise. Convention:

**Auto-detect the close.** From the "decision to make" / scarcity / CTA language onward, ramp:
- CAPS density goes up (more emphasis words per paragraph)
- Exclamation marks replace periods on urgency lines
- Action verbs lead the CTA (`click` over `look`, `grab` over `consider`)

**MAX PUNCH on the final 3 lines** of any close. Every key word CAPS, every line ends in `!`. Example:
- Flat: `Thanks so much. Click below. I'll see you inside.`
- Punch: `Thanks SO much! CLICK below! I'll SEE you INSIDE!`

The difference between those two on v2 is night and day. Without the punch markup, v2 reads the second sentence with the same flat tone as the first. With it, the close actually closes.

**Override markers** if you want to control the ramp manually:
- `[ENERGY:rising]` at any paragraph to start the ramp earlier than auto-detect
- `[!]` at end of a single line to mark "hit this line hard"

---

## Post-processing (FFmpeg audio filters)

After every ElevenLabs render, apply this filter chain before measuring clip duration or mixing into video:

```
aformat=channel_layouts=stereo,areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-45dB,areverse
```

Or as a constant:

```javascript
export const VOICE_FFMPEG_FILTERS = [
  'aformat=channel_layouts=stereo',
  'areverse',
  'silenceremove=start_periods=1:start_duration=0.05:start_threshold=-45dB',
  'areverse',
].join(',');
```

What each filter does:
- `aformat=channel_layouts=stereo`: ElevenLabs outputs mono MP3. Without this, audio plays in the left ear only.
- `areverse` + `silenceremove` + `areverse`: Trims trailing silence (reverse, remove leading silence, reverse back). ElevenLabs adds 0.5-1.5s of silence at the end of every clip, which causes gaps when you stitch clips together.

Apply with ffmpeg:

```bash
ffmpeg -i input.mp3 -af "$VOICE_FFMPEG_FILTERS" output.mp3
```

---

## Atempo: pacing tightening for cloned voices

Some cloned voices come back slightly slow at speed 1.0 and feel laggy on a tight VSL. A small atempo speedup tightens the pace without sounding rushed. **Test on your voice before adopting.**

- **atempo=1.05 to 1.08** tightens about 5-8%, often the sweet spot for laggy clones. Preserves pitch.
- Don't go above 1.10 (sounds rushed) or below 0.90 (sounds dying).
- For a 2:27 target video, a natural render around 2:28-2:30 with atempo 1.08 lands at ~2:18-2:20.

```bash
ffmpeg -i input.mp3 -af "atempo=1.08" output.mp3
```

**Caution: Some Pro Voice Clones (PVCs) are already paced perfectly at speed 1.0.** Adding atempo on a correctly-paced voice produces a chipmunk effect. Always render a sample first at speed 1.0 with no atempo. If it sounds right, leave it alone. Only add atempo if the natural render genuinely feels slow.

---

## Working API call shape

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$ELEVENLABS_VOICE_ID" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/mpeg" \
  -o output.mp3 \
  -d '{
    "text": "<your text with strategic punctuation, ALL CAPS for emphasis, phonetic acronyms, and at most one or two SSML <break time=\"0.7s\"/> at major beat boundaries>",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.35,
      "similarity_boost": 0.85,
      "style": 0.40,
      "use_speaker_boost": true
    }
  }'
```

### Reusable render helper

```javascript
const VOICE_PROFILE = {
  voiceId: process.env.ELEVENLABS_VOICE_ID,
  modelId: 'eleven_multilingual_v2',  // or 'eleven_v3' for tagged scripts
  settings: {
    stability: 0.35,
    similarity_boost: 0.85,
    style: 0.40,
    use_speaker_boost: true,
  },
};

function markersToSSML(text) {
  return text
    .replace(/\[pause long\]/g, '<break time="0.8s"/>')
    .replace(/\[pause\]/g, '<break time="0.4s"/>');
}

async function renderVoice(rawText, apiKey) {
  const text = markersToSSML(rawText);
  const r = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_PROFILE.voiceId}`,
    {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
      },
      body: JSON.stringify({
        text,
        model_id: VOICE_PROFILE.modelId,
        voice_settings: VOICE_PROFILE.settings,
      }),
    }
  );
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
  return Buffer.from(await r.arrayBuffer());
}
```

Drop this into any project that renders your voice.

---

## Model compatibility matrix

| Feature | v3 (alpha) | v2 multilingual | Flash v2 | English v1 |
|---|---|---|---|---|
| Audio tags | YES | NO | NO | NO |
| `[pause]` family | YES | NO | NO | NO |
| SSML `<break>` | NO | YES | YES | YES |
| SSML `<phoneme>` (IPA, Arpabet) | NO | NO | YES | YES |
| Punctuation pacing | YES | YES | YES | YES |
| ALL CAPS emphasis | YES | YES (subtle) | YES (subtle) | YES (subtle) |
| Voice cloning quality | High | High | Medium | Medium |
| Speed | Slow | Fast | Fastest | Fast |

### When to use which model
- **VSL with emotion + punch** > v3 (with audio tags) IF your voice supports v3
- **Steady educational tutorials** > v2 multilingual (stable, fast)
- **Real-time / low latency** > Flash v2
- **Forced phonetic pronunciation needed** (e.g., medical terms) > Flash v2 or English v1 with SSML phoneme tags

### v3 pause family (only on v3)
`[pause]`, `[short pause]`, `[long pause]`. v3 does NOT support SSML `<break time="2s" />`. If you need exact-duration pauses, use Flash v2 with SSML break tags instead.

### CRITICAL: `[pause]` markers are NOT native to v2 (footgun)

If you write `[pause]` in raw text and send it to `eleven_multilingual_v2`, the model reads "pause" out loud as a word. Bracket tags only work natively on v3. On v2, you must convert them BEFORE sending to the API.

Standard conversion:
```javascript
function markersToSSML(text) {
  return text
    .replace(/\[pause long\]/g, '<break time="0.8s"/>')
    .replace(/\[pause\]/g, '<break time="0.4s"/>');
}
```

SSML `<break>` tags ARE honored on v2, Flash v2, and English v1 (but NOT on v3). Run this conversion as the last step before the POST body. Same applies for any `[short pause]`, `[long pause]`, or other bracket markers in source scripts.

When in doubt, raw test on the target model:
```bash
curl ... -d '{"text":"hello [pause] world","model_id":"eleven_multilingual_v2",...}'
```
If you hear the word "pause," your text needs pre-processing.

---

## Pro Voice Clone (PVC) limitation

ElevenLabs fine-tunes each Professional Voice Clone (PVC) for specific models. v3 alpha is NOT yet in the fine-tuned list for most PVCs. When you send a v3 request with a PVC voice ID, the API quietly falls back to a generic v3-compatible voice. The audio tags work, but you lose your voice.

**How to verify before rendering anything for production:**
```bash
curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" \
  "https://api.elevenlabs.io/v1/voices/$ELEVENLABS_VOICE_ID" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fine_tuning',{}).get('state'))"
```

If `eleven_v3` is not in the dict (or not `fine_tuned`), v3 with that voice will use a fallback voice, not yours.

**Workarounds:**
1. **Stick with v2** until ElevenLabs ships v3 fine-tuning for PVCs (expected at v3 GA). Tagged audio tags will be ignored, but the voice is yours.
2. **Strip tags before sending to v2** so they don't get read aloud. Keep `[pause]` (after SSML conversion), ALL CAPS, ellipses, punctuation: those work on v2.
3. **Create an Instant Voice Clone (IVC) sidecar** if you need v3 tags + a similar-sounding voice today. Different fingerprint, lower fidelity than your PVC, but renders v3 tags. Use only for prototyping the tag-stack feel.

**Re-check weekly.** ElevenLabs is shipping v3 fine-tuning rollouts.

---

## HeyGen-specific rules

HeyGen's TTS does NOT understand ElevenLabs audio tags. Tags will be read aloud as text. For HeyGen scenes:

1. Take the VO Tagged script
2. Strip every bracket-tag pattern: `/\[[^\]]+\]/g`
3. Keep phonetic spellings, ALL CAPS emphasis, ellipses, punctuation
4. Send the cleaned phonetic version to HeyGen's `input_text` field

If you want true voice control on HeyGen:
- Pre-generate audio with ElevenLabs v3 (full tags)
- Upload the MP3 to HeyGen as the avatar's audio source via `voice.type = "audio"` instead of `"text"`
- HeyGen lip-syncs the avatar to your audio, ignoring its own TTS entirely

This is the highest-quality path. Default for fast-turn projects: phonetic-only on HeyGen.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Tags being read aloud | Wrong model (using v2 / Flash with tags) | Switch to `eleven_v3` |
| Tags ignored, no effect | Voice mismatch (meditative voice with `[shouts]`) | Pick a voice whose character matches the tag |
| Inconsistent emotional output | Insufficient surrounding text | Pad the line with more context, regenerate |
| Phonetic word still mispronounced | Voice has a strong accent already biasing | Try another voice, or add more letter spacing: "B-E-N-S-O-N" |
| Sound effect too subtle | Effect at start fades into voice | Combine with a delivery tag: `[gunshot][shouts]` |
| Tags work some times, not others | v3 alpha inconsistency | Generate 2 to 3 versions, pick the best take |
| Generated audio cuts off mid-word | Output not padded | Add a tail-pad of 0.08s before silence trim |
| Audio in left ear only | ElevenLabs outputs mono | Apply `aformat=channel_layouts=stereo` in ffmpeg post-processing |
| Long pauses between paragraphs | Trailing ElevenLabs silence + raw ellipsis in source | Strip `...` to space in sanitizeForVO; apply areverse+silenceremove+areverse filter chain |
| Chipmunk / sped-up voice | atempo too high | Drop atempo to 1.0; some voices need no speedup at all |
| TM / R / C symbols spoken aloud | Unicode symbols not stripped | Run sanitizeForVO before API call; strips ™ ® © automatically |
| Uptalk (rising pitch) on short fragments | Sentence too short | Merge fragments into a single comma-joined sentence |
| Voice sounds flat / narrator-like | Stability too high | Drop stability to 0.30-0.45, raise style to 0.40-0.50 |
| Voice sounds wobbly / unstable | Stability too low | Raise stability toward 0.50 |

---

## Worked example

### VSL TEXT (on screen)
> With BNSN and SLIDR combined you'll get a fantastic VSL.

### VO PHONETIC (HeyGen)
> With Benson and Slider combined you'll get a fantastic V-S-L.

### VO TAGGED (ElevenLabs v3)
> `[excited]`With Benson and Slider combined you'll get `[stress on next word]`a `[emphasized]`fantastic V-S-L.

Notice:
- "BNSN" becomes "Benson" (phonetic for both VO scripts)
- "VSL" becomes "V-S-L" (letter-by-letter; phonetic for both VO scripts)
- Tags only appear in the v3 version

---

## Workflow summary

1. **Write the VSL Text first** (on-screen, letter-perfect, no markup).
2. **Generate the VO Phonetic** (rewrite acronyms, brand names, numbers, foreign words).
3. **Mark up the VO Tagged version** (audio tags for v3, OR `[pause]` markers + CAPS for v2).
4. **Run sanitizeForVO** on the final string before sending.
5. **Convert `[pause]` markers to SSML `<break>`** if you're on v2 / Flash / English v1.
6. **Render continuously** (one full call, not per-paragraph).
7. **Apply FFmpeg filters** (mono-to-stereo + trailing silence trim).
8. **Test atempo** at 1.0 first. Only add 1.05-1.08 if the voice genuinely lags.
9. **Output one MP3** to a known location.

Hand back one file. No per-beat MP3s. No raw unprocessed takes.

---

## Sources

Compiled from official docs plus community guides and one open-source plugin.

- [Prompting Eleven v3 (alpha) - ElevenLabs official](https://elevenlabs.io/docs/best-practices/prompting/eleven-v3)
- [How do audio tags work with Eleven v3? - ElevenLabs help](https://help.elevenlabs.io/hc/en-us/articles/35869142561297-How-do-audio-tags-work-with-Eleven-v3)
- [On Text Markup For the ElevenLabs v3 - Victor Kh., Medium](https://medium.com/@v-jur-kh/on-text-markup-for-the-elevenlabs-v3-text-to-speech-2b0a330110e1)
- [ElevenLabs Eleven v3 Alpha - Complete Guide to Audio Tags (audio-generation-plugin.com)](https://audio-generation-plugin.com/elevenlabs-v3/)
- [Ultimate ElevenLabs Tutorial (testified.ai)](https://testified.ai/tutorials/ultimate-guide-master-elevenlabs-text-to-speech)
- [ElevenLabs v3 Audio Tags User Guide (Jonathan Mast)](https://jonathanmast.com/elevenlabs-v3-audio-tags-user-guide-mastering-emotional-voice-control/)
- [opencode-voice plugin (GitHub - anomalyco)](https://github.com/anomalyco/opencode-voice)
- [SSML phoneme tags compatibility - ElevenLabs help](https://help.elevenlabs.io/hc/en-us/articles/24352686926609-Do-pauses-and-SSML-phoneme-tags-work-with-the-API)
- [Pronunciation forcing - ElevenLabs help](https://help.elevenlabs.io/hc/en-us/articles/16712320194577-How-can-I-force-a-certain-pronunciation-of-a-word-or-name)

---

## Want every skill like this one? Plus live coaching?

This is one skill. Jon ships custom skills like this one every single month, plus live coaching calls, plus the one-click setup for the entire AI stack we actually use, plus full access to the AI Collective.

One URL gets you everything: **[collective.bnsn.ai](https://collective.bnsn.ai)**

What's inside:
- Every custom skill Jon builds, this one plus dozens more, dropped monthly
- Live coaching every single month
- One-click setup for the AI stack running on our own machines
- Step-by-step tutorial videos, kept current as tools evolve
- Daily TLDR briefings on every AI development that matters
- Direct line to Jon inside the community

If this skill saved you an hour, what's behind that one link will save you a hundred.

---

## Update this skill when

- ElevenLabs ships new model versions (v4, v3 GA)
- New audio tags get discovered through user testing
- HeyGen adds tag support (would change the strip-tags-for-HeyGen rule)
- Your specific voice profile shifts (re-tune stability/style)
