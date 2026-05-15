"""Cinematic walkthrough renderer — reference template.

Copy this file to your project, rename to render_<topic>.py, and edit the
SCENES at the bottom (durations, offsets) and each scene's content for the
topic you're walking through.

Visual building blocks (see SKILL.md for a full catalog):
  • bg_layer()                — particles + perspective grid + drifting glow
  • kinetic_title()           — letter-by-letter animated title with glow
  • render_text_glow()        — sharp text on a blurred glow halo (correct order!)
  • icon_filmstrip / image_stack / browser / waveform / design_canvas
  • draw_terminal_window() + scanline_strip() + oscilloscope()
  • neon_line()               — glowing accent lines / arrows
  • draw_caption()            — bottom narration strip (timed in GLOBAL t)
  • finalize()                — vignette + caption — call last in every scene

Run:  python3 render_reference.py <scene_number|all>
Then encode + stitch (see the bottom of the file for the ffmpeg commands).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import math, os, sys, random

# ─── canvas ────────────────────────────────────────────────────────────────
W, H = 1280, 720
FPS = 30

# Palette — dark cinematic
BG          = (8, 8, 18)
BG_2        = (24, 22, 44)
ACCENT      = (138, 127, 255)   # purple
ACCENT_2    = (96, 220, 255)    # cyan
ACCENT_3    = (255, 110, 200)   # pink
WHITE       = (255, 255, 255)
DIM         = (176, 176, 192)
GREEN       = (90, 230, 150)
YELLOW      = (255, 200, 90)
TERMINAL_BG = (14, 14, 24)

FONTS_DIR = "/usr/share/fonts/truetype"   # adjust on macOS if needed
def font(name, size):
    paths = {
        "bold":     f"{FONTS_DIR}/google-fonts/Poppins-Bold.ttf",
        "medium":   f"{FONTS_DIR}/google-fonts/Poppins-Medium.ttf",
        "regular":  f"{FONTS_DIR}/google-fonts/Poppins-Regular.ttf",
        "light":   f"{FONTS_DIR}/google-fonts/Poppins-Light.ttf",
        "mono":    f"{FONTS_DIR}/liberation/LiberationMono-Bold.ttf",
        "mono-r":  f"{FONTS_DIR}/liberation/LiberationMono-Regular.ttf",
        "serif-b": f"{FONTS_DIR}/dejavu/DejaVuSerif-Bold.ttf",
        "sans-b":  f"{FONTS_DIR}/dejavu/DejaVuSans-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)

# ─── easing ────────────────────────────────────────────────────────────────
def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    return 4*t*t*t if t < 0.5 else 1 - (-2*t + 2) ** 3 / 2
def ease_out_back(t, s=1.70158):
    u = t - 1
    return u*u*((s+1)*u + s) + 1
def ease_out_elastic(t):
    if t == 0 or t == 1: return t
    c4 = (2*math.pi) / 3
    return 2**(-10*t) * math.sin((t*10 - 0.75)*c4) + 1
def clamp01(x): return max(0.0, min(1.0, x))

# ─── utils ─────────────────────────────────────────────────────────────────
def text_size(text, fnt):
    tmp = Image.new("RGBA", (1, 1))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def with_alpha(rgb, a):
    return (rgb[0], rgb[1], rgb[2], int(max(0, min(255, a*255))))

def _alpha_mul(im, a):
    if a >= 1.0: return im
    arr = np.array(im).astype(np.int16)
    arr[..., 3] = (arr[..., 3] * a).astype(np.int16)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def paste_with_alpha(base, sprite, x, y, alpha=1.0):
    if alpha <= 0: return base
    if alpha < 1.0:
        sprite = _alpha_mul(sprite, alpha)
    base.alpha_composite(sprite, (int(x), int(y)))
    return base

# ─── particle field (parallax background dots) ─────────────────────────────
random.seed(42)
NUM_PARTICLES = 220
PARTICLES = [{"x": random.uniform(0, W), "y": random.uniform(0, H),
              "z": random.uniform(0.2, 1.0), "speed": random.uniform(8, 22),
              "phase": random.uniform(0, math.tau)} for _ in range(NUM_PARTICLES)]

def particle_field(t, drift=8.0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for p in PARTICLES:
        offset = (p["speed"] * p["z"] * t) % (W + 100)
        x = (p["x"] + offset + drift * math.sin(t * 0.3 + p["phase"]) * p["z"]) % (W + 40) - 20
        y = (p["y"] + drift * 0.4 * math.cos(t * 0.25 + p["phase"]) * p["z"]) % H
        r = 0.5 + 2.4 * p["z"]
        a = int(40 + 180 * (p["z"] ** 1.5))
        c = ACCENT if p["z"] > 0.6 else ACCENT_2
        d.ellipse([x-r, y-r, x+r, y+r], fill=(*c, a))
    return layer

def perspective_grid(t, alpha=0.55):
    """Tron-style grid floor receding to vanishing point."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    horizon = H * 0.55
    vp_x = W * 0.5
    pan = math.sin(t * 0.2) * 30
    for i in range(1, 16):
        y = horizon + (H - horizon) * (i / 15) ** 1.6
        a = int(alpha * 255 * (1 - i/16))
        d.line([(0, y), (W, y)], fill=(*ACCENT, max(8, a // 3)), width=1)
    n = 19
    for i in range(n):
        x_bot = (i / (n - 1)) * (W * 1.6) - W * 0.3 + pan
        a = int(alpha * 255 * 0.6)
        d.line([(vp_x, horizon), (x_bot, H)], fill=(*ACCENT, max(8, a // 3)), width=1)
    return layer

def bg_layer(t, grid=True, particles=True):
    """Composite background — solid + drifting glow + (optional) grid + particles."""
    img = Image.new("RGBA", (W, H), (*BG, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx = W * 0.5 + math.sin(t * 0.5) * 280
    cy = H * 0.5 + math.cos(t * 0.35) * 120
    for r, a in [(520, 18), (380, 30), (260, 42), (160, 60)]:
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*ACCENT, a))
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    img = Image.alpha_composite(img, glow)
    if grid:
        img = Image.alpha_composite(img, perspective_grid(t, alpha=0.35))
    if particles:
        img = Image.alpha_composite(img, particle_field(t))
    return img

# ─── vignette + caption finalizer ──────────────────────────────────────────
_VIGNETTE_CACHE = None
def vignette_overlay(strength=0.55):
    global _VIGNETTE_CACHE
    if _VIGNETTE_CACHE is not None: return _VIGNETTE_CACHE
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W/2, H/2
    d = np.sqrt((x-cx)**2 + (y-cy)**2)
    maxd = math.sqrt(cx**2 + cy**2)
    v = np.clip((d / maxd) ** 2.4, 0, 1) * 255 * strength
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[..., 3] = v.astype(np.uint8)
    _VIGNETTE_CACHE = Image.fromarray(arr)
    return _VIGNETTE_CACHE

# Caption schedule — edit this for your project. Times are GLOBAL (final cut).
CAPTIONS = [
    (0.3,  3.8,  "Welcome — this is your cinematic walkthrough."),
    (4.0,  8.0,  "Each scene is a Python function returning a PIL image."),
    (8.0, 12.0,  "Effects: particles · perspective grid · glow · kinetic type."),
    (12.0, 16.0, "Replace these captions for your actual project."),
]
CAPTION_FADE = 0.18

def get_active_caption(global_t):
    for start, end, text in CAPTIONS:
        if start - CAPTION_FADE <= global_t <= end + CAPTION_FADE:
            if global_t < start:    a = (global_t - (start - CAPTION_FADE)) / CAPTION_FADE
            elif global_t > end:    a = (end + CAPTION_FADE - global_t) / CAPTION_FADE
            else:                   a = 1.0
            return text, clamp01(a)
    return None, 0

def draw_caption(global_t):
    text, alpha = get_active_caption(global_t)
    if not text or alpha <= 0: return None
    layer = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    fnt = font("medium", 22)
    tw, th = text_size(text, fnt)
    pad_x, pad_y = 28, 12
    box_w = tw + pad_x*2
    box_h = th + pad_y*2 + 4
    bx = (W - box_w) // 2
    by = H - box_h - 24
    backdrop = Image.new("RGBA", (box_w+40, box_h+40), (0,0,0,0))
    bd = ImageDraw.Draw(backdrop)
    bd.rounded_rectangle([20, 20, 20+box_w, 20+box_h], radius=12, fill=(0,0,0,140))
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(8))
    layer.alpha_composite(backdrop, (bx-20, by-20))
    d.rounded_rectangle([bx, by, bx+box_w, by+box_h], radius=12,
                        fill=(0, 0, 0, 170), outline=(*ACCENT, 100), width=1)
    d.text((bx + pad_x, by + pad_y - 2), text, font=fnt, fill=(*WHITE, 255))
    return _alpha_mul(layer, alpha)

def finalize(img, global_t):
    """Always call this at the end of a scene. Adds vignette + caption."""
    if img.mode != "RGBA": img = img.convert("RGBA")
    img = Image.alpha_composite(img, vignette_overlay(0.55))
    cap = draw_caption(global_t)
    if cap is not None:
        img = Image.alpha_composite(img, cap)
    return img.convert("RGB")

# ─── glowed text — CRITICAL: render glow + sharp text into SEPARATE layers ─
def render_text_glow(text, fnt, color, glow_color=None, glow_radius=12, glow_strength=1.2):
    if glow_color is None: glow_color = color
    tmp = Image.new("RGBA", (1, 1))
    td = ImageDraw.Draw(tmp)
    bbox = td.textbbox((0, 0), text, font=fnt)
    pad = glow_radius * 2 + 8
    w = bbox[2] - bbox[0] + pad * 2
    h = bbox[3] - bbox[1] + pad * 2
    # 1) Glow layer (text in glow color, then blur, then alpha boost)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text((pad - bbox[0], pad - bbox[1]), text, font=fnt, fill=(*glow_color, 200))
    glow = glow.filter(ImageFilter.GaussianBlur(glow_radius))
    arr = np.array(glow).astype(np.int16)
    arr[..., 3] = np.clip(arr[..., 3] * glow_strength, 0, 255)
    glow = Image.fromarray(arr.astype(np.uint8))
    # 2) Sharp text on a separate layer
    main = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    md = ImageDraw.Draw(main)
    md.text((pad - bbox[0], pad - bbox[1]), text, font=fnt, fill=(*color, 255))
    # 3) Composite glow UNDER sharp text
    return Image.alpha_composite(glow, main), (-pad + bbox[0], -pad + bbox[1])

# ─── kinetic title — per-letter scale/rotate/bounce ────────────────────────
def kinetic_title(t, text, base_y, fnt, color=WHITE, glow_color=ACCENT,
                  start=0.0, char_delay=0.05, settle=0.7,
                  fade_out_at=None, fade_out_dur=0.5):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sizes = [text_size(ch, fnt) for ch in text]
    total_w = sum(s[0] for s in sizes)
    x_cursor = (W - total_w) // 2
    for i, ch in enumerate(text):
        delay = start + i * char_delay
        local = t - delay
        cw, chh = sizes[i]
        if local <= 0:
            x_cursor += cw; continue
        p = clamp01(local / settle)
        e = ease_out_back(p)
        off_y = (1 - e) * 90
        scale = 0.4 + 0.6 * e
        rot = (1 - e) * (15 if i % 2 == 0 else -15)
        a_in = clamp01(local / 0.4)
        a_out = 1.0 if fade_out_at is None or t <= fade_out_at \
                    else clamp01((fade_out_at + fade_out_dur - t) / fade_out_dur)
        a = a_in * a_out
        if a <= 0:
            x_cursor += cw; continue
        sprite, _ = render_text_glow(ch, fnt, color, glow_color,
                                     glow_radius=14, glow_strength=1.5)
        if scale != 1.0:
            ns = (max(1, int(sprite.width * scale)),
                  max(1, int(sprite.height * scale)))
            sprite = sprite.resize(ns, Image.LANCZOS)
        if abs(rot) > 0.1:
            sprite = sprite.rotate(rot, resample=Image.BICUBIC, expand=True)
        cx = x_cursor + cw / 2
        cy = base_y + chh / 2 + off_y
        paste_with_alpha(layer, sprite, cx - sprite.width/2, cy - sprite.height/2, alpha=a)
        x_cursor += cw
    return layer

# ─── neon accent line ──────────────────────────────────────────────────────
def neon_line(size, p1, p2, color=ACCENT, width=3, glow_radius=8):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([p1, p2], fill=(*color, 255), width=width+4)
    layer = layer.filter(ImageFilter.GaussianBlur(glow_radius))
    d2 = ImageDraw.Draw(layer)
    d2.line([p1, p2], fill=(*color, 255), width=width)
    return layer

# ─── icon library ──────────────────────────────────────────────────────────
def icon_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def icon_filmstrip(w, h, t, color=ACCENT, alpha=1.0):
    """Video / render concept icon — filmstrip with scrolling sprockets + play arrow."""
    spr = icon_canvas(w, h); d = ImageDraw.Draw(spr)
    body_x = int(w*0.18); body_w = int(w*0.64)
    d.rounded_rectangle([body_x, 4, body_x+body_w, h-4], radius=6, fill=(*color, int(220*alpha)))
    scroll = (t * 12) % 14
    hole_w = int(body_w * 0.07)
    for side_x in (body_x - hole_w//2 - 2, body_x + body_w - hole_w//2 + 2):
        for k in range(6):
            y = 6 + int(k*14 - scroll)
            if y + 8 < 0 or y > h: continue
            d.rounded_rectangle([side_x, y, side_x+hole_w, y+8], radius=2, fill=(*BG, int(255*alpha)))
    inner_x = body_x + int(body_w*0.14); inner_w = int(body_w*0.72)
    for k in range(3):
        y = 14 + k * int((h-28)/3)
        d.rounded_rectangle([inner_x, y, inner_x+inner_w, y + int((h-28)/3) - 6],
                            radius=3, fill=(*BG_2, int(255*alpha)))
    cx, cy = w//2, h//2; s = int(min(w, h)*0.13)
    d.polygon([(cx-s, cy-s), (cx-s, cy+s), (cx+s+2, cy)], fill=(*WHITE, int(255*alpha)))
    return spr

def icon_image_stack(w, h, t, color=ACCENT_2, alpha=1.0):
    """Images concept icon — 3 stacked image cards, top one shifts subtly."""
    spr = icon_canvas(w, h); d = ImageDraw.Draw(spr)
    card_w = int(w*0.72); card_h = int(h*0.66)
    base_x = (w - card_w) // 2; base_y = (h - card_h) // 2
    shifts = [(-10, 14), (-3, 6), (3 + int(math.sin(t*1.5)*2), -2)]
    fills = [(BG_2, 180), (BG_2, 220), (color, 240)]
    for (dx, dy), (rgb, op) in zip(shifts, fills):
        d.rounded_rectangle([base_x+dx, base_y+dy, base_x+dx+card_w, base_y+dy+card_h],
                            radius=8, fill=(*rgb, int(op*alpha)),
                            outline=(*WHITE, int(60*alpha)), width=1)
        if (dx, dy) == shifts[-1]:
            ix0, iy0 = base_x+dx+12, base_y+dy+12
            ix1, iy1 = base_x+dx+card_w-12, base_y+dy+card_h-22
            d.rectangle([ix0, iy0, ix1, iy1], fill=(*BG, int(220*alpha)))
            d.polygon([(ix0+6, iy1-4), (ix0+(ix1-ix0)//3, iy0+(iy1-iy0)//2),
                       (ix0+(ix1-ix0)//2+6, iy1-4)], fill=(*WHITE, int(200*alpha)))
            d.polygon([(ix0+(ix1-ix0)//2, iy1-4), (ix0+(ix1-ix0)*3//4, iy0+(iy1-iy0)//3),
                       (ix1-6, iy1-4)], fill=(*color, int(200*alpha)))
            sun_x, sun_y, sun_r = ix1-22, iy0+14, 6
            d.ellipse([sun_x-sun_r, sun_y-sun_r, sun_x+sun_r, sun_y+sun_r],
                      fill=(255, 220, 120, int(255*alpha)))
    return spr

def icon_browser(w, h, t, color=ACCENT_3, alpha=1.0):
    """Web / browser automation concept icon — animated cursor with click pulses."""
    spr = icon_canvas(w, h); d = ImageDraw.Draw(spr)
    pad = 6
    d.rounded_rectangle([pad, pad, w-pad, h-pad], radius=10,
                        fill=(*BG_2, int(240*alpha)),
                        outline=(*color, int(220*alpha)), width=2)
    bar_h = 22
    d.rounded_rectangle([pad, pad, w-pad, pad+bar_h], radius=10,
                        fill=(*color, int(140*alpha)))
    d.rectangle([pad, pad+bar_h-10, w-pad, pad+bar_h], fill=(*color, int(140*alpha)))
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        cx = pad + 8 + i*10
        d.ellipse([cx, pad+6, cx+6, pad+12], fill=(*c, int(255*alpha)))
    url_y0 = pad+bar_h+6
    d.rounded_rectangle([pad+8, url_y0, w-pad-30, url_y0+12], radius=3, fill=(*BG, int(220*alpha)))
    cy = url_y0+12 + 8
    for i in range(3):
        ly = cy + i*10
        d.rectangle([pad+12, ly, pad+12 + int((w-pad*2)*0.6) - i*10, ly+4],
                    fill=(*WHITE, int(140*alpha)))
    cx_anim = pad + 0.55*(w-pad*2) + math.sin(t*2.1) * 22
    cy_anim = cy + 28 + math.cos(t*1.7) * 8
    d.polygon([(cx_anim, cy_anim), (cx_anim, cy_anim+14),
               (cx_anim+4, cy_anim+10), (cx_anim+10, cy_anim+14),
               (cx_anim+12, cy_anim+12), (cx_anim+7, cy_anim+7),
               (cx_anim+12, cy_anim+5)], fill=(*WHITE, int(255*alpha)))
    pulse_t = (t * 0.7) % 1.0
    if pulse_t < 0.25:
        rr = int(4 + pulse_t * 40)
        d.ellipse([cx_anim-rr, cy_anim-rr, cx_anim+rr, cy_anim+rr],
                  outline=(*color, int((1 - pulse_t/0.25) * 200 * alpha)), width=2)
    return spr

def icon_waveform(w, h, t, color=ACCENT_2, alpha=1.0):
    """Audio / transcribe concept icon — animated equalizer bars + carrier line."""
    spr = icon_canvas(w, h); d = ImageDraw.Draw(spr)
    cx, cy = w//2, h//2
    n = 18
    bar_w = max(2, int(w*0.045))
    gap = max(1, int((w - n*bar_w) / (n+1)))
    x = gap
    for i in range(n):
        env = math.sin(math.pi * (i + 0.5) / n)
        amp = (math.sin(t*5 + i*0.7) * 0.5 + math.sin(t*3.2 + i*0.4) * 0.5) * 0.5 + 0.5
        bar_h = int(env * amp * (h*0.7) + h*0.08)
        d.rounded_rectangle([x, cy - bar_h//2, x + bar_w, cy + bar_h//2],
                            radius=2, fill=(*color, int(230*alpha)))
        x += bar_w + gap
    line_glow = Image.new("RGBA", (w, h), (0,0,0,0))
    ld = ImageDraw.Draw(line_glow)
    ld.line([(8, cy), (w-8, cy)], fill=(*color, int(80*alpha)), width=4)
    line_glow = line_glow.filter(ImageFilter.GaussianBlur(4))
    return Image.alpha_composite(spr, line_glow)

def icon_design_canvas(w, h, t, color=ACCENT, alpha=1.0):
    """Design / prototype concept icon — mini canvas with header, text rows, button, sparkle."""
    spr = icon_canvas(w, h); d = ImageDraw.Draw(spr)
    pad = 8
    d.rounded_rectangle([pad, pad, w-pad, h-pad], radius=8,
                        fill=(*BG_2, int(240*alpha)),
                        outline=(*color, int(220*alpha)), width=2)
    d.rounded_rectangle([pad+8, pad+8, w-pad-8, pad+22], radius=3,
                        fill=(*color, int(220*alpha)))
    rows_y = pad+30
    row_w = w - pad*2 - 16
    for i, frac in enumerate([1.0, 0.85, 0.6]):
        phase = math.sin(t*1.4 + i*0.7) * 0.5 + 0.5
        opa = int((200 - i*40) * alpha * (0.65 + 0.35 * phase))
        d.rectangle([pad+8, rows_y + i*10, pad+8 + int(row_w*frac), rows_y + i*10 + 4],
                    fill=(*WHITE, opa))
    d.rounded_rectangle([pad + 12, h - pad - 20, pad + 60, h - pad - 8], radius=4,
                        fill=(*color, int(255*alpha)))
    sp_x = w - pad - 18 + math.sin(t*2.3) * 3
    sp_y = pad + 38 + math.cos(t*2.1) * 3
    sp_a = (math.sin(t*4) + 1) * 0.5
    sp_r = 3
    d.ellipse([sp_x-sp_r, sp_y-sp_r, sp_x+sp_r, sp_y+sp_r],
              fill=(255, 255, 200, int(255*alpha*sp_a)))
    return spr

# ─── terminal mock ─────────────────────────────────────────────────────────
def draw_terminal_window(layer, x, y, w, h, title, alpha=1.0):
    """Draw a glowing terminal-style window onto `layer`."""
    a = alpha
    d = ImageDraw.Draw(layer)
    glow = Image.new("RGBA", (w+60, h+60), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle([30, 30, 30+w, 30+h], radius=18, fill=(*ACCENT, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    paste_with_alpha(layer, glow, x-30, y-30, a*0.7)
    d.rounded_rectangle([x, y, x+w, y+h], radius=18, fill=with_alpha(TERMINAL_BG, a),
                        outline=with_alpha((60, 60, 80), a), width=1)
    d.rounded_rectangle([x, y, x+w, y+48], radius=18, fill=with_alpha((30, 30, 46), a))
    d.rectangle([x, y+32, x+w, y+48], fill=with_alpha((30, 30, 46), a))
    for i, c in enumerate([(255,95,86), (255,189,46), (39,201,63)]):
        cx = x + 22 + i*22
        d.ellipse([cx, y+16, cx+14, y+30], fill=with_alpha(c, a))
    ff = font("medium", 16)
    tw, _ = text_size(title, ff)
    d.text((x + w/2 - tw/2, y + 16), title, font=ff, fill=with_alpha(DIM, a*0.9))

def scanline_strip(w, h, alpha=1.0):
    """CRT scanline overlay sized to a terminal window. Composite at the window's origin."""
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[::3, :, 3] = int(20 * alpha)
    return Image.fromarray(arr)

def oscilloscope(x, y, w, h, t, alpha=1.0, amplitude=14.0):
    """Glowing multi-sine waveform overlay — full-canvas RGBA layer."""
    layer = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    points = []
    for px in range(0, w, 2):
        v = (math.sin((px / w) * 12 + t * 6) * 0.6 +
             math.sin((px / w) * 30 + t * 9) * 0.25 +
             math.sin((px / w) * 50 + t * 14) * 0.15)
        py = y + h/2 + v * amplitude
        points.append((x + px, py))
    if len(points) >= 2:
        glow = Image.new("RGBA", (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        gd.line(points, fill=(*ACCENT_2, int(180*alpha)), width=4)
        glow = glow.filter(ImageFilter.GaussianBlur(6))
        layer = Image.alpha_composite(layer, glow)
        d = ImageDraw.Draw(layer)
        d.line(points, fill=(*ACCENT_2, int(255*alpha)), width=2)
    return layer

# ─── EXAMPLE SCENES — edit these for your project ──────────────────────────
# Each scene takes (local_t, dur, scene_offset_in_global_cut). Call finalize() last.

def scene_1(t, dur=5.0, scene_offset=0.0):
    base = bg_layer(t)
    base.alpha_composite(kinetic_title(
        t, "Your Title", base_y=240, fnt=font("bold", 130),
        color=WHITE, glow_color=ACCENT,
        char_delay=0.05, settle=0.7, fade_out_at=dur-0.5))
    return finalize(base, scene_offset + t)

def scene_2_tools_grid(t, dur=12.0, scene_offset=4.6):
    """Example: 5 tool cards rising from below with elastic ease + custom icons."""
    base = bg_layer(t)
    base.alpha_composite(kinetic_title(
        t, "Five tools, one stack", base_y=70, fnt=font("bold", 78),
        color=WHITE, glow_color=ACCENT,
        char_delay=0.025, settle=0.6, fade_out_at=dur-0.6))

    tools = [
        ("FFmpeg",      "Video",   "filmstrip",     ACCENT),
        ("ImageMagick", "Images",  "image_stack",   ACCENT_2),
        ("Playwright",  "Browser", "browser",       ACCENT_3),
        ("Whisper.cpp", "Audio",   "waveform",      ACCENT_2),
        ("Open Design", "Design",  "design_canvas", ACCENT),
    ]
    icon_fns = {
        "filmstrip":     icon_filmstrip,
        "image_stack":   icon_image_stack,
        "browser":       icon_browser,
        "waveform":      icon_waveform,
        "design_canvas": icon_design_canvas,
    }
    card_w, card_h = 200, 260
    gap = 22
    total_w = 5 * card_w + 4 * gap
    start_x = (W - total_w) // 2
    cards_y = 200
    for i, (name, cat, kind, color) in enumerate(tools):
        delay = 0.6 + i * 0.18
        local = t - delay
        if local <= 0: continue
        p = clamp01(local / 0.85)
        e = ease_out_elastic(p)
        off_y = (1 - e) * 200
        a = clamp01(local / 0.35)
        if t > dur - 0.6: a *= clamp01((dur - t) / 0.6)
        x0 = start_x + i * (card_w + gap)
        y0 = int(cards_y + off_y)
        # card glow halo
        glow = Image.new("RGBA", (card_w + 60, card_h + 60), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        gd.rounded_rectangle([30, 30, 30+card_w, 30+card_h], radius=22, fill=(*color, 70))
        glow = glow.filter(ImageFilter.GaussianBlur(18))
        paste_with_alpha(base, glow, x0-30, y0-30, a*0.9)
        # card body — composite FIRST
        layer_c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lcd = ImageDraw.Draw(layer_c)
        lcd.rounded_rectangle([x0, y0, x0+card_w, y0+card_h], radius=22,
                              fill=(*BG_2, int(230*a)),
                              outline=with_alpha(color, a*0.9), width=2)
        base.alpha_composite(layer_c)
        # THEN paste icon and name on top
        ic = icon_fns[kind](card_w - 36, 130, t - delay, color, a)
        paste_with_alpha(base, ic, x0 + 18, y0 + 16, a)
        layer_t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ltd = ImageDraw.Draw(layer_t)
        fnt_n = font("bold", 22)
        nw, _ = text_size(name, fnt_n)
        ltd.text((x0 + card_w/2 - nw/2, y0 + 168), name, font=fnt_n, fill=with_alpha(WHITE, a))
        fnt_s = font("regular", 16)
        sw, _ = text_size(cat.upper(), fnt_s)
        ltd.text((x0 + card_w/2 - sw/2, y0 + 200), cat.upper(),
                 font=fnt_s, fill=with_alpha(color, a))
        base.alpha_composite(layer_t)
    return finalize(base, scene_offset + t)

def scene_3_terminal(t, dur=14.0, scene_offset=16.6):
    """Example: animated install terminal with typewriter + scanlines + log scroll + progress."""
    base = bg_layer(t)
    base.alpha_composite(kinetic_title(
        t, "Install", base_y=50, fnt=font("bold", 64),
        color=WHITE, glow_color=ACCENT,
        char_delay=0.03, settle=0.5, fade_out_at=dur-0.6))

    if t < 0.55: return finalize(base, scene_offset + t)
    local = t - 0.55
    p = clamp01(local / 0.7); e = ease_out_back(p, s=0.8)
    a = clamp01(local / 0.4)
    if t > dur - 0.6: a *= clamp01((dur - t) / 0.6)
    tw_w, tw_h = 960, 400
    tx = (W - tw_w)//2
    ty = 160 + int((1 - e) * 50)
    term_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_terminal_window(term_layer, tx, ty, tw_w, tw_h, "Terminal — bash", alpha=a)
    sl = scanline_strip(tw_w, tw_h, alpha=a)
    term_layer.alpha_composite(sl, (tx, ty))
    base = Image.alpha_composite(base, term_layer)
    # typewriter command
    mono = font("mono", 19)
    cmd = "curl -fsSL https://example.com/install.sh | bash"
    c_start = 0.55 + 0.85
    if t >= c_start:
        chars = min(len(cmd), int((t - c_start) / 0.025))
        shown = cmd[:chars]
        d = ImageDraw.Draw(base)
        d.text((tx+26, ty+64), "$", font=mono, fill=with_alpha(ACCENT_2, a))
        d.text((tx+52, ty+64), shown, font=mono, fill=with_alpha(WHITE, a))
        if chars < len(cmd) and int(t*2)%2 == 0:
            wsf = text_size(shown, mono)[0]
            d.rectangle([tx+52+wsf, ty+66, tx+52+wsf+10, ty+88], fill=with_alpha(WHITE, a))
    # animated log + oscilloscope + progress
    inst_start = c_start + 0.025*len(cmd) + 0.4
    if t >= inst_start:
        inst_t = t - inst_start
        log_lines = [
            ("==> Step 1 …",            GREEN),
            ("==> Step 2 …",            GREEN),
            ("    detail line",         DIM),
            ("==> Step 3 …",            YELLOW),
            ("==> All installed ✓",     GREEN),
        ]
        small = font("mono-r", 16)
        d2 = ImageDraw.Draw(base)
        for i, (ln, color) in enumerate(log_lines):
            lt = inst_t - i * 0.4
            if lt <= 0: break
            la = clamp01(lt / 0.2)
            d2.text((tx+26, ty+130 + i*22), ln, font=small, fill=with_alpha(color, a*la))
        base = Image.alpha_composite(base,
            oscilloscope(tx+24, ty+tw_h-90, tw_w-48, 26, t, alpha=a, amplitude=9))
        # progress bar
        pb_x = tx + 26; pb_y = ty + tw_h - 46; pb_w = tw_w - 52
        d3 = ImageDraw.Draw(base)
        d3.rounded_rectangle([pb_x, pb_y, pb_x+pb_w, pb_y+14], radius=7,
                              fill=with_alpha((30,30,46), a))
        prog = clamp01(inst_t / (0.4 * len(log_lines) + 0.5))
        prog_w = int(pb_w * ease_in_out_cubic(prog))
        d3.rounded_rectangle([pb_x, pb_y, pb_x+prog_w, pb_y+14], radius=7,
                              fill=with_alpha(ACCENT, a))
    return finalize(base, scene_offset + t)

# ─── scene registry — edit per project ─────────────────────────────────────
SCENES = {
    1: (scene_1,            5.0,  0.0),
    2: (scene_2_tools_grid, 12.0, 4.6),
    3: (scene_3_terminal,   14.0, 16.2),
}

def render_scene(n, out_dir):
    fn, dur, offset = SCENES[n]
    os.makedirs(out_dir, exist_ok=True)
    total = int(dur * FPS)
    for fi in range(total):
        t = fi / FPS
        img = fn(t, dur, offset)
        img.save(os.path.join(out_dir, f"frame_{fi:05d}.png"), optimize=False)
    return total, dur

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    base = "./anim"
    if arg == "all":
        for n in sorted(SCENES):
            d = f"{base}/s{n:02d}"
            f, du = render_scene(n, d)
            print(f"scene {n}: {f} frames ({du}s)")
        print()
        print("Encode + stitch:")
        cumulative = 0.0
        encode_lines = []
        xfade_chain = []
        for n in sorted(SCENES):
            _, dur, _ = SCENES[n]
            encode_lines.append(f"ffmpeg -y -framerate 30 -i {base}/s{n:02d}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -movflags +faststart {base}/s{n:02d}.mp4")
        for line in encode_lines: print("  " + line)
        # build xfade chain
        ids = sorted(SCENES)
        prev = "[0:v]"
        chain = []
        cum = SCENES[ids[0]][1]
        for i, n in enumerate(ids[1:], start=1):
            cum_before = sum(SCENES[ids[j]][1] for j in range(i)) - 0.4 * (i - 1)
            offset = cum_before - 0.4
            label = f"[v{i}]"
            chain.append(f"{prev}[{i}:v]xfade=transition=fade:duration=0.4:offset={offset:.2f}{label}")
            prev = label
        inputs = " ".join(f"-i {base}/s{n:02d}.mp4" for n in ids)
        final_label = prev
        print(f"  ffmpeg -y {inputs} -filter_complex \"" + ";".join(chain) + f"\" -map \"{final_label}\" -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -movflags +faststart final.mp4")
    else:
        n = int(arg)
        d = f"{base}/s{n:02d}"
        f, du = render_scene(n, d)
        print(f"scene {n}: {f} frames ({du}s)")
