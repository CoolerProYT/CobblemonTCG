import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import finish as F

W, H = 256, 352
SS = 4
RADIUS = 13
FACE = (11, 11, 244, 340)
STAGE_Y = 13
NAME_Y = 34
ART = (24, 40, 231, 183)
STRIP = (30, 188, 225, 198)
BODY = (22, 203, 233, 292)
WRR = (18, 296, 237, 311)
FLAVOR = (22, 314, 233, 328)
FOOTER_Y = 332
RULES = (22, 194, 233, 326)
EVOLUTION_BOX = (14, 13, 45, 36)

YELLOW = (246, 212, 70)
YELLOW_LIGHT = (255, 236, 130)
YELLOW_DARK = (200, 156, 36)
TEXT = (28, 24, 26)

TYPE_COLORS = {
    "grass": (96, 170, 70),
    "fire": (226, 86, 50),
    "water": (64, 130, 214),
    "lightning": (246, 200, 40),
    "psychic": (150, 92, 176),
    "fighting": (186, 104, 56),
    "colorless": (226, 224, 214),
}
FACE_COLORS = {
    "grass": (170, 206, 128),
    "fire": (238, 156, 112),
    "water": (148, 188, 232),
    "lightning": (246, 222, 128),
    "psychic": (196, 160, 210),
    "fighting": (214, 166, 124),
    "colorless": (232, 230, 222),
    "trainer": (226, 226, 230),
    "energy": (240, 236, 222),
}


STYLES = {
    "base1": {
        "rim": (232, 198, 92), "trainer_rim": (204, 206, 216),
        "strip": (236, 206, 120), "strip_edge": (178, 140, 60), "strip_shine": (255, 245, 200),
        "scenery": None, "mark": None,
    },
    "base2": {
        "rim": (150, 164, 92), "trainer_rim": (178, 196, 170),
        "strip": (188, 214, 138), "strip_edge": (92, 128, 58), "strip_shine": (236, 250, 210),
        "scenery": "jungle", "mark": "leaf",
    },
}
DEFAULT_STYLE = "base1"


def style(set_name: str) -> dict:
    return STYLES.get(set_name, STYLES[DEFAULT_STYLE])


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _seed(name: str) -> int:
    return sum(map(ord, name)) * 31


def rgba(c, a=255):
    return (*c, a)


def card_mask(scale: int = 1) -> Image.Image:
    m = Image.new("L", (W * scale, H * scale), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W * scale - 1, H * scale - 1), radius=RADIUS * scale, fill=255)
    return m.resize((W, H), Image.LANCZOS) if scale > 1 else m


