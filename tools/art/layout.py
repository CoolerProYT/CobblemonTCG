"""
Card layout in the style of the 1999 Base Set (original drawing, no official assets):
yellow border, a card face coloured by type, name and HP on top, framed art window,
attack rows with energy costs, weakness / resistance / retreat bar, number and rarity at the bottom.

All coordinates are pixels in a 256x256 texture; the card itself is 184x256 in the middle.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SIZE = 256
SS = 4
CARD = (36, 0, 219, 255)
FACE = (43, 7, 212, 248)
NAME_Y = 10
ART = (51, 29, 204, 120)            # art window, inclusive
INFO = (58, 124, 197, 130)
ATTACK_ROWS = (139, 175)
WRR = (48, 203, 207, 216)
FLAVOR = (54, 220, 201, 235)
FOOTER_Y = 238

YELLOW = (238, 200, 60)
YELLOW_DARK = (196, 150, 30)
TEXT = (30, 26, 28)

TYPE_COLORS = {
    "grass": (120, 184, 82),
    "fire": (232, 104, 64),
    "water": (82, 146, 222),
    "lightning": (246, 206, 64),
    "psychic": (170, 112, 190),
    "fighting": (196, 120, 70),
    "colorless": (222, 220, 210),
}
FACE_COLORS = {
    "grass": (178, 214, 140),
    "fire": (240, 168, 128),
    "water": (156, 196, 236),
    "lightning": (250, 228, 140),
    "psychic": (206, 172, 218),
    "fighting": (222, 176, 136),
    "colorless": (236, 234, 226),
    "trainer": (222, 222, 226),
    "energy": (244, 240, 226),
}
WEAKNESS = {
    "grass": "fire", "fire": "water", "water": "lightning", "lightning": "fighting",
    "psychic": "psychic", "fighting": "psychic", "colorless": "fighting",
}
RESISTANCE = {"colorless": "psychic", "fighting": None, "lightning": None, "grass": None,
              "fire": None, "water": None, "psychic": None}


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.load_default(size=size)


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rgba(c, a=255):
    return (*c, a)


ACCENTED = {"é": "e", "É": "E"}


def text(img: Image.Image, xy, s: str, size: int, color=TEXT, bold=False, anchor="la", max_width=None):
    """Draws text; shrinks it until it fits max_width. The bundled font is ASCII only, so
    accented letters and the male / female signs are drawn by hand."""
    d = ImageDraw.Draw(img)
    plain = "".join(ACCENTED.get(c, "  " if c in "♂♀" else c) for c in s)
    while True:
        f = font(size)
        width = d.textlength(plain, font=f) + (1 if bold else 0)
        if max_width is None or width <= max_width or size <= 7:
            break
        size -= 1
    x0 = xy[0] - (width / 2 if anchor[0] == "m" else width if anchor[0] == "r" else 0)
    top = xy[1]
    for dx in ((0, 1) if bold else (0,)):
        d.text((x0 + dx, top), plain, font=f, fill=rgba(color), anchor="la")

    # hand-drawn extras, positioned from the width of the text before them
    prefix = ""
    for c in s:
        px = x0 + d.textlength(prefix, font=f)
        if c in ACCENTED:
            cw = d.textlength(ACCENTED[c], font=f)
            d.line((px + cw * 0.45, top + size * 0.28, px + cw * 0.75, top + size * 0.08), fill=rgba(color), width=max(1, size // 10))
            prefix += ACCENTED[c]
        elif c in "♂♀":
            r = size * 0.22
            cx, cy = px + size * 0.3, top + size * 0.62
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(color), width=max(1, size // 9))
            if c == "♂":
                d.line((cx + r * 0.7, cy - r * 0.7, cx + r * 1.9, cy - r * 1.9), fill=rgba(color), width=max(1, size // 9))
                d.line((cx + r * 1.0, cy - r * 1.9, cx + r * 1.9, cy - r * 1.9, cx + r * 1.9, cy - r * 1.0), fill=rgba(color), width=max(1, size // 9))
            else:
                d.line((cx, cy + r, cx, cy + r * 2.2), fill=rgba(color), width=max(1, size // 9))
                d.line((cx - r * 0.6, cy + r * 1.6, cx + r * 0.6, cy + r * 1.6), fill=rgba(color), width=max(1, size // 9))
            prefix += "  "
        else:
            prefix += c
    return width


# ---------------------------------------------------------------- symbols

def type_symbol(kind: str, diameter: int) -> Image.Image:
    """Round energy symbol of a type, drawn from simple shapes."""
    n = diameter * SS
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    base = TYPE_COLORS[kind]
    d.ellipse((0, 0, n - 1, n - 1), fill=rgba(mix(base, (0, 0, 0), 0.45)))
    d.ellipse((n * 0.06, n * 0.06, n * 0.94, n * 0.94), fill=rgba(base))
    d.ellipse((n * 0.12, n * 0.1, n * 0.62, n * 0.5), fill=rgba(mix(base, (255, 255, 255), 0.35)))
    d.ellipse((n * 0.06, n * 0.06, n * 0.94, n * 0.94), outline=rgba(mix(base, (0, 0, 0), 0.25)), width=max(1, n // 20))
    glyph = (40, 34, 36) if kind in ("lightning", "colorless") else (255, 255, 255)
    g = rgba(glyph)
    c = n / 2
    s = n * 0.3

    def P(x, y):
        return (c + x * s, c + y * s)

    if kind == "fire":
        flame = [(0, 1.0), (-0.62, 0.78), (-0.85, 0.2), (-0.6, -0.4), (-0.42, 0.05), (-0.25, -0.75), (-0.05, -0.2),
                 (0.12, -1.15), (0.32, -0.3), (0.52, -0.62), (0.6, 0.0), (0.85, 0.25), (0.62, 0.78)]
        d.polygon([P(x, y) for x, y in flame], fill=g)
    elif kind == "water":
        pts = [P(0, -1.1)] + [P(0.6 * math.cos(a), 0.3 + 0.6 * math.sin(a)) for a in [math.radians(t) for t in range(-30, 211, 10)]]
        d.polygon(pts, fill=g)
    elif kind == "grass":
        d.polygon([P(0, -1.1), P(0.75, -0.2), P(0.45, 0.6), P(0, 0.85), P(-0.45, 0.6), P(-0.75, -0.2)], fill=g)
        d.line([P(0, -0.7), P(0, 1.0)], fill=rgba(base), width=max(1, n // 18))
    elif kind == "lightning":
        d.polygon([P(0.2, -1.1), P(-0.55, 0.1), P(-0.05, 0.1), P(-0.3, 1.1), P(0.55, -0.15), P(0.05, -0.15), P(0.35, -1.1)], fill=g)
    elif kind == "psychic":
        d.ellipse((P(-0.95, -0.55)[0], P(-0.95, -0.55)[1], P(0.95, 0.55)[0], P(0.95, 0.55)[1]), fill=g)
        d.ellipse((P(-0.4, -0.4)[0], P(-0.4, -0.4)[1], P(0.4, 0.4)[0], P(0.4, 0.4)[1]), fill=rgba(mix(base, (0, 0, 0), 0.4)))
    elif kind == "fighting":
        d.rounded_rectangle((P(-0.75, -0.55)[0], P(-0.75, -0.55)[1], P(0.75, 0.75)[0], P(0.75, 0.75)[1]), radius=s * 0.3, fill=g)
        for i in range(3):
            x = -0.5 + i * 0.5
            d.line([P(x, -0.55), P(x, 0.1)], fill=rgba(base), width=max(1, n // 22))
    else:  # colorless
        pts = []
        for i in range(10):
            r = 0.95 if i % 2 == 0 else 0.4
            a = math.radians(-90 + i * 36)
            pts.append(P(r * math.cos(a), r * math.sin(a)))
        d.polygon(pts, fill=g)
    return img.resize((diameter, diameter), Image.LANCZOS)


def paste_symbol(img, kind, cx, cy, diameter):
    sym = type_symbol(kind, diameter)
    img.alpha_composite(sym, (round(cx - diameter / 2), round(cy - diameter / 2)))


def rarity_symbol(img, rarity, cx, cy):
    """Circle = common, diamond = uncommon, star = rare (holo rares carry a star too)."""
    n = 12 * SS
    s = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = n / 2
    if rarity == "common":
        d.ellipse((c - n * 0.28, c - n * 0.28, c + n * 0.28, c + n * 0.28), fill=rgba(TEXT))
    elif rarity == "uncommon":
        d.polygon([(c, c - n * 0.36), (c + n * 0.36, c), (c, c + n * 0.36), (c - n * 0.36, c)], fill=rgba(TEXT))
    else:
        pts = []
        for i in range(10):
            r = n * (0.44 if i % 2 == 0 else 0.19)
            a = math.radians(-90 + i * 36)
            pts.append((c + r * math.cos(a), c + r * math.sin(a)))
        d.polygon(pts, fill=rgba(TEXT))
    img.alpha_composite(s.resize((12, 12), Image.LANCZOS), (round(cx - 6), round(cy - 6)))


# ---------------------------------------------------------------- frames

def _card_base(face_color) -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(CARD, radius=10, fill=rgba(YELLOW_DARK))
    d.rounded_rectangle((CARD[0] + 1, CARD[1] + 1, CARD[2] - 1, CARD[3] - 1), radius=9, fill=rgba(YELLOW))
    d.rounded_rectangle(FACE, radius=4, fill=rgba(face_color))

    # faint diagonal texture on the face, like printed card stock
    arr = np.asarray(img).astype(np.int16)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    mask = (xx >= FACE[0]) & (xx <= FACE[2]) & (yy >= FACE[1]) & (yy <= FACE[3]) & (((xx + yy) % 7) < 2)
    arr[mask, :3] = np.clip(arr[mask, :3] + 10, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def _art_window(img, kind, foil_rim=False):
    d = ImageDraw.Draw(img)
    rim = (226, 196, 110) if not foil_rim else (200, 200, 210)
    d.rectangle((ART[0] - 4, ART[1] - 4, ART[2] + 4, ART[3] + 4), fill=rgba(mix(rim, (60, 50, 30), 0.35)))
    d.rectangle((ART[0] - 3, ART[1] - 3, ART[2] + 3, ART[3] + 3), fill=rgba(rim))
    d.rectangle((ART[0] - 1, ART[1] - 1, ART[2] + 1, ART[3] + 1), fill=rgba(mix(rim, (40, 30, 20), 0.5)))
    img.alpha_composite(background(kind), (ART[0], ART[1]))


def pokemon_frame(kind: str) -> Image.Image:
    img = _card_base(FACE_COLORS[kind])
    d = ImageDraw.Draw(img)
    _art_window(img, kind)

    # info strip under the art (length / weight line on real cards)
    d.rounded_rectangle(INFO, radius=3, fill=rgba((236, 214, 140)), outline=rgba((176, 150, 80)))

    # attack rows: separators only, costs and names are per card
    line_col = rgba(mix(FACE_COLORS[kind], (0, 0, 0), 0.35))
    for y in (ATTACK_ROWS[1] - 6,):
        d.line((52, y, 203, y), fill=line_col, width=1)
    d.line((48, WRR[1] - 3, 207, WRR[1] - 3), fill=line_col, width=1)

    # weakness / resistance / retreat labels
    labels = ("weakness", "resistance", "retreat cost")
    cell = (WRR[2] - WRR[0]) / 3
    for i, label in enumerate(labels):
        cx = WRR[0] + cell * i + cell / 2
        text(img, (cx, WRR[1] + 1), label, 7, mix(TEXT, FACE_COLORS[kind], 0.25), anchor="ma")

    # flavour box
    d.rounded_rectangle(FLAVOR, radius=2, outline=rgba(mix(FACE_COLORS[kind], (0, 0, 0), 0.3)))
    for y in (FLAVOR[1] + 5, FLAVOR[1] + 10):
        d.line((FLAVOR[0] + 6, y, FLAVOR[2] - 6, y), fill=rgba(mix(FACE_COLORS[kind], (0, 0, 0), 0.18)))
    text(img, (50, FOOTER_Y), "Illus.", 7, mix(TEXT, FACE_COLORS[kind], 0.3))
    return img


def trainer_frame() -> Image.Image:
    img = _card_base(FACE_COLORS["trainer"])
    d = ImageDraw.Draw(img)
    _art_window(img, "trainer", foil_rim=True)
    d.rounded_rectangle((52, 128, 203, 228), radius=3, fill=rgba((244, 244, 246)), outline=rgba((150, 150, 158)))
    for y in range(140, 222, 9):
        d.line((60, y, 195, y), fill=rgba((196, 196, 204)))
    text(img, (50, FOOTER_Y), "Illus.", 7, (110, 110, 118))
    return img


def energy_frame() -> Image.Image:
    img = _card_base(FACE_COLORS["energy"])
    d = ImageDraw.Draw(img)
    d.rectangle((50, 28, 205, 232), outline=rgba((200, 186, 140)), width=1)
    return img


# ---------------------------------------------------------------- backgrounds

def _gradient(w, h, top, bottom):
    arr = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        arr[y, :, :3] = mix(top, bottom, y / max(h - 1, 1))
        arr[y, :, 3] = 255
    return Image.fromarray(arr, "RGBA")


def background(kind: str) -> Image.Image:
    """Art window scenery per type, shared by every card of that type."""
    w, h = (ART[2] - ART[0] + 1) * SS, (ART[3] - ART[1] + 1) * SS
    rng = random.Random(kind)
    horizon = int(h * 0.62)

    def sky(top, bottom):
        return _gradient(w, h, top, bottom)

    if kind == "fire":
        img = sky((250, 196, 110), (236, 110, 70))
        d = ImageDraw.Draw(img)
        d.polygon([(0, horizon), (w * 0.18, h * 0.3), (w * 0.34, horizon)], fill=rgba((120, 60, 50)))
        d.polygon([(w * 0.55, horizon), (w * 0.78, h * 0.22), (w, horizon)], fill=rgba((96, 46, 44)))
        d.polygon([(w * 0.74, h * 0.25), (w * 0.78, h * 0.22), (w * 0.82, h * 0.25), (w * 0.79, h * 0.12)], fill=rgba((250, 120, 50)))
        d.rectangle((0, horizon, w, h), fill=rgba((150, 82, 52)))
        for _ in range(14):
            x, y = rng.uniform(0, w), rng.uniform(horizon + 6, h)
            r = rng.uniform(4, 12) * SS / 4
            d.ellipse((x - r * 2, y - r, x + r * 2, y + r), fill=rgba((120, 64, 44)))
    elif kind == "water":
        img = sky((170, 220, 250), (220, 240, 252))
        d = ImageDraw.Draw(img)
        d.rectangle((0, horizon - 10, w, h), fill=rgba((60, 130, 210)))
        for i in range(9):
            y = horizon + i * (h - horizon) / 8
            for x in range(0, w, 60):
                ox = rng.uniform(-20, 20)
                d.arc((x + ox, y - 8, x + ox + 50, y + 8), 200, 340, fill=rgba((180, 220, 250)), width=SS)
    elif kind == "grass":
        img = sky((170, 214, 246), (226, 244, 222))
        d = ImageDraw.Draw(img)
        d.ellipse((-w * 0.2, horizon - h * 0.2, w * 0.6, horizon + h * 0.3), fill=rgba((128, 186, 110)))
        d.ellipse((w * 0.4, horizon - h * 0.16, w * 1.3, horizon + h * 0.3), fill=rgba((112, 172, 98)))
        d.rectangle((0, horizon, w, h), fill=rgba((104, 168, 80)))
        for _ in range(40):
            x, y = rng.uniform(0, w), rng.uniform(horizon + 4, h)
            d.line((x, y, x + rng.uniform(-4, 4), y - rng.uniform(6, 14)), fill=rgba((76, 140, 60)), width=SS)
        for bx in (w * 0.08, w * 0.92):
            d.ellipse((bx - 40, horizon - 70, bx + 40, horizon + 10), fill=rgba((70, 138, 64)))
    elif kind == "lightning":
        img = sky((54, 50, 96), (120, 110, 150))
        d = ImageDraw.Draw(img)
        for x in (w * 0.15, w * 0.85):
            pts, y = [(x, 0)], 0
            while y < horizon - 20:
                y += rng.uniform(16, 30)
                pts.append((pts[-1][0] + rng.uniform(-14, 14), y))
            d.line(pts, fill=rgba((255, 240, 140)), width=SS)
        d.rectangle((0, horizon, w, h), fill=rgba((86, 84, 96)))
        for _ in range(10):
            x, y = rng.uniform(0, w), rng.uniform(horizon + 4, h)
            d.ellipse((x - 14, y - 5, x + 14, y + 5), fill=rgba((70, 68, 80)))
    elif kind == "psychic":
        img = sky((96, 60, 140), (220, 150, 210))
        d = ImageDraw.Draw(img)
        for _ in range(50):
            x, y = rng.uniform(0, w), rng.uniform(0, horizon)
            r = rng.uniform(1, 3) * SS / 2
            d.ellipse((x - r, y - r, x + r, y + r), fill=rgba((255, 240, 255)))
        for r in (60, 110, 160):
            d.ellipse((w / 2 - r * 2, h * 0.35 - r, w / 2 + r * 2, h * 0.35 + r), outline=rgba((240, 190, 240), 120), width=SS)
        d.rectangle((0, horizon, w, h), fill=rgba((132, 92, 150)))
    elif kind == "fighting":
        img = sky((246, 206, 150), (232, 170, 110))
        d = ImageDraw.Draw(img)
        d.polygon([(0, h * 0.15), (w * 0.22, h * 0.2), (w * 0.28, horizon), (0, horizon)], fill=rgba((150, 92, 60)))
        d.polygon([(w, h * 0.1), (w * 0.76, h * 0.24), (w * 0.7, horizon), (w, horizon)], fill=rgba((136, 82, 54)))
        d.rectangle((0, horizon, w, h), fill=rgba((176, 120, 76)))
        for _ in range(12):
            x, y = rng.uniform(0, w), rng.uniform(horizon + 6, h)
            d.ellipse((x - 16, y - 6, x + 16, y + 6), fill=rgba((150, 100, 62)))
    elif kind == "trainer":
        img = sky((236, 236, 240), (200, 206, 220))
        d = ImageDraw.Draw(img)
        for i in range(0, w, 24):
            d.line((i, 0, i - h * 0.6, h), fill=rgba((222, 224, 232)), width=SS * 2)
    else:  # colorless
        img = sky((140, 196, 246), (214, 236, 252))
        d = ImageDraw.Draw(img)
        for cx, cy in ((w * 0.2, h * 0.2), (w * 0.75, h * 0.14), (w * 0.5, h * 0.32)):
            for dx in (-30, 0, 30):
                d.ellipse((cx + dx - 34, cy - 18, cx + dx + 34, cy + 18), fill=rgba((255, 255, 255)))
        d.rectangle((0, horizon, w, h), fill=rgba((150, 196, 110)))
        for _ in range(30):
            x, y = rng.uniform(0, w), rng.uniform(horizon + 4, h)
            d.line((x, y, x + rng.uniform(-4, 4), y - rng.uniform(5, 10)), fill=rgba((112, 166, 84)), width=SS)
    return img.resize((ART[2] - ART[0] + 1, ART[3] - ART[1] + 1), Image.LANCZOS)


# ---------------------------------------------------------------- holo foil

def holo_overlay(frames: int = 8):
    """Animated foil over the art window. Sits between the frame and the card art."""
    w, h = ART[2] - ART[0] + 1, ART[3] - ART[1] + 1
    strip = np.zeros((SIZE * frames, SIZE, 4), np.uint8)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (xx + yy * 1.3) / (w + h * 1.3)
    rng = np.random.default_rng(7)
    sparkle = rng.random((h, w)) > 0.985
    for f in range(frames):
        phase = f / frames
        hue = (d * 1.6 - phase) % 1.0
        r = 0.5 + 0.5 * np.cos((hue + 0.0) * 2 * np.pi)
        g = 0.5 + 0.5 * np.cos((hue + 0.33) * 2 * np.pi)
        b = 0.5 + 0.5 * np.cos((hue + 0.66) * 2 * np.pi)
        band = np.clip(np.cos((d - phase * 1.2) * 2 * np.pi * 1.5), 0, 1) ** 2
        rgb = np.stack([r, g, b], -1) * 0.55 + 0.45
        rgb = rgb * (0.75 + 0.25 * band[..., None])
        alpha = 150 + 80 * band
        tile = np.zeros((h, w, 4), np.float32)
        tile[..., :3] = rgb * 255
        tile[..., 3] = alpha
        tw = np.roll(sparkle, f * 3, axis=1)
        tile[tw] = (255, 255, 255, 255)
        strip[f * SIZE + ART[1]:f * SIZE + ART[1] + h, ART[0]:ART[0] + w] = tile.astype(np.uint8)
    return Image.fromarray(strip, "RGBA"), {"animation": {"frametime": 3, "interpolate": True}}
