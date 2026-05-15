#!/usr/bin/env python3
"""ElevenLabs voiceover template — generate, atempo-fit to video, mux.

Copy to your project. Edit VOICE_ID, NARRATION, SRC_VIDEO at the top. Then:

    python3 voiceover.py

API key is read from macOS Keychain entry 'elevenlabs-api'. The key never
appears in this file, in environment variables, or in command-line arguments.
Set it once with:
    security add-generic-password -s "elevenlabs-api" -a "$USER" -w
"""
from __future__ import annotations
import json, os, pathlib, subprocess, sys, urllib.error, urllib.request

# ─── EDIT THESE FOR YOUR PROJECT ───────────────────────────────────────────
VOICE_ID  = "JBkETLRMd2up1dGzeche"   # `python3 list_voices.py` to find one
MODEL_ID  = "eleven_multilingual_v2"
SRC_VIDEO = pathlib.Path(__file__).resolve().parent / "walkthrough.mp4"
OUT_VIDEO = pathlib.Path(__file__).resolve().parent / "walkthrough-narrated.mp4"

NARRATION = (
    "Replace this with your narration. One continuous block, no SSML, "
    "no stage directions. ElevenLabs' natural prosody handles sentence "
    "pauses from punctuation. Aim for roughly 2.5 words per second of "
    "target video — atempo will compress slight overshoot."
)

VOICE_SETTINGS = {
    "stability":         0.55,   # 0.5–0.6 = narration sweet spot
    "similarity_boost":  0.75,
    "style":             0.0,    # 0 = clean read; bump 0.2 for warmth
    "use_speaker_boost": True,
}

# ─── machinery ─────────────────────────────────────────────────────────────
OUT_DIR    = pathlib.Path(__file__).resolve().parent
TTS_DIR    = OUT_DIR / "tts"
RAW_MP3    = TTS_DIR / "narration.mp3"
FITTED_M4A = TTS_DIR / "narration-fitted.m4a"

TARGET_DURATION: float | None = None  # None = auto from SRC_VIDEO
ATEMPO_TOLERANCE_MS = 200
KEYCHAIN_NAME = "elevenlabs-api"

def die(msg):
    print(f"\n✗ {msg}", file=sys.stderr); sys.exit(1)

def get_key():
    account = os.environ.get("USER") or subprocess.check_output(["whoami"]).decode().strip()
    try:
        return subprocess.check_output(
            ["security", "find-generic-password",
             "-s", KEYCHAIN_NAME, "-a", account, "-w"],
            stderr=subprocess.STDOUT,
        ).decode().strip()
    except subprocess.CalledProcessError as e:
        die(f"Keychain entry '{KEYCHAIN_NAME}' not found: {e.output.decode().strip()}\n"
            f"  Create it:  security add-generic-password -s \"{KEYCHAIN_NAME}\" -a \"$USER\" -w")

def have(cmd): return subprocess.run(["which", cmd], capture_output=True).returncode == 0

def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", str(path),
    ])
    return float(out.strip())

def tts(text, key, out_path):
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=body,
        headers={"xi-api-key": key,
                 "Content-Type": "application/json",
                 "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            out_path.write_bytes(r.read())
    except urllib.error.HTTPError as e:
        die(f"ElevenLabs HTTP {e.code}: {e.read().decode()[:400]}")
    except urllib.error.URLError as e:
        die(f"Couldn't reach api.elevenlabs.io: {e.reason}")

def fit_audio_to(target, src, dst):
    src_dur = probe_duration(src)
    if abs(src_dur - target) * 1000 < ATEMPO_TOLERANCE_MS:
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src), "-c:a", "aac", "-b:a", "192k", str(dst),
        ], check=True)
        return 1.0, src_dur
    atempo = src_dur / target
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-filter:a", f"atempo={atempo:.4f}",
        "-c:a", "aac", "-b:a", "192k",
        str(dst),
    ], check=True)
    return atempo, probe_duration(dst)

def main():
    if not SRC_VIDEO.exists():
        die(f"Source video not found: {SRC_VIDEO}")
    if not have("ffmpeg") or not have("ffprobe"):
        die("ffmpeg/ffprobe not on PATH. Run setup.sh first.")
    TTS_DIR.mkdir(exist_ok=True)
    target = TARGET_DURATION if TARGET_DURATION is not None else probe_duration(SRC_VIDEO)
    print(f"Target audio duration: {target:.2f} s  (matches {SRC_VIDEO.name})")

    if RAW_MP3.exists() and RAW_MP3.stat().st_size > 0:
        print(f"▸ Using cached narration  ({RAW_MP3.stat().st_size//1024} KB)")
    else:
        print("▸ Requesting narration from ElevenLabs …")
        tts(NARRATION, get_key(), RAW_MP3)
        print(f"  done  ({RAW_MP3.stat().st_size//1024} KB)")
    raw_dur = probe_duration(RAW_MP3)
    print(f"  raw duration: {raw_dur:.2f} s")

    print(f"▸ Fitting to {target:.2f} s …")
    atempo, fitted_dur = fit_audio_to(target, RAW_MP3, FITTED_M4A)
    print(f"  atempo = {atempo:.4f}   fitted = {fitted_dur:.2f} s")
    if abs(atempo - 1.0) > 0.15:
        print("  ⚠ atempo outside ±15% — voice may sound rushed/slowed.")
        print(f"    Consider editing NARRATION to be ~{int(raw_dur/target * len(NARRATION.split()))} words.")

    print(f"▸ Muxing onto {SRC_VIDEO.name} …")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(SRC_VIDEO), "-i", str(FITTED_M4A),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(OUT_VIDEO),
    ], check=True)

    final_dur = probe_duration(OUT_VIDEO)
    print(f"\n✓ {OUT_VIDEO.name}  ({OUT_VIDEO.stat().st_size//1024} KB, {final_dur:.2f} s)")
    chars = len(NARRATION)
    print(f"  Approx ElevenLabs usage: {chars} chars (~${chars/1000*0.30:.2f} on the creator plan)")
    print(f"  To regenerate after editing NARRATION:  rm {RAW_MP3.name} && python3 {pathlib.Path(__file__).name}")

if __name__ == "__main__":
    main()
