---
name: cinematic-walkthroughs
description: Render high-polish animated walkthrough videos (intro videos, install guides, tutorial walkthroughs, explainer videos, website tours) using Python + PIL + FFmpeg, with optional ElevenLabs voiceover. Use when the user asks for a "walkthrough video," "intro video," "explainer," "demo video," "animated tutorial," or anything where the deliverable is a short polished MP4 that pairs animated visuals with optional narration. Produces the cinematic style (particle backgrounds, perspective grids, glowed kinetic typography, custom illustrated icons, animated terminals, oscilloscope waveforms, baked captions, crossfade transitions) — not flat text-on-background slide videos.
---

# Cinematic walkthroughs

A renderer architecture and technique catalog for producing the kind of animated walkthrough videos that look like Anthropic / Linear / Vercel intro videos — calm, dark-themed, kinetic typography, custom illustrations — rather than corporate clipart or flat slide cards.

This skill ships with a working reference renderer plus an ElevenLabs voiceover pipeline. Read the architecture section, then copy `templates/render_reference.py` and edit the scenes for the topic at hand. Don't rebuild from scratch each time — the visual primitives (particle field, perspective grid, glowed text, kinetic title, terminal mock, oscilloscope, icon library) are the slow part to get right.

## What "good" looks like in this style

When the user wants an intro or walkthrough video, they almost always want this:

- 1280×720 H.264 MP4, 30 fps, 30–90 seconds
- Dark navy background (`#08081A` ish) with a soft drifting purple radial glow
- Parallax particle field — ~200 dots at varying depths drifting independently
- Faint perspective grid floor receding to a vanishing point
- Bold display title that flies in letter-by-letter with overshoot, lit by a soft glow halo
- Subtitle that types in character-by-character with a blinking cursor
- Multi-card layouts where cards rise from below with elastic ease, staggered
- Custom illustrated icons (filmstrip, waveform, browser window, design canvas, image stack — whatever the topic needs), not text labels
- Animated terminal mock with traffic lights + typewriter commands + scrolling install log + animated oscilloscope + progress bar
- Bottom caption strip with semi-transparent backdrop, baked from the narration timing
- 0.4-second crossfade transitions between scenes (xfade filter)
- Optional ElevenLabs voiceover muxed via atempo-fit so the audio lands on the video duration exactly

When the user asks for an explainer video, this is the floor — not the ceiling.

## What this skill does NOT produce

Reject these defaults if asked for a walkthrough:

- **Flat text-on-background slides.** FFmpeg `drawtext` with timed alpha looks like a 2010 PowerPoint export. Always layer on at least the background-particle-and-glow stack from `bg_layer()` in the reference renderer.
- **Stock corporate clipart icons.** If a tool/concept needs an icon, draw it from PIL primitives (see the icon library in the reference renderer — filmstrip, image stack, browser, waveform, design canvas).
- **Bright white backgrounds.** This style is dark navy. White-bg variants exist (the IRS walkthrough does this for an authentic government-site feel) but they require the page itself to be the visual focus, not floating elements.
- **TikTok / vertical / 9:16.** Default is 16:9 1280×720. If the user explicitly asks for vertical, change `W, H = 720, 1280` and re-layout scenes.

## Setup (one-time per machine)

```bash
bash scripts/setup.sh
```

Installs:
- FFmpeg (via Homebrew on macOS, apt on Linux)
- ImageMagick (for thumbnails and storyboard contact sheets)
- Python 3 with Pillow ≥ 11 and NumPy ≥ 2 (via `pip install --break-system-packages`)
- Verifies Poppins, Liberation Mono, and DejaVu Sans fonts are reachable

For voiceover support, also store the ElevenLabs API key in macOS Keychain (one command, one secure prompt — never paste the key into source files):

```bash
security add-generic-password -s "elevenlabs-api" -a "$USER" -w
```

If it already exists and you need to overwrite (e.g. you fat-fingered your password into the prompt — yes, that happens), add `-U`.

Then list available voices to pick one:

```bash
python3 scripts/list_voices.py
```

Copy the `voice_id` of whichever voice fits the project's tone — narration-friendly male voices with use-case "narration" or "conversational" work well for tutorials; a calm female voice is good for product intros.

## Architecture

Per-scene PIL frame renderers → ffmpeg encode → xfade-stitch. One Python file, one ffmpeg command, one optional voiceover.

