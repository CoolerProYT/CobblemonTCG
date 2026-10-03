"""
Booster pack wrappers in the spirit of the 1999 Base Set packs (original drawing, no official
logo): a tall foil pack with crimped silver seals, a big mascot illustration and the set name,
plus the back of the pack (seam, blurb, barcode) and the card back.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import finish as F
from . import layout as L
from .canvas import Sprite
from .pokemon_base1 import DRAW as POKEMON

PACK_W, PACK_H = 240, 368          # whole texture is the pack
SS = 4
SEAL = 26                          # height of the crimped seals
TOOTH = 6                          # zig-zag width at the crimped edge

# wrapper name -> (mascot card number, background type, top colour, bottom colour, accent)
WRAPPERS = {
    "charizard": (4, "fire", (34, 38, 104), (196, 66, 34), (255, 170, 60)),
    "blastoise": (2, "water", (20, 44, 112), (36, 118, 204), (130, 210, 255)),
    "venusaur": (15, "grass", (18, 64, 60), (64, 150, 84), (190, 240, 140)),
}
BACK = ((26, 34, 96), (40, 70, 150), (250, 214, 64))


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _pack_mask() -> Image.Image:
    """Pack silhouette: zig-zag edges where the seals are crimped, slightly pinched seals."""
    w, h = PACK_W * SS, PACK_H * SS
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    tooth = TOOTH * SS
    pinch = 3 * SS
    top = [(x, (tooth * 0.5 if (i % 2) else 0)) for i, x in enumerate(range(pinch, w - pinch + 1, tooth))]
    bottom = [(x, h - 1 - (tooth * 0.5 if (i % 2) else 0)) for i, x in enumerate(range(w - pinch, pinch - 1, -tooth))]
    seal = SEAL * SS
    d.polygon(top + [(w - pinch, seal), (w - 1, seal + 2 * SS), (w - 1, h - seal - 2 * SS), (w - pinch, h - seal)] + bottom
              + [(pinch, h - seal), (0, h - seal - 2 * SS), (0, seal + 2 * SS), (pinch, seal)], fill=255)
    return mask.resize((PACK_W, PACK_H), Image.LANCZOS)


def _foil(top_col, bottom_col, seed) -> Image.Image:
    """Metallic body: colour gradient, crinkles, a soft pillow shape and diagonal reflections."""
    w, h = PACK_W, PACK_H
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (yy / h) ** 1.3
    arr = np.zeros((h, w, 4), np.float32)
    for i in range(3):
        arr[..., i] = top_col[i] + (bottom_col[i] - top_col[i]) * t
    arr[..., 3] = 255
    # pillow: the filled pack bulges, darker towards the side edges
    bulge = 1 - ((xx / w - 0.5) * 2) ** 4 * 0.35
    crinkle = F.noise(w, h, 18, seed, 4)
    fine = F.noise(w, h, 3, seed + 1, 2)
    arr[..., :3] *= (bulge * (0.9 + (crinkle - 0.5) * 0.35 + (fine - 0.5) * 0.08))[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return img


def _sheen(img: Image.Image, seed: int) -> Image.Image:
    """Diagonal bands of reflected light with crinkly edges, like light on a foil wrapper."""
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    crinkle = F.noise(w, h, 22, seed + 5, 4)
    d = (xx * 0.9 - yy * 0.45) / w + (crinkle - 0.5) * 0.05
    band = np.clip(np.cos((d - 0.05) * 2 * np.pi * 1.3), 0, 1) ** 24 * 0.32 + np.clip(np.cos((d + 0.3) * 2 * np.pi * 2.4), 0, 1) ** 30 * 0.16
    arr = np.asarray(img).astype(np.float32)
    arr[..., :3] = arr[..., :3] + (255 - arr[..., :3]) * band[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def _seals(img: Image.Image, seed: int):
    """Crimped silver seals at the top and bottom: vertical ridges with a metallic gradient."""
    w, h = img.size
    arr = np.asarray(img).astype(np.float32)
    xx = np.arange(w, dtype=np.float32)
    ridges = 0.82 + 0.18 * np.cos(xx / 2.2 * np.pi)
    crinkle = F.noise(w, h, 10, seed + 3, 3)
    for y0, y1 in ((0, SEAL), (h - SEAL, h)):
        for y in range(y0, y1):
            t = (y - y0) / SEAL
            base = 196 + 40 * math.cos(t * math.pi * 2 + 0.6)
            row = base * ridges * (0.9 + (crinkle[y] - 0.5) * 0.3)
            arr[y, :, 0] = row * 0.97
            arr[y, :, 1] = row * 0.98
            arr[y, :, 2] = row * 1.04
    img2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(img2, "RGBA")
    d.line((0, SEAL, w, SEAL), fill=(60, 60, 76, 200), width=2)
    d.line((0, SEAL + 2, w, SEAL + 2), fill=(255, 255, 255, 50), width=1)
    d.line((0, h - SEAL - 1, w, h - SEAL - 1), fill=(60, 60, 76, 200), width=2)
    return img2


def _finish(img: Image.Image) -> Image.Image:
    """Cut to the pack silhouette and add a thin dark edge."""
    mask = _pack_mask()
    edge = Image.new("RGBA", img.size, (24, 22, 34, 255))
    edge.putalpha(mask)
    inner = mask.filter(ImageFilter.MinFilter(3))
    body = F.clip_to(img, inner)
    edge.alpha_composite(body)
    return F.grain(edge, 3)


def make_wrapper(name: str) -> Image.Image:
    number, kind, top_col, bottom_col, accent = WRAPPERS[name]
    w, h = PACK_W, PACK_H
    seed = sum(map(ord, name))
    img = _foil(top_col, bottom_col, seed)

    # light burst behind the mascot
    burst = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    cx, cy = w / 2 * SS, 196 * SS
    for i in range(24):
        a0, a1 = math.radians(i * 15), math.radians(i * 15 + 6)
        r = 330 * SS
        bd.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=(*accent, 40))
    burst = burst.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(burst)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((w / 2 - 90, 120, w / 2 + 90, 280), fill=(*accent, 110))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(28)))

    # the mascot, much bigger than on the card, bursting out of the frame
    sprite = Sprite(300, 200)
    POKEMON[number](sprite)
    mascot = sprite.render()
    img.alpha_composite(mascot, (int(w / 2 - 150), 104))

    # set name plate
    plate = (22, SEAL + 12, w - 22, SEAL + 64)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((plate[0] - 2, plate[1] - 2, plate[2] + 2, plate[3] + 2), radius=10, fill=(250, 214, 80, 255))
    d.rounded_rectangle(plate, radius=8, fill=(16, 20, 58, 235))
    F.draw(img, (w / 2, plate[1] + 6), "BASE SET", F.font("Bold", 30), (252, 214, 64), anchor="ma", stroke=2, stroke_color=(28, 50, 150))
    F.draw(img, (w / 2, plate[1] + 40), "TRADING CARD GAME", F.font("CondensedBold", 10), (255, 255, 255), anchor="ma")

    # "11 cards" badge and booster banner at the bottom
    by = h - SEAL - 44
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((14, by - 2, 58, by + 42), fill=(250, 214, 64, 255), outline=(28, 46, 130, 255), width=3)
    F.draw(img, (36, by + 5), "11", F.font("Bold", 20), (28, 40, 100), anchor="ma")
    F.draw(img, (36, by + 27), "CARDS", F.font("CondensedBold", 7), (28, 40, 100), anchor="ma")
    d.rounded_rectangle((66, by + 10, w - 16, by + 32), radius=4, fill=(250, 250, 255, 230), outline=(28, 46, 130, 255), width=2)
    F.draw(img, ((66 + w - 16) / 2, by + 21), "BOOSTER PACK", F.font("Bold", 12), (200, 36, 40), anchor="mm")

    img = _sheen(img, seed)
    img = _seals(img, seed)
    return _finish(img)


def make_pack_back() -> Image.Image:
    """Back of every pack: vertical glued seam, a short blurb and a barcode panel."""
    top_col, bottom_col, accent = BACK
    w, h = PACK_W, PACK_H
    img = _foil(top_col, bottom_col, 404)

    # the glued fin seam down the middle
    d = ImageDraw.Draw(img, "RGBA")
    sx = w / 2
    d.rectangle((sx - 9, SEAL, sx + 9, h - SEAL), fill=(*mix(bottom_col, (0, 0, 0), 0.2), 255))
    for x in range(int(sx - 8), int(sx + 9), 3):
        d.line((x, SEAL, x, h - SEAL), fill=(255, 255, 255, 30))
    d.line((sx - 10, SEAL, sx - 10, h - SEAL), fill=(0, 0, 0, 120), width=2)
    d.line((sx + 10, SEAL, sx + 10, h - SEAL), fill=(255, 255, 255, 60), width=1)

    # blurb panel on the left half
    panel = (16, SEAL + 22, int(sx) - 16, SEAL + 196)
    d.rounded_rectangle(panel, radius=6, fill=(12, 16, 50, 190), outline=(*accent, 255), width=2)
    F.draw(img, ((panel[0] + panel[2]) / 2, panel[1] + 8), "BASE SET", F.font("Bold", 14), accent, anchor="ma")
    F.paragraph(img, (panel[0] + 8, panel[1] + 30, panel[2] - 8, panel[3] - 8),
                "Each pack holds 11 cards: 1 rare, 3 uncommons and 7 commons. About 1 pack in 3 has a "
                "holo rare instead! Collect all 102 cards of the Base Set.",
                "Regular", 8, (236, 236, 250), L.paste_symbol)

    # right half: card fan and barcode
    for i, kind in enumerate(("grass", "water", "fire")):
        c = Image.new("RGBA", (34, 47), (0, 0, 0, 0))
        cd = ImageDraw.Draw(c)
        cd.rounded_rectangle((0, 0, 33, 46), radius=3, fill=(246, 212, 70, 255))
        cd.rounded_rectangle((2, 2, 31, 44), radius=2, fill=(*L.FACE_COLORS[kind], 255))
        cd.rectangle((5, 8, 28, 24), fill=(*L.TYPE_COLORS[kind], 255))
        c = c.rotate(18 - i * 18, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(c, (int(sx) + 18 + i * 22, SEAL + 40 + abs(i - 1) * 6))
    bx0, by0 = int(sx) + 22, h - SEAL - 74
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((bx0 - 4, by0 - 4, w - 18, by0 + 46), fill=(250, 250, 250, 255))
    rng = np.random.default_rng(11)
    x = bx0
    while x < w - 24:
        bw = int(rng.integers(1, 3))
        d.rectangle((x, by0, x + bw - 1, by0 + 32), fill=(20, 20, 20, 255))
        x += bw + int(rng.integers(1, 3))
    F.draw(img, ((bx0 + w - 18) / 2, by0 + 35), "0 12345 67890 5", F.font("Regular", 7), (20, 20, 20), anchor="ma")
    F.draw(img, (w / 4, h - SEAL - 20), "Fan-made pack for Cobblemon: TCG", F.font("Italic", 7), (210, 214, 240), anchor="ma")

    img = _sheen(img, 404)
    img = _seals(img, 404)
    return _finish(img)


def make_card_back() -> Image.Image:
    """Original card back (not the official one): a blue swirl with a gold emblem."""
    w, h = L.W, L.H
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    ang = np.arctan2(yy - cy, xx - cx)
    rad = np.hypot(xx - cx, (yy - cy) * 0.8)
    swirl = np.sin(ang * 3 + rad / 16 + F.noise(w, h, 40, 5, 3) * 3) * 0.5 + 0.5
    t = np.clip(rad / (w * 0.75), 0, 1)
    arr = np.zeros((h, w, 4), np.float32)
    deep, mid, light = np.array((14, 26, 92)), np.array((34, 74, 176)), np.array((90, 150, 230))
    base = mid * (1 - t[..., None]) + deep * t[..., None]
    arr[..., :3] = base * (0.82 + swirl[..., None] * 0.3) + light * (np.exp(-(rad / 70) ** 2) * 0.35)[..., None]
    arr[..., 3] = 255
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

    # darker blue border, like the border on the back of real cards
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=L.RADIUS, outline=(18, 34, 110, 255), width=12)
    d.rounded_rectangle((11, 11, w - 12, h - 12), radius=5, outline=(120, 170, 240, 160), width=1)

    # emblem: gold ring, a ring of stars and the name
    ring = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    r = 62 * SS
    c = (w / 2 * SS, h / 2 * SS)
    rd.ellipse((c[0] - r - 6 * SS, c[1] - r - 6 * SS, c[0] + r + 6 * SS, c[1] + r + 6 * SS), fill=(150, 104, 30, 255))
    rd.ellipse((c[0] - r - 4 * SS, c[1] - r - 4 * SS, c[0] + r + 4 * SS, c[1] + r + 4 * SS), fill=(246, 206, 80, 255))
    rd.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(22, 42, 130, 255))
    rd.ellipse((c[0] - r * 0.86, c[1] - r * 0.86, c[0] + r * 0.86, c[1] + r * 0.86), outline=(246, 206, 80, 255), width=SS)
    for i in range(4):
        a = math.radians(i * 90)
        sx, sy = c[0] + math.cos(a) * r * 0.86, c[1] + math.sin(a) * r * 0.86
        q = 5 * SS
        rd.polygon([(sx, sy - q), (sx + q, sy), (sx, sy + q), (sx - q, sy)], fill=(250, 220, 110, 255), outline=(150, 104, 30, 255))
    img.alpha_composite(ring.resize((w, h), Image.LANCZOS))
    F.draw(img, (w / 2, h / 2 - 12), "COBBLEMON", F.font("Bold", 18), (252, 214, 64), anchor="mm", stroke=2, stroke_color=(28, 50, 150))
    F.draw(img, (w / 2, h / 2 + 12), "TRADING CARD GAME", F.font("CondensedBold", 9), (236, 240, 255), anchor="mm")

    # gloss
    gloss = np.clip(np.cos(((xx - yy * 0.6) / w - 0.15) * np.pi * 1.6), 0, 1) ** 6 * 0.12
    arr = np.asarray(img).astype(np.float32)
    arr[..., :3] = arr[..., :3] + (255 - arr[..., :3]) * gloss[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return F.grain(F.clip_to(img, L.card_mask(4)), 4, seed=3)