def type_symbol(kind: str, diameter: float) -> Image.Image:
    size = max(4, round(diameter))
    n = size * SS * 2
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    base = TYPE_COLORS[kind]
    d.ellipse((0, 0, n - 1, n - 1), fill=rgba(mix(base, (0, 0, 0), 0.5)))
    d.ellipse((n * 0.05, n * 0.05, n * 0.95, n * 0.95), fill=rgba(base))
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) / n
    dome = np.clip(1.0 - np.hypot(xx - 0.35, yy - 0.3) * 1.25, 0, 1)
    arr = np.asarray(img).astype(np.float32)
    inside = np.hypot(xx - 0.5, yy - 0.5) < 0.45
    arr[inside, :3] = np.clip(arr[inside, :3] * (0.78 + dome[inside, None] * 0.45), 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(img)
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
        d.ellipse((*P(-0.95, -0.55), *P(0.95, 0.55)), fill=g)
        d.ellipse((*P(-0.4, -0.4), *P(0.4, 0.4)), fill=rgba(mix(base, (0, 0, 0), 0.4)))
    elif kind == "fighting":
        d.rounded_rectangle((*P(-0.75, -0.55), *P(0.75, 0.75)), radius=s * 0.3, fill=g)
        for i in range(3):
            x = -0.5 + i * 0.5
            d.line([P(x, -0.55), P(x, 0.1)], fill=rgba(base), width=max(1, n // 22))
    else:
        pts = []
        for i in range(10):
            r = 0.95 if i % 2 == 0 else 0.4
            a = math.radians(-90 + i * 36)
            pts.append(P(r * math.cos(a), r * math.sin(a)))
        d.polygon(pts, fill=g)
    d.ellipse((n * 0.2, n * 0.14, n * 0.46, n * 0.3), fill=(255, 255, 255, 70))
    return img.resize((size, size), Image.LANCZOS)


def paste_symbol(img, kind, cx, cy, diameter):
    sym = type_symbol(kind, diameter)
    img.alpha_composite(sym, (round(cx - sym.width / 2), round(cy - sym.height / 2)))


def rarity_symbol(img, rarity, cx, cy, size=9):
    n = size * SS
    s = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = n / 2
    if rarity == "common":
        d.ellipse((c - n * 0.3, c - n * 0.3, c + n * 0.3, c + n * 0.3), fill=rgba(TEXT))
    elif rarity == "uncommon":
        d.polygon([(c, c - n * 0.4), (c + n * 0.4, c), (c, c + n * 0.4), (c - n * 0.4, c)], fill=rgba(TEXT))
    else:
        pts = []
        for i in range(10):
            r = n * (0.48 if i % 2 == 0 else 0.2)
            a = math.radians(-90 + i * 36)
            pts.append((c + r * math.cos(a), c + r * math.sin(a)))
        d.polygon(pts, fill=rgba(TEXT))
    img.alpha_composite(s.resize((size, size), Image.LANCZOS), (round(cx - size / 2), round(cy - size / 2)))


def _card_base(face_color, seed: int) -> Image.Image:
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.rounded_rectangle((0, 0, W * SS - 1, H * SS - 1), radius=RADIUS * SS, fill=rgba(YELLOW_DARK))
    d.rounded_rectangle((SS, SS, W * SS - 1 - SS, H * SS - 1 - SS), radius=(RADIUS - 1) * SS, fill=rgba(YELLOW))
    fx0, fy0, fx1, fy1 = [v * SS for v in FACE]
    d.rounded_rectangle((fx0 - SS, fy0 - SS, fx1 + SS, fy1 + SS), radius=5 * SS, fill=rgba(YELLOW_DARK))
    d.rounded_rectangle((fx0, fy0, fx1, fy1), radius=4 * SS, fill=rgba(face_color))
    img = big.resize((W, H), Image.LANCZOS)

    arr = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    on_face = (xx >= FACE[0]) & (xx <= FACE[2]) & (yy >= FACE[1]) & (yy <= FACE[3])
    border = ~on_face & (arr[..., 3] > 0)
    light = 1.06 - yy / H * 0.12
    arr[border, :3] = np.clip(arr[border, :3] * light[border, None], 0, 255)

    mottle = F.noise(W, H, 40, seed, 4)
    fine = F.noise(W, H, 4, seed + 1, 2)
    shade = 1.04 - (xx / W * 0.04 + yy / H * 0.08) + (mottle - 0.5) * 0.10 + (fine - 0.5) * 0.05
    arr[on_face, :3] = np.clip(arr[on_face, :3] * shade[on_face, None], 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "RGBA")

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(FACE, radius=4, outline=(255, 255, 255, 60))
    d.rounded_rectangle((FACE[0] - 2, FACE[1] - 2, FACE[2] + 2, FACE[3] + 2), radius=6, outline=rgba(YELLOW_LIGHT, 120))
    return img


def _art_frame(img, kind, set_name, silver=False):
    x0, y0, x1, y1 = ART
    rim = style(set_name)["trainer_rim" if silver else "rim"]
    dark = mix(rim, (40, 30, 20), 0.55)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((x0 - 5, y0 - 5, x1 + 5, y1 + 5), fill=rgba(mix(rim, (0, 0, 0), 0.4)))
    for i in range(4, 0, -1):
        t = i / 4
        d.rectangle((x0 - i, y0 - i, x1 + i, y1 + i), outline=rgba(mix(rim, (255, 255, 255), 0.35 * t) if i > 2 else mix(rim, dark, 0.3)))
    d.line((x0 - 4, y0 - 4, x1 + 4, y0 - 4), fill=(255, 255, 255, 120))
    d.line((x0 - 4, y0 - 4, x0 - 4, y1 + 4), fill=(255, 255, 255, 90))
    d.line((x0 - 4, y1 + 4, x1 + 4, y1 + 4), fill=(0, 0, 0, 70))
    d.line((x1 + 4, y0 - 4, x1 + 4, y1 + 4), fill=(0, 0, 0, 60))
    d.rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), outline=rgba(dark))
    img.alpha_composite(background(kind, set_name), (x0, y0))
    sh = Image.new("RGBA", (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(5):
        sd.rectangle((i, i, sh.width - 1 - i, sh.height - 1 - i), outline=(0, 0, 0, 46 - i * 9))
    img.alpha_composite(sh, (x0, y0))


def pokemon_frame(kind: str, set_name: str = DEFAULT_STYLE) -> Image.Image:
    face = FACE_COLORS[kind]
    look = style(set_name)
    img = _card_base(face, _seed(kind))
    _art_frame(img, kind, set_name)
    d = ImageDraw.Draw(img, "RGBA")

    sx0, sy0, sx1, sy1 = STRIP
    d.polygon([(sx0 + 4, sy0), (sx1 - 4, sy0), (sx1, (sy0 + sy1) / 2), (sx1 - 4, sy1), (sx0 + 4, sy1), (sx0, (sy0 + sy1) / 2)],
              fill=rgba(look["strip"]), outline=rgba(look["strip_edge"]))
    d.line((sx0 + 5, sy0 + 1, sx1 - 5, sy0 + 1), fill=rgba(look["strip_shine"], 160))
    if look["mark"]:
        set_mark(img, look["mark"], sx1 + 8, (sy0 + sy1) / 2, 13)

    line_col = rgba(mix(face, (0, 0, 0), 0.35))
    d.line((BODY[0] + 4, WRR[1] - 2, BODY[2] - 4, WRR[1] - 2), fill=line_col)
    cell = (WRR[2] - WRR[0]) / 3
    f = F.font("CondensedSemiBold", 7)
    for i, label in enumerate(("weakness", "resistance", "retreat cost")):
        F.draw(img, (WRR[0] + cell * i + cell / 2, WRR[1] - 0.5), label, f, mix(TEXT, face, 0.2), anchor="ma")

    d.rounded_rectangle(FLAVOR, radius=2, fill=rgba(mix(face, (255, 255, 255), 0.35), 150), outline=rgba(mix(face, (0, 0, 0), 0.25)))
    return F.grain(img, 4, seed=_seed(kind))


def trainer_frame(set_name: str = DEFAULT_STYLE) -> Image.Image:
    face = FACE_COLORS["trainer"]
    img = _card_base(face, 77)
    _art_frame(img, "trainer", set_name, silver=True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(RULES, radius=3, fill=(250, 250, 252, 255), outline=(150, 150, 160, 255))
    mark = style(set_name)["mark"]
    if mark:
        set_mark(img, mark, RULES[2] - 11, RULES[1] + 11, 13)
    return F.grain(img, 4, seed=77)


def energy_frame(set_name: str = DEFAULT_STYLE) -> Image.Image:
    img = _card_base(FACE_COLORS["energy"], 91)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((FACE[0] + 9, FACE[1] + 26, FACE[2] - 9, FACE[3] - 22), radius=3, outline=(200, 186, 140, 255))
    mark = style(set_name)["mark"]
    if mark:
        set_mark(img, mark, FACE[2] - 20, FACE[3] - 34, 13)
    return F.grain(img, 4, seed=91)


def _leaf(d, cx, cy, length, width, angle, fill, vein=None):
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(25):
        t = i / 24 * 2 - 1
        pts.append((t * length / 2, (1 - t * t) * width / 2))
    for i in range(25):
        t = 1 - i / 24 * 2
        pts.append((t * length / 2, -(1 - t * t) * width / 2))
    d.polygon([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], fill=fill)
    if vein:
        d.line((cx - length / 2 * ca, cy - length / 2 * sa, cx + length * 0.42 * ca, cy + length * 0.42 * sa), fill=vein, width=max(1, round(width / 6)))


def set_mark(img, mark: str, cx, cy, size):
    big = Image.new("RGBA", (round(size * SS), round(size * SS)), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    n = size * SS
    d.ellipse((0, 0, n - 1, n - 1), fill=(36, 34, 30, 255))
    d.ellipse((SS * 0.9, SS * 0.9, n - 1 - SS * 0.9, n - 1 - SS * 0.9), fill=(248, 246, 234, 255))
    if mark == "leaf":
        _leaf(d, n * 0.5, n * 0.52, n * 0.72, n * 0.36, -50, (34, 70, 38, 255), vein=(248, 246, 234, 255))
        d.line((n * 0.26, n * 0.8, n * 0.36, n * 0.68), fill=(34, 70, 38, 255), width=round(SS * 0.9))
    img.alpha_composite(big.resize((round(size), round(size)), Image.LANCZOS), (round(cx - size / 2), round(cy - size / 2)))


def _gradient(w, h, top, bottom, power=1.0):
    t = (np.arange(h, dtype=np.float32) / max(h - 1, 1)) ** power
    arr = np.zeros((h, w, 4), np.float32)
    for i in range(3):
        arr[..., i] = (top[i] + (bottom[i] - top[i]) * t)[:, None]
    arr[..., 3] = 255
    return arr


def _paint(arr, mask, colour, alpha=1.0):
    m = mask[..., None] * alpha
    arr[..., :3] = arr[..., :3] * (1 - m) + np.array(colour, np.float32) * m


def _ridge(w, horizon, height, seed, rough=0.5):
    n = F.noise(w, 1, w * 0.35, seed, 4)[0]
    r = F.noise(w, 1, w * 0.06, seed + 9, 3)[0]
    return horizon - height * (0.4 + 0.6 * n) - (r - 0.5) * height * rough


def _jungle(arr, w, h, seed):
    rng = random.Random(seed * 7 + 3)
    sky = arr[: int(h * 0.3), :, :3].mean() / 255
    dark = 0.55 + 0.45 * min(1.0, sky * 1.3)
    greens = [tuple(int(c * dark) for c in col) for col in ((30, 86, 44), (44, 112, 52), (62, 136, 60), (24, 70, 40))]
    layer = Image.new("RGBA", (w * SS // 2, h * SS // 2), (0, 0, 0, 0))
    k = SS / 2
    d = ImageDraw.Draw(layer)
    horizon = h * 0.64

    for _ in range(26):
        x = rng.uniform(-0.05, 1.05) * w
        r = rng.uniform(h * 0.06, h * 0.12)
        y = horizon - r * rng.uniform(0.2, 0.9)
        col = (*greens[rng.randrange(4)], 235)
        d.ellipse(((x - r * 1.2) * k, (y - r) * k, (x + r * 1.2) * k, (y + r) * k), fill=col)
    for side in (0, 1):
        bx = w * (0.04 if side == 0 else 0.96)
        top = (w * (0.16 if side == 0 else 0.84), h * 0.3)
        d.line((bx * k, horizon * k, top[0] * k, top[1] * k), fill=(int(110 * dark), int(84 * dark), int(56 * dark), 255), width=round(5 * k))
        for i in range(7):
            ang = -170 + i * 28 + rng.uniform(-6, 6)
            r = math.radians(ang)
            length = rng.uniform(h * 0.16, h * 0.22)
            _leaf(d, (top[0] + math.cos(r) * length * 0.5) * k, (top[1] + math.sin(r) * length * 0.5) * k,
                  length * k, length * 0.28 * k, ang, (*greens[(i + side) % 3], 255))
    for _ in range(70):
        u = rng.random()
        x = (u ** 1.8 * 0.45 if rng.random() < 0.5 else 1 - u ** 1.8 * 0.45) * w
        y = rng.uniform(-h * 0.06, h * 0.12) * (1.6 - abs(x / w - 0.5) * 2) + rng.uniform(0, h * 0.05) * (abs(x / w - 0.5) * 2)
        length = rng.uniform(h * 0.09, h * 0.17)
        _leaf(d, x * k, y * k, length * k, length * 0.38 * k, rng.uniform(40, 140), (*greens[rng.randrange(4)], 255),
              vein=(*tuple(int(c * 1.25) for c in greens[2]), 255))
    for x0 in (w * rng.uniform(0.08, 0.2), w * rng.uniform(0.8, 0.92), w * rng.uniform(0.3, 0.4)):
        length = rng.uniform(h * 0.22, h * 0.42)
        pts = [((x0 + math.sin(t / 8 * math.pi + seed) * 4) * k, (t / 16 * length) * k) for t in range(17)]
        d.line(pts, fill=(*greens[3], 255), width=round(2 * k))
        for j in range(2, 17, 3):
            px, py = pts[j]
            _leaf(d, px + 4 * k * (1 if j % 2 else -1), py, 9 * k, 4 * k, 30 if j % 2 else 150, (*greens[1], 255))
    for cx in (0, w):
        for i in range(9):
            ang = (-80 + i * 9) if cx == 0 else (-100 - i * 9)
            r = math.radians(ang)
            length = rng.uniform(h * 0.22, h * 0.32)
            _leaf(d, (cx + math.cos(r) * length * 0.5) * k, (h + math.sin(r) * length * 0.5) * k,
                  length * k, length * 0.2 * k, ang, (*greens[i % 3], 255), vein=(*greens[3], 255))

    leaves = layer.resize((w, h), Image.LANCZOS)
    light = np.clip((F.noise(w, h, w * 0.06, seed + 21, 3) - 0.6) * 3, 0, 1) * np.clip(1 - np.abs(np.arange(h)[:, None] / h - 0.45) * 2, 0, 1)
    _paint(arr, light, (255, 250, 210), 0.18)
    la = np.asarray(leaves).astype(np.float32)
    a = la[..., 3:] / 255
    arr[..., :3] = arr[..., :3] * (1 - a) + la[..., :3] * a


def background(kind: str, set_name: str = DEFAULT_STYLE) -> Image.Image:
    w, h = (ART[2] - ART[0] + 1) * 2, (ART[3] - ART[1] + 1) * 2
    seed = sum(map(ord, kind))
    rng = random.Random(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    horizon = h * 0.64
    clouds = F.noise(w, h, w * 0.25, seed, 5)
    tex = F.noise(w, h, 14, seed + 3, 4)

    def land(arr, top_col, height, s, rough=0.5, base=None):
        ridge = _ridge(w, base if base is not None else horizon, height, s, rough)
        mask = np.clip((yy - ridge[None, :]) / 2.0, 0, 1)
        shade = 0.9 + (tex - 0.5) * 0.25 + np.clip((yy - ridge[None, :]) / h, 0, 1) * -0.25
        col = np.array(top_col, np.float32)[None, None, :] * shade[..., None]
        arr[..., :3] = arr[..., :3] * (1 - mask[..., None]) + col * mask[..., None]

    def ground(arr, near, far):
        mask = np.clip((yy - horizon) / 2.0, 0, 1)
        t = np.clip((yy - horizon) / (h - horizon), 0, 1)
        col = np.array(far, np.float32) + (np.array(near, np.float32) - np.array(far, np.float32)) * t[..., None]
        col *= (0.88 + (tex - 0.5) * 0.4 + (F.noise(w, h, 5, seed + 7, 2) - 0.5) * 0.15)[..., None]
        arr[..., :3] = arr[..., :3] * (1 - mask[..., None]) + col * mask[..., None]

    def soft_clouds(arr, colour, amount=0.85, cover=0.52):
        c = np.clip((clouds - cover) * 4, 0, 1) * np.clip(1.2 - yy / horizon, 0, 1)
        _paint(arr, c, colour, amount)

    if kind == "fire":
        arr = _gradient(w, h, (252, 214, 140), (238, 120, 70), 0.9)
        soft_clouds(arr, (255, 236, 200), 0.5)
        land(arr, (150, 80, 66), h * 0.42, seed, 0.9)
        land(arr, (112, 52, 44), h * 0.22, seed + 1, 0.7)
        glow = np.exp(-(((xx - w * 0.78) / (w * 0.08)) ** 2 + ((yy - h * 0.2) / (h * 0.1)) ** 2))
        _paint(arr, glow, (255, 170, 60), 0.7)
        ground(arr, (140, 70, 46), (176, 96, 60))
    elif kind == "water":
        arr = _gradient(w, h, (150, 206, 248), (226, 242, 252), 1.2)
        soft_clouds(arr, (255, 255, 255))
        land(arr, (150, 186, 200), h * 0.12, seed, 0.3)
        sea = np.clip((yy - horizon) / 2.0, 0, 1)
        t = np.clip((yy - horizon) / (h - horizon), 0, 1)
        waves = np.sin(xx / w * 40 + F.noise(w, h, 20, seed + 4, 3) * 9 + yy * 0.25) * 0.5 + 0.5
        col = np.array((70, 140, 214), np.float32) * (1 - t[..., None]) * 1.05 + np.array((30, 90, 170), np.float32) * t[..., None]
        col = col * (0.9 + waves[..., None] * 0.18 * (0.3 + t[..., None]))
        arr[..., :3] = arr[..., :3] * (1 - sea[..., None]) + col * sea[..., None]
        sparkle = (waves > 0.97) & (sea > 0) & (tex > 0.55)
        arr[sparkle, :3] = 245
    elif kind == "grass":
        arr = _gradient(w, h, (150, 202, 244), (226, 242, 226), 1.1)
        soft_clouds(arr, (255, 255, 255))
        land(arr, (140, 184, 150), h * 0.22, seed, 0.5)
        land(arr, (98, 160, 88), h * 0.12, seed + 1, 0.8)
        for _ in range(9):
            cx, r = rng.uniform(0, w), rng.uniform(h * 0.07, h * 0.13)
            cy = horizon - r * 0.6
            blob = np.clip(1 - np.hypot((xx - cx) / r, (yy - cy) / (r * 1.1)) + (tex - 0.5) * 0.4, 0, 1) ** 0.3
            _paint(arr, np.clip(blob * 3, 0, 1), (56, 116, 60), 1)
        ground(arr, (84, 150, 62), (118, 176, 82))
        blades = (F.noise(w, h, 2, seed + 8, 1) > 0.72) & (yy > horizon + 4)
        arr[blades, :3] *= 0.8
    elif kind == "lightning":
        arr = _gradient(w, h, (40, 36, 80), (120, 108, 150), 1.0)
        soft_clouds(arr, (84, 78, 120), 0.9, 0.45)
        for x in (w * 0.18, w * 0.84):
            pts, y = [(x, 0)], 0.0
            while y < horizon - 20:
                y += rng.uniform(14, 30)
                pts.append((pts[-1][0] + rng.uniform(-18, 18), y))
            bolt = Image.new("L", (w, h), 0)
            ImageDraw.Draw(bolt).line(pts, fill=255, width=3)
            glow = np.asarray(bolt.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
            _paint(arr, np.clip(glow * 3, 0, 1), (200, 190, 255), 0.6)
            _paint(arr, np.asarray(bolt, np.float32) / 255, (255, 250, 200))
        land(arr, (70, 66, 86), h * 0.14, seed, 0.6)
        ground(arr, (70, 70, 82), (96, 94, 108))
    elif kind == "psychic":
        arr = _gradient(w, h, (70, 40, 120), (214, 150, 206), 1.0)
        soft_clouds(arr, (236, 190, 236), 0.4)
        stars = (F.noise(w, h, 1.5, seed + 2, 1) > 0.93) & (yy < horizon)
        arr[stars, :3] = 255
        for r in (0.18, 0.3, 0.42):
            ring = np.exp(-((np.hypot((xx - w / 2) / 2, yy - h * 0.36) - r * h) / 2.5) ** 2)
            _paint(arr, ring, (250, 210, 250), 0.35)
        land(arr, (120, 84, 150), h * 0.1, seed, 0.4)
        ground(arr, (110, 74, 136), (150, 108, 170))
    elif kind == "fighting":
        arr = _gradient(w, h, (248, 214, 160), (232, 172, 112), 1.0)
        soft_clouds(arr, (255, 236, 210), 0.6)
        land(arr, (184, 124, 86), h * 0.36, seed, 1.0)
        land(arr, (150, 92, 60), h * 0.2, seed + 1, 0.8)
        ground(arr, (160, 106, 66), (196, 140, 92))
    elif kind == "trainer":
        arr = _gradient(w, h, (238, 238, 244), (196, 204, 222), 1.0)
        stripes = (np.sin((xx + yy * 0.6) / 10) > 0.6)
        arr[stripes, :3] *= 1.04
        _paint(arr, np.exp(-((xx - w / 2) / (w * 0.4)) ** 2 - ((yy - h * 0.45) / (h * 0.45)) ** 2), (255, 255, 255), 0.6)
    else:
        arr = _gradient(w, h, (130, 190, 246), (220, 238, 252), 1.2)
        soft_clouds(arr, (255, 255, 255), 0.95, 0.48)
        land(arr, (150, 190, 170), h * 0.16, seed, 0.5)
        ground(arr, (132, 184, 96), (166, 204, 122))

    if style(set_name)["scenery"] == "jungle" and kind != "trainer":
        _jungle(arr, w, h, seed)

    v = np.hypot((xx - w / 2) / (w * 0.7), (yy - h / 2) / (h * 0.7))
    arr[..., :3] *= np.clip(1.08 - v * 0.22, 0.75, 1.05)[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    return img.resize((ART[2] - ART[0] + 1, ART[3] - ART[1] + 1), Image.LANCZOS)


def holo_overlay(frames: int = 8):
    w, h = ART[2] - ART[0] + 1, ART[3] - ART[1] + 1
    strip = np.zeros((h * frames, w, 4), np.uint8)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (xx + yy * 1.3) / (w + h * 1.3)
    swirl = np.sin(np.hypot(xx - w * 0.5, yy - h * 0.55) / 7 + np.arctan2(yy - h * 0.55, xx - w * 0.5) * 3) * 0.5 + 0.5
    rng = np.random.default_rng(7)
    star_x, star_y = rng.uniform(0, w, 90), rng.uniform(0, h, 90)
    star_r, star_p = rng.uniform(0.8, 2.2, 90), rng.uniform(0, 1, 90)
    for f in range(frames):
        phase = f / frames
        hue = (d * 1.4 + swirl * 0.15 - phase) % 1.0
        r = 0.5 + 0.5 * np.cos((hue + 0.0) * 2 * np.pi)
        g = 0.5 + 0.5 * np.cos((hue + 0.33) * 2 * np.pi)
        b = 0.5 + 0.5 * np.cos((hue + 0.66) * 2 * np.pi)
        band = np.clip(np.cos((d - phase) * 2 * np.pi), 0, 1) ** 3
        rgb = np.stack([r, g, b], -1) * 0.5 + 0.5
        alpha = 70 + 110 * band + swirl * 25
        tile = np.zeros((h, w, 4), np.float32)
        tile[..., :3] = np.clip(rgb * (0.85 + 0.3 * band[..., None]), 0, 1) * 255
        tile[..., 3] = alpha
        for x, y, rad, p in zip(star_x, star_y, star_r, star_p):
            tw = max(0.0, math.sin((phase + p) * 2 * math.pi))
            if tw < 0.2:
                continue
            size = rad * (1 + tw * 2.2)
            dist = np.abs(xx - x) * np.abs(yy - y)
            core = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (size * 0.8) ** 2)
            cross = np.exp(-dist / (size * 0.35)) * np.exp(-np.hypot(xx - x, yy - y) / (size * 2.5))
            s = np.clip((core + cross) * tw, 0, 1)
            tile[..., :3] = tile[..., :3] * (1 - s[..., None]) + 255 * s[..., None]
            tile[..., 3] = np.maximum(tile[..., 3], s * 255)
        strip[f * h:(f + 1) * h] = np.clip(tile, 0, 255).astype(np.uint8)
    return Image.fromarray(strip, "RGBA"), {"animation": {"frametime": 3, "interpolate": True, "width": w, "height": h}}