```
narration text  →  ElevenLabs API  →  raw.mp3
                                          ↓ ffprobe duration
scene_1(t) ──► frames/s01/*.png  →  s01.mp4 ─┐
scene_2(t) ──► frames/s02/*.png  →  s02.mp4 ─┤  xfade stitch  ─►  video.mp4
   ...                                       │                          │
scene_N(t) ──► frames/sNN/*.png  →  sNN.mp4 ─┘                          │ ffmpeg
                                                                        │  mux
                                                                       fitted.m4a  ◄── atempo fit
                                                                        │
                                                                        ▼
                                                               narrated.mp4
```

### Scene functions

Every scene is a function `scene_N(t, dur, scene_offset)` that returns a `PIL.Image`. `t` is local time within the scene (0..dur), `dur` is the scene's duration in seconds, `scene_offset` is when the scene starts in the GLOBAL timeline after xfade overlap absorption. Pass `scene_offset + t` to `finalize()` so the caption strip can look up the right phrase.

```python
def scene_2(t, dur=12.0, scene_offset=4.6):
    base = bg_layer(t, grid=True, particles=True)
    base.alpha_composite(kinetic_title(t, "Five tools, one stack", ...))
    # ... draw cards, icons, etc.
    return finalize(base, scene_offset + t)
```

### Timing the xfade offsets

With 0.4-second crossfades, each scene's *effective* on-screen window starts `0.4s` later in the cut than the simple cumulative duration would suggest. For scene durations `[5, 12, 8, 14, 10, 10, 10, 8]`:

| Scene | Source duration | scene_offset (start in final cut) |
|-------|-----------------|-----------------------------------|
| 1     | 5               | 0.0                               |
| 2     | 12              | 4.6                               |
| 3     | 8               | 16.2                              |
| 4     | 14              | 23.8                              |
| 5     | 10              | 37.4                              |
| 6     | 10              | 47.0                              |
| 7     | 10              | 56.6                              |
| 8     | 8               | 66.2                              |

Final video duration = `sum(durations) - 0.4 * (N - 1)`. For the example above: `77 - 2.8 = 74.2s`.

The ffmpeg xfade offsets follow the same pattern — see the stitching one-liner at the end of `templates/render_reference.py`.

## Visual building blocks (copy as needed)

All of these are implemented in `templates/render_reference.py`. Read that file for the exact signatures.

### Background stack — `bg_layer(t, grid=True, particles=True)`

Returns a 1280×720 RGBA with: solid navy + soft drifting radial glow + optional perspective grid + optional particle field. Apply at the start of every scene before drawing content.

### Particle field — `particle_field(t)`

220 pre-seeded dots with z-depth (0.2..1.0). Depth controls speed (parallax), size, and alpha. Closer dots are larger and brighter. Cheap to render.

### Perspective grid — `perspective_grid(t)`

Tron-style floor receding to a vanishing point at `H * 0.55`. Subtle horizontal pan via `sin(t * 0.2)`. Set `alpha=0.35` for the full-strength version, lower for less assertive scenes.

### Glowed text — `render_text_glow(text, fnt, color, glow_color, glow_radius, glow_strength)`

Returns a tight RGBA sprite of the text with a soft glow halo behind sharp foreground text. **Critical**: render the glow into its own RGBA layer first, blur it, scale its alpha, THEN composite sharp text on top — NOT the other way around. The mistake of drawing main text into the same buffer before compositing glow makes the title look like uniform fuzz instead of sharp-text-with-halo.

### Kinetic title — `kinetic_title(t, text, base_y, fnt, color, glow_color, ...)`

Each letter eases in from below with a slight overshoot rotation and a scale 0.4→1.0. Letters can be staggered (`char_delay=0.05`) for a typewriter-like reveal that also has motion. Use `fade_out_at=dur-0.5` to fade the title out near the end of the scene.

### Caption strip — `draw_caption(global_t)`

Looks up the current `CAPTIONS` entry and draws a semi-transparent rounded-rect at the bottom of the canvas with the narration phrase. Times are GLOBAL (in final-cut timeline, not per-scene). Always call this from `finalize()` so every scene picks up the same captions.

### Terminal mock — `draw_terminal_window(layer, x, y, w, h, title, alpha)`

