"""
Booster pack wrappers in the spirit of the 1999 Base Set packs: a tall foil pack with crimped
silver seals, a big mascot illustration and the set name. Original drawing, no official logo.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .canvas import Sprite
from .pokemon_base1 import DRAW as POKEMON

SIZE = 128
SS = 4
BODY = (26, 3, 101, 124)          # pack outline inside the 128x128 texture
SEAL = 11                         # height of the crimped seals

# wrapper name -> (mascot card number, top colour, bottom colour, accent)
WRAPPERS = {
    "charizard": (4, (40, 46, 120), (190, 70, 40), (255, 170, 60)),
    "blastoise": (2, (28, 52, 120), (40, 120, 200), (130, 210, 255)),
    "venusaur": (15, (24, 70, 70), (70, 150, 90), (190, 240, 140)),
}


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _font(size):
    return ImageFont.load_default(size=size)


def _pack_mask() -> Image.Image:
    """Pack silhouette: a tall rectangle with zig-zag edges at the crimped top and bottom."""
    x0, y0, x1, y1 = [v * SS for v in BODY]
    mask = Image.new("L", (SIZE * SS, SIZE * SS), 0)
    d = ImageDraw.Draw(mask)
    tooth = 3 * SS
    top = [(x, y0 + (0 if (i % 2) else tooth * 0.6)) for i, x in enumerate(range(x0, x1 + 1, tooth))]
    bottom = [(x, y1 - (0 if (i % 2) else tooth * 0.6)) for i, x in enumerate(range(x1, x0 - 1, -tooth))]
    d.polygon(top + [(x1, y0 + tooth), (x1, y1 - tooth)] + bottom + [(x0, y1 - tooth), (x0, y0 + tooth)], fill=255)
    return mask


def make_wrapper(name: str) -> Image.Image:
    number, top_col, bottom_col, accent = WRAPPERS[name]
    W = SIZE * SS
    x0, y0, x1, y1 = [v * SS for v in BODY]
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))

    # body gradient
    arr = np.zeros((W, W, 4), np.uint8)
    for y in range(y0, y1 + 1):
        t = (y - y0) / (y1 - y0)
        arr[y, x0:x1 + 1, :3] = mix(top_col, bottom_col, t ** 1.4)
        arr[y, x0:x1 + 1, 3] = 255
    img = Image.fromarray(arr, "RGBA")
    d = ImageDraw.Draw(img, "RGBA")

    # light burst behind the mascot
    cx, cy = (x0 + x1) / 2, 74 * SS
    for i in range(18):
        a0 = math.radians(i * 20)
        a1 = math.radians(i * 20 + 9)
        r = 90 * SS
        d.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=(*accent, 46))
    d.ellipse((cx - 30 * SS, cy - 26 * SS, cx + 30 * SS, cy + 26 * SS), fill=(*accent, 70))

    # mascot, larger than the card art and clipped by the pack
    sprite = Sprite(132, 82)
    POKEMON[number](sprite)
    mascot = sprite.render().resize((132 * SS, 82 * SS), Image.LANCZOS)
    img.alpha_composite(mascot, (int(cx - 66 * SS), int(cy - 46 * SS)))

    # header banner with the set name
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((x0 + 5 * SS, 16 * SS, x1 - 5 * SS, 38 * SS), radius=4 * SS, fill=(18, 22, 60, 220), outline=(250, 214, 80, 255), width=SS)
    d.text(((x0 + x1) / 2, 18 * SS), "BASE SET", font=_font(11 * SS), fill=(252, 214, 64, 255), anchor="ma",
           stroke_width=int(1.2 * SS), stroke_fill=(30, 50, 140, 255))
    d.text(((x0 + x1) / 2, 30 * SS), "BOOSTER PACK", font=_font(6 * SS), fill=(255, 255, 255, 255), anchor="ma")

    # "11 cards" badge and an emblem star at the bottom
    d.ellipse((x0 + 4 * SS, 96 * SS, x0 + 20 * SS, 112 * SS), fill=(250, 214, 64, 255), outline=(30, 50, 140, 255), width=SS)
    d.text((x0 + 12 * SS, 98 * SS), "11", font=_font(7 * SS), fill=(30, 40, 100, 255), anchor="ma")
    d.text((x0 + 12 * SS, 105 * SS), "CARDS", font=_font(3 * SS), fill=(30, 40, 100, 255), anchor="ma")
    sx, sy, r = x1 - 12 * SS, 104 * SS, 7 * SS
    pts = [(sx + (r if i % 2 == 0 else r * 0.42) * math.cos(math.radians(-90 + i * 36)),
            sy + (r if i % 2 == 0 else r * 0.42) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
    d.polygon(pts, fill=(255, 236, 140, 255), outline=(150, 100, 30, 255))

    # foil sheen: diagonal streaks
    sheen = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheen)
    for off, w, a in ((-40, 14, 40), (10, 6, 30), (60, 20, 26)):
        o = off * SS
        sd.polygon([(x0 + o, y1), (x0 + o + w * SS, y1), (x1 + o + w * SS - 60 * SS, y0), (x1 + o - 60 * SS, y0)], fill=(255, 255, 255, a))
    img.alpha_composite(sheen)

    # crimped silver seals
    d = ImageDraw.Draw(img, "RGBA")
    for sy0, sy1 in ((y0, y0 + SEAL * SS), (y1 - SEAL * SS, y1)):
        d.rectangle((x0, sy0, x1, sy1), fill=(196, 198, 210, 255))
        for x in range(x0, x1, 2 * SS):
            d.rectangle((x, sy0, x + SS - 1, sy1), fill=(150, 152, 168, 255))
        d.line((x0, sy1 if sy0 == y0 else sy0, x1, sy1 if sy0 == y0 else sy0), fill=(110, 110, 126, 255), width=SS)

    # side edges: dark rim and a highlight
    d.line((x0 + SS, y0 + SEAL * SS, x0 + SS, y1 - SEAL * SS), fill=(10, 10, 30, 160), width=2 * SS)
    d.line((x1 - SS, y0 + SEAL * SS, x1 - SS, y1 - SEAL * SS), fill=(10, 10, 30, 160), width=2 * SS)
    d.line((x0 + 5 * SS, y0 + SEAL * SS + 4 * SS, x0 + 5 * SS, y1 - SEAL * SS - 30 * SS), fill=(255, 255, 255, 70), width=SS)

    # cut to the pack shape, add a thin outline, downscale
    mask = _pack_mask()
    img.putalpha(Image.composite(img.getchannel("A"), Image.new("L", mask.size, 0), mask))
    outline = mask.filter(ImageFilter.MaxFilter(2 * SS + 1))
    rim = Image.new("RGBA", (W, W), (24, 22, 34, 255))
    rim.putalpha(outline)
    rim.alpha_composite(img)
    return rim.resize((SIZE, SIZE), Image.LANCZOS)


def make_card_back() -> Image.Image:
    """Original card back (not the official one): teal with a gold diamond emblem."""
    W = SIZE * SS
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx0, cx1 = 18 * SS, 109 * SS
    d.rounded_rectangle((cx0, 0, cx1, W - 1), radius=6 * SS, fill=(222, 216, 198, 255))
    inner = (cx0 + 4 * SS, 4 * SS, cx1 - 4 * SS, W - 4 * SS - 1)
    d.rounded_rectangle(inner, radius=3 * SS, fill=(24, 86, 84, 255))
    stripes = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripes)
    for i in range(-W, W, 6 * SS):
        sd.line((cx0 + i, 0, cx0 + i + W, W), fill=(34, 104, 100, 255), width=SS)
    clip = Image.new("L", (W, W), 0)
    ImageDraw.Draw(clip).rounded_rectangle(inner, radius=3 * SS, fill=255)
    stripes.putalpha(Image.composite(stripes.getchannel("A"), Image.new("L", (W, W), 0), clip))
    img.alpha_composite(stripes)
    d = ImageDraw.Draw(img)
    mx, my = W / 2, W / 2
    d.polygon([(mx, my - 34 * SS), (mx + 26 * SS, my), (mx, my + 34 * SS), (mx - 26 * SS, my)], fill=(232, 196, 90, 255), outline=(120, 80, 30, 255), width=SS)
    d.polygon([(mx, my - 22 * SS), (mx + 16 * SS, my), (mx, my + 22 * SS), (mx - 16 * SS, my)], fill=(24, 86, 84, 255))
    d.ellipse((mx - 7 * SS, my - 7 * SS, mx + 7 * SS, my + 7 * SS), fill=(250, 226, 140, 255))
    return img.resize((SIZE, SIZE), Image.LANCZOS)
