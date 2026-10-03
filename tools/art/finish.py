"""
Shared helpers that make the textures look printed rather than drawn: value noise, card stock
grain, fonts and text layout with inline energy symbols.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = Path(__file__).resolve().parent.parent / "fonts"


# ---------------------------------------------------------------- noise

def noise(w: int, h: int, scale: float, seed: int, octaves: int = 4) -> np.ndarray:
    """Smooth fractal value noise in 0..1, `scale` is the size of the largest blobs in pixels."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        cell = max(scale / (2 ** o), 1.0)
        gw, gh = max(int(w / cell) + 2, 2), max(int(h / cell) + 2, 2)
        grid = Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8), "L")
        layer = grid.resize((int(gw * cell), int(gh * cell)), Image.BICUBIC).crop((0, 0, w, h))
        out += np.asarray(layer, np.float32) / 255 * amp
        total += amp
        amp *= 0.5
    return out / total


def grain(img: Image.Image, strength: float = 6.0, seed: int = 0) -> Image.Image:
    """Fine print grain on every visible pixel."""
    arr = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(seed)
    n = (rng.random(arr.shape[:2]) - 0.5) * 2 * strength
    arr[..., :3] = np.clip(arr[..., :3] + n[..., None], 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def tint(img: Image.Image, field: np.ndarray, amount: float) -> Image.Image:
    """Brightens / darkens by a 0..1 field around 0.5 (mottled paint, foil wrinkles)."""
    arr = np.asarray(img).astype(np.float32)
    f = (field - 0.5)[..., None] * 2 * amount
    rgb = arr[..., :3]
    arr[..., :3] = np.clip(np.where(f > 0, rgb + (255 - rgb) * f, rgb * (1 + f)), 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def clip_to(img: Image.Image, mask: Image.Image) -> Image.Image:
    out = img.copy()
    out.putalpha(Image.composite(img.getchannel("A"), Image.new("L", img.size, 0), mask))
    return out


# ---------------------------------------------------------------- text

@lru_cache(maxsize=None)
def font(name: str, size: float) -> ImageFont.FreeTypeFont:
    """Cabin (SIL Open Font License, tools/fonts/OFL.txt): Regular, Bold, Italic, CondensedBold, CondensedSemiBold."""
    return ImageFont.truetype(str(FONTS / f"Cabin-{name}.ttf"), size)


def fit(name: str, size: float, s: str, max_width: float, min_size: float = 6) -> ImageFont.FreeTypeFont:
    while size > min_size and length(s, font(name, size)) > max_width:
        size -= 0.5
    return font(name, size)


TEXT_SS = 4


def draw(img: Image.Image, xy, s: str, f: ImageFont.FreeTypeFont, color, anchor="la", stroke=0, stroke_color=None):
    """Draws text supersampled 4x and scaled down, so small sizes keep even spacing and soft edges."""
    if not s:
        return
    if "♂" in s or "♀" in s:
        _draw_gender(img, xy, s, f, color, anchor)
        return
    big = font_like(f, TEXT_SS)
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    bbox = probe.textbbox((0, 0), s, font=big, anchor=anchor, stroke_width=stroke * TEXT_SS)
    pad = 2 * TEXT_SS
    ox = xy[0] * TEXT_SS
    oy = xy[1] * TEXT_SS
    # align the temporary canvas to the output pixel grid so nothing shifts when scaling down
    x0 = int(np.floor((ox + bbox[0] - pad) / TEXT_SS)) * TEXT_SS
    y0 = int(np.floor((oy + bbox[1] - pad) / TEXT_SS)) * TEXT_SS
    x1 = int(np.ceil((ox + bbox[2] + pad) / TEXT_SS)) * TEXT_SS
    y1 = int(np.ceil((oy + bbox[3] + pad) / TEXT_SS)) * TEXT_SS
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (*color, 0))
    ImageDraw.Draw(layer).text((ox - x0, oy - y0), s, font=big, fill=(*color, 255), anchor=anchor,
                               stroke_width=stroke * TEXT_SS, stroke_fill=(*(stroke_color or color), 255))
    small = layer.resize((layer.width // TEXT_SS, layer.height // TEXT_SS), Image.LANCZOS)
    img.alpha_composite(small, (x0 // TEXT_SS, y0 // TEXT_SS))


def _draw_gender(img, xy, s, f, color, anchor):
    """Cabin has no male / female signs: draw the text before the sign, then the sign by hand."""
    sign = "♂" if "♂" in s else "♀"
    before, after = s.split(sign, 1)
    size = f.size
    sign_w = size * 0.62
    total = length(before, f) + sign_w + length(after, f)
    x = xy[0] - (total / 2 if anchor[0] == "m" else total if anchor[0] == "r" else 0)
    draw(img, (x, xy[1]), before, f, color, anchor="l" + anchor[1])
    # vertical centre of lowercase letters relative to the anchor's baseline / middle / top
    ascent, descent = f.getmetrics()
    base_y = {"s": xy[1], "m": xy[1] + (ascent - descent) / 2, "a": xy[1] + ascent, "t": xy[1] + ascent}.get(anchor[1], xy[1] + ascent)
    sx = x + length(before, f) + sign_w * 0.5
    sy = base_y - size * 0.36
    k = TEXT_SS
    layer = Image.new("RGBA", (img.width * k, img.height * k), (*color, 0))
    d = ImageDraw.Draw(layer)
    r = size * 0.2 * k
    lw = max(1, round(size * 0.1 * k))
    cx, cy = sx * k, sy * k
    if sign == "♂":
        cx -= r * 0.3
        cy += r * 0.3
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*color, 255), width=lw)
        tip = (cx + r * 2.0, cy - r * 2.0)
        d.line((cx + r * 0.7, cy - r * 0.7, *tip), fill=(*color, 255), width=lw)
        d.line((tip[0] - r * 0.9, tip[1], *tip, tip[0], tip[1] + r * 0.9), fill=(*color, 255), width=lw)
    else:
        cy -= r * 0.5
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*color, 255), width=lw)
        d.line((cx, cy + r, cx, cy + r * 2.4), fill=(*color, 255), width=lw)
        d.line((cx - r * 0.7, cy + r * 1.7, cx + r * 0.7, cy + r * 1.7), fill=(*color, 255), width=lw)
    img.alpha_composite(layer.resize(img.size, Image.LANCZOS))
    if after:
        draw(img, (x + length(before, f) + sign_w, xy[1]), after, f, color, anchor="l" + anchor[1])


def font_like(f: ImageFont.FreeTypeFont, scale: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f.path, f.size * scale)


def length(s: str, f: ImageFont.FreeTypeFont) -> float:
    """Text width measured at 4x, so it matches what draw() produces."""
    return ImageDraw.Draw(Image.new("L", (1, 1))).textlength(s, font=font_like(f, TEXT_SS)) / TEXT_SS


ENERGY_WORDS = ("Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting", "Colorless")


def tokens(s: str):
    """Splits rules text into words; '{fire}' style tokens become energy symbols."""
    out = []
    for word in s.replace("\n", " \n ").split(" "):
        if not word:
            continue
        if word.startswith("{") and "}" in word:
            out.append(("sym", word[1:word.index("}")], word[word.index("}") + 1:]))
        else:
            out.append(("word", word, ""))
    return out


def wrap(s: str, f: ImageFont.FreeTypeFont, width: float, sym: float):
    """Greedy word wrap; returns lines of tokens."""
    space = length(" ", f)
    lines, line, x = [], [], 0.0
    for tok in tokens(s):
        if tok[1] == "\n":
            lines.append(line)
            line, x = [], 0.0
            continue
        w = sym + length(tok[2], f) if tok[0] == "sym" else length(tok[1], f)
        if line and x + space + w > width:
            lines.append(line)
            line, x = [], 0.0
        line.append((tok, w))
        x += (space if len(line) > 1 else 0) + w
    if line:
        lines.append(line)
    return lines


def paragraph(img, box, s: str, name: str, size: float, color, symbol_fn, leading=1.12, min_size=5.5, draw_it=True):
    """Draws wrapped text into box (x0, y0, x1, y1), shrinking until it fits. Returns the height used."""
    x0, y0, x1, y1 = box
    while True:
        f = font(name, size)
        sym = size * 0.95
        lines = wrap(s, f, x1 - x0, sym)
        line_h = size * leading
        if len(lines) * line_h <= (y1 - y0) or size <= min_size:
            break
        size -= 0.25
    if not draw_it:
        return len(lines) * line_h
    space = length(" ", f)
    y = y0
    for line in lines:
        x = x0
        run, run_x = [], x
        for i, (tok, w) in enumerate(line):
            if i:
                x += space
            if tok[0] == "sym":
                if run:
                    draw(img, (run_x, y), " ".join(run), f, color)
                    run = []
                symbol_fn(img, tok[1], x + sym / 2, y + size * 0.62, sym)
                if tok[2]:
                    draw(img, (x + sym, y), tok[2], f, color)
                run_x = x + w + space
            else:
                if not run:
                    run_x = x
                run.append(tok[1])
            x += w
        if run:
            draw(img, (run_x, y), " ".join(run), f, color)
        y += line_h
    return len(lines) * line_h


def energy_text(s: str) -> str:
    """'Provides ColorlessColorless energy.' -> 'Provides {colorless}{colorless} energy.'"""
    for word in ENERGY_WORDS:
        s = s.replace(word + word, "{" + word.lower() + "} {" + word.lower() + "}")
    return s