Rounded rect with header bar, traffic lights, title text. Pair with `scanline_strip(w, h, alpha)` overlaid on top of the terminal body for CRT vibes. The renderer also has typewriter logic — every 0.025s reveals one more character of the command string, with a blinking caret while typing.

### Oscilloscope — `oscilloscope(x, y, w, h, t, alpha, amplitude)`

Multi-sine waveform with a soft glow under-layer. Use it inside a terminal mock to suggest "audio is happening" or "install is running" — anywhere you want motion in an otherwise static block.

### Neon line — `neon_line(size, p1, p2, color, width, glow_radius)`

Glowing line. Use for arrows between cards (step 1 → step 2 → step 3), underlines under titles, accent strokes.

### Icon library

`render_reference.py` includes 5 PIL-drawn illustrations you'll reach for over and over:

- `icon_filmstrip(w, h, t, color, alpha)` — vertical filmstrip with sprocket holes scrolling, frame slots inside, play arrow center. Use for "video" / "render" concepts.
- `icon_image_stack(w, h, t, color, alpha)` — three stacked image cards, top one with a tiny mountain-and-sun composition. Use for "images" / "photos" concepts.
- `icon_browser(w, h, t, color, alpha)` — rounded browser window with traffic lights, URL bar, content lines, animated cursor doing a small loop with periodic click pulse. Use for "web" / "browser" / "automation" concepts.
- `icon_waveform(w, h, t, color, alpha)` — 18-bar animated equalizer with twin-sine envelope and a glowing carrier line. Use for "audio" / "transcribe" / "podcast" concepts.
- `icon_design_canvas(w, h, t, color, alpha)` — design canvas with header bar, three text rows that pulse subtly, button, drifting sparkle. Use for "design" / "prototype" concepts.

Need a new icon? Same approach: draw with PIL primitives (rounded_rectangle, line, ellipse, polygon), include a subtle time-driven animation (`sin(t)` somewhere), accept `alpha` and `color` parameters.

### Card / hero patterns

- **Stagger-bounce cards** — five tool cards on `Scene 2` in the reference: each card has `delay = base + i * 0.18`, eases in with `ease_out_elastic`, lands from below. The card body is on its own RGBA layer composited onto the base. **Important**: if you have text or sprites that need to land ON TOP of the card body (numbers, icons), composite the card body first, THEN paste the foreground sprites — otherwise the card fill covers them. This was a real bug we hit.
- **Big-number capability cards** — `Scene 7` in the reference. Cards zoom from 60% → 100% with a soft bob loop after settling.

### Effect: particle burst

For URL reveals, "you're done" moments, scene-8 outros. 36 particles radiating outward from a point in alternating accent colors, fading over ~1.6 seconds. See the scene 8 implementation.

## Pipeline (the lazy man's path)

1. Copy `templates/render_reference.py` to your project, rename to `render_<topic>.py`.
2. Edit `SCENES = {...}` to set scene functions, durations, and offsets.
3. Edit the narration in your script doc.
4. Edit `CAPTIONS` to match — each entry is `(start_t, end_t, text)` in GLOBAL timeline.
5. Render: `python3 render_<topic>.py all`
6. Encode each scene and stitch (the renderer prints the exact ffmpeg commands you need; or use the `stitch.sh` template).
7. Voiceover (optional): adapt `templates/voiceover.py` — update `VOICE_ID`, `NARRATION`, `SRC_VIDEO`, run.
8. Mux: `voiceover.py` does this automatically as its last step.

Render time on a modern Mac: ~4–8 seconds per scene at 720p/30fps depending on per-frame complexity. Total typically under 5 minutes for an 80-second video.

## Voiceover via ElevenLabs

The voiceover pipeline runs on the user's machine, not in a sandbox — the API key lives in macOS Keychain and must not appear in source files or chat.

### Flow

1. Read API key from Keychain (`security find-generic-password -s elevenlabs-api -a "$USER" -w`).
2. POST the narration text to `https://api.elevenlabs.io/v1/text-to-speech/<voice_id>` with `model_id: eleven_multilingual_v2`.
3. Save MP3 to a cache directory.
4. `ffprobe` the raw audio duration.
5. Compute `atempo = raw_dur / target_video_dur` and apply via `ffmpeg -filter:a "atempo=<value>"` to compress/stretch.
6. Mux audio onto video with `-c:v copy` (no video re-encode).

### Why atempo

