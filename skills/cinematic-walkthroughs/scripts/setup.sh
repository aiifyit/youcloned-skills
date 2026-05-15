#!/usr/bin/env bash
# cinematic-walkthroughs — environment setup
# Installs FFmpeg, ImageMagick, Python deps; verifies fonts.
# macOS + Linux. Re-runnable; skips anything already installed.

set -euo pipefail

BOLD=$'\033[1m'; GRN=$'\033[32m'; YLW=$'\033[33m'; RED=$'\033[31m'; DIM=$'\033[2m'; RST=$'\033[0m'
say()  { printf "%s==> %s%s\n" "${BOLD}" "$*" "${RST}"; }
ok()   { printf " %s✓%s %s\n" "${GRN}" "${RST}" "$*"; }
warn() { printf " %s!%s %s\n" "${YLW}" "${RST}" "$*"; }
die()  { printf " %s✗%s %s\n" "${RED}" "${RST}" "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# ── platform detection
case "$(uname -s)" in
  Darwin)
    PLATFORM=mac
    have brew || die "Homebrew not found. Install from https://brew.sh first."
    PKG_INSTALL() { brew install "$@"; }
    ;;
  Linux)
    PLATFORM=linux
    if have apt-get; then PKG_INSTALL() { sudo apt-get install -y "$@"; }
    elif have dnf; then PKG_INSTALL() { sudo dnf install -y "$@"; }
    else die "No supported package manager (need apt or dnf)."
    fi
    ;;
  *) die "Unsupported OS: $(uname -s)" ;;
esac
ok "Platform: ${PLATFORM}"

# ── ffmpeg
say "FFmpeg"
if have ffmpeg; then
  ok "Already installed: $(ffmpeg -version | head -1 | awk '{print $1,$2,$3}')"
else
  PKG_INSTALL ffmpeg
  ok "Installed $(ffmpeg -version | head -1 | awk '{print $1,$2,$3}')"
fi

# ── imagemagick
say "ImageMagick"
if have magick || have convert; then
  ok "Already installed: $({ magick -version 2>/dev/null || convert -version; } | head -1 | awk '{print $1,$2,$3}')"
else
  PKG_INSTALL imagemagick
  ok "Installed"
fi

# ── python3
say "Python 3"
if have python3; then
  major=$(python3 -c 'import sys; print(sys.version_info[0])')
  minor=$(python3 -c 'import sys; print(sys.version_info[1])')
  if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
    ok "Python $(python3 --version | awk '{print $2}') ✓"
  else
    warn "Python ${major}.${minor} is older than 3.10. Some PIL features may behave differently."
  fi
else
  PKG_INSTALL python3 python3-pip
fi

# ── pillow + numpy
say "Pillow + NumPy"
if python3 -c "import PIL, numpy; assert PIL.__version__.split('.')[0] >= '10'" 2>/dev/null; then
  ok "PIL $(python3 -c 'import PIL; print(PIL.__version__)') · NumPy $(python3 -c 'import numpy; print(numpy.__version__)')"
else
  pip3 install --break-system-packages 'Pillow>=11.0' 'numpy>=1.24' >/dev/null 2>&1 \
    || pip3 install 'Pillow>=11.0' 'numpy>=1.24' >/dev/null 2>&1 \
    || die "pip3 install failed. Run 'pip3 install Pillow numpy' manually."
  ok "Installed Pillow $(python3 -c 'import PIL; print(PIL.__version__)') · NumPy $(python3 -c 'import numpy; print(numpy.__version__)')"
fi

# ── fonts
say "Fonts"
font_root_mac=/Library/Fonts
font_root_user=$HOME/Library/Fonts
font_root_linux=/usr/share/fonts/truetype

found_count=0
missing=()
for f in "Poppins-Bold.ttf" "Poppins-Regular.ttf" "DejaVuSans-Bold.ttf" "LiberationMono-Bold.ttf"; do
  if find "$font_root_mac" "$font_root_user" "$font_root_linux" -name "$f" 2>/dev/null | grep -q .; then
    found_count=$((found_count+1))
  else
    missing+=("$f")
  fi
done
if [ ${#missing[@]} -eq 0 ]; then
  ok "All 4 reference fonts found"
else
  warn "Missing fonts: ${missing[*]}"
  if [ "$PLATFORM" = "mac" ]; then
    echo "    Install Google Poppins:"
    echo "      brew install --cask font-poppins font-dejavu font-liberation"
  else
    echo "    Install:  sudo apt-get install fonts-poppins fonts-dejavu fonts-liberation"
  fi
  warn "Render will fall back to system defaults if these are missing — output will look less polished."
fi

# ── voiceover (optional) — Keychain key on macOS
if [ "$PLATFORM" = "mac" ]; then
  say "ElevenLabs key (optional, for voiceover)"
  if security find-generic-password -s "elevenlabs-api" -a "$USER" >/dev/null 2>&1; then
    ok "Keychain entry 'elevenlabs-api' already exists"
  else
    warn "No ElevenLabs key in Keychain yet. To enable voiceovers later, run:"
    echo "      security add-generic-password -s \"elevenlabs-api\" -a \"\$USER\" -w"
    echo "    (You'll get a secure prompt — paste the API key, not your password.)"
  fi
fi

# ── summary
printf "\n%s%sSetup complete.%s\n" "${BOLD}" "${GRN}" "${RST}"
cat <<EOF

Next steps:
  1. Copy a renderer:  cp $(dirname "$0")/../templates/render_reference.py ./render_<topic>.py
  2. Edit scenes + captions for your topic.
  3. Render:           python3 render_<topic>.py all
  4. Stitch (the renderer prints the command to run).
  5. (Optional) Voiceover:  copy templates/voiceover.py, set NARRATION + SRC_VIDEO, run.

Read SKILL.md for the full pipeline and visual technique catalog.
EOF