ElevenLabs voices come back at unpredictable lengths — same script can be 68s in one voice and 82s in another. Atempo within `0.92..1.10` is imperceptible. Outside `±15%` the voice starts to sound rushed/slowed; if you hit that, edit the narration to fit instead of cranking atempo. The reference voiceover prints a warning when atempo lands outside the comfortable band.

### Why one continuous narration block, not per-scene MP3s

We tried both. Per-scene generation produces sentence-level gaps that read as awkward silence; one continuous TTS call lets ElevenLabs handle prosody naturally and gives a smoother result. Cache the single MP3 and only regenerate when the script changes.

### Voice settings worth caring about

```python
VOICE_SETTINGS = {
    "stability": 0.55,         # 0.5–0.6 = narration sweet spot
    "similarity_boost": 0.75,
    "style": 0.0,              # 0 = straight read; bump to 0.2 for warmth
    "use_speaker_boost": True,
}
```

If the voice sounds flat, increase `style` to 0.2. If it sounds inconsistent across the take, raise `stability` to 0.6.

## No-Terminal execution (.app bundle)

Some users don't want to touch Terminal. Wrap the voiceover script in a minimal macOS `.app` bundle that runs invisibly with notifications. See `templates/voiceover_app_template/`.

Structure:

```
Voiceover.app/
  Contents/
    Info.plist                  # LSUIElement=true → no Dock icon, no Terminal
    MacOS/
      run                       # executable shell script
```

The shell script does:
1. `osascript display notification` — tell the user something is happening.
2. `cd ~/Documents/YourProject && python3 voiceover.py > /tmp/log 2>&1`.
3. On success: `osascript display notification` + `open <result.mp4>`.
4. On failure: `osascript display dialog` with the tail of the log.

User just double-clicks the .app in Finder. No Terminal opens.

**Gatekeeper note**: Unsigned local apps usually don't get the quarantine flag (it's set on downloaded files), but if macOS warns, the user does Right-click → Open → Open Anyway once.

## Common pitfalls (don't repeat these)

These are real bugs we hit and fixed during the original development cycle. Encoded here so the next conversation doesn't burn cycles on them.

1. **Glow text fuzz**: drawing the main text in the same buffer as the glow, then `alpha_composite`-ing onto it, makes the buffer reference dangle. Render glow and sharp text into separate RGBA layers, then composite together. (See `render_text_glow` in the reference renderer.)
2. **Empty cards**: pasting sprites (numbers, icons) onto `base` BEFORE compositing the card body layer means the card body covers them. Always: card body → composite to base → THEN paste icon/text sprites on top of base.
3. **Caption sync drift**: caption times are GLOBAL (in the final cut, after xfade absorption), not per-scene local. Pass `scene_offset + t` into `finalize()`, not just `t`.
4. **xfade timing math**: each crossfade subtracts `0.4s` from the total run length. The xfade `offset=` parameter for chain step N is `(cumulative_dur_before_step) - 0.4`, not the simple sum. Use the table in the Architecture section.
5. **Sandbox cannot reach ElevenLabs**: `api.elevenlabs.io` is on most sandbox egress denylists. The voiceover step MUST run on the user's machine, not in the renderer environment.
6. **Don't ask for the API key**: the security model is that the key lives in macOS Keychain and never appears in chat or source. If a user pastes a key, instruct them to rotate it immediately.
7. **bnsn.ai and other allowlist-blocked domains**: similar — assume any domain might be blocked from sandbox. If the renderer needs assets, ship them inline (PIL primitives) rather than fetching at runtime.

## File reference

- `scripts/setup.sh` — install FFmpeg + ImageMagick + Python deps + check fonts
- `scripts/list_voices.py` — query ElevenLabs `/v1/voices` and print a table; key comes from Keychain
- `templates/render_reference.py` — the full renderer with all visual building blocks and 8 example scenes — copy and edit per project
- `templates/voiceover.py` — ElevenLabs + atempo fit + mux pipeline; edit `VOICE_ID`, `NARRATION`, `SRC_VIDEO` per project
- `templates/voiceover_app_template/` — minimal .app bundle wrapping voiceover.py for one-double-click execution

## When the user asks for "a quick video" instead

If the request really is "just throw a 5-second test card up," do a single FFmpeg command instead of this whole pipeline. This skill is for deliverables ≥30 seconds where polish matters. Don't over-engineer a 5-second sanity check.
