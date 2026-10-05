#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parent
TEXTURES = TOOLS.parent / "common" / "src" / "main" / "resources" / "assets" / "cobblemontcg" / "textures"

POCKET_W, POCKET_H = 22, 30
POCKET_X = (13, 39, 65, 113, 139, 165)
POCKET_Y = (12, 45, 78)
INVENTORY_X, INVENTORY_Y, HOTBAR_Y = 20, 148, 206

COVER = (0, 0, 200, 128)
PAGES = ((6, 6, 94, 122), (106, 6, 194, 122))
PANEL = (12, 130, 188, 228)

LEATHER = (44, 62, 112)
LEATHER_DARK = (27, 38, 72)
LEATHER_LIGHT = (70, 92, 150)
STITCH = (196, 176, 112)
PAGE = (241, 236, 222)
PAGE_SHADE = (214, 207, 188)
SLEEVE = (226, 222, 211)
SLEEVE_EDGE = (176, 169, 151)
RING = (176, 182, 192)
RING_LIGHT = (236, 240, 246)
RING_DARK = (98, 104, 116)
INK = (60, 70, 100)
INK_HOVER = (120, 140, 200)
INK_DISABLED = (190, 184, 170)


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def cover(img: Image.Image):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = COVER
    d.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=6, fill=LEATHER, outline=LEATHER_DARK)
    for y in range(y0 + 1, y1 - 1):
        for x in range(x0 + 1, x1 - 1):
            if img.getpixel((x, y))[3] and (x * 7 + y * 13 + (x * y) % 5) % 11 == 0:
                img.putpixel((x, y), (*lerp(LEATHER, LEATHER_DARK, 0.35), 255))
    d.line((x0 + 3, y0 + 1, x1 - 4, y0 + 1), fill=LEATHER_LIGHT)
    for x in range(x0 + 4, x1 - 4, 3):
        d.point((x, y0 + 3), fill=STITCH)
        d.point((x, y1 - 4), fill=STITCH)
    for y in range(y0 + 4, y1 - 4, 3):
        d.point((x0 + 3, y), fill=STITCH)
        d.point((x1 - 4, y), fill=STITCH)


def page(img: Image.Image, box, left: bool):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0 - 1)
        shade = t if left else 1 - t
        d.line((x, y0, x, y1 - 1), fill=lerp(PAGE, PAGE_SHADE, max(0.0, shade - 0.75) * 4))
    d.rectangle((x0, y0, x1 - 1, y1 - 1), outline=PAGE_SHADE)
    d.line((x0 + 1, y1, x1 - 2, y1), fill=(200, 192, 172))
    for px in (POCKET_X[:3] if left else POCKET_X[3:]):
        for py in POCKET_Y:
            pocket(d, px, py)


def pocket(d: ImageDraw.ImageDraw, x, y):
    d.rectangle((x, y, x + POCKET_W - 1, y + POCKET_H - 1), fill=SLEEVE, outline=SLEEVE_EDGE)
    d.line((x + 1, y + 1, x + POCKET_W - 2, y + 1), fill=(250, 248, 242))
    d.line((x + 1, y + 1, x + 1, y + POCKET_H - 2), fill=(250, 248, 242))
    d.line((x + 2, y + 4, x + POCKET_W - 3, y + 4), fill=(206, 201, 187))
    d.line((x + POCKET_W - 7, y + 7, x + POCKET_W - 4, y + 4), fill=(248, 247, 242))


def spine(img: Image.Image):
    d = ImageDraw.Draw(img)
    d.rectangle((94, 4, 105, 123), fill=LEATHER_DARK)
    d.line((99, 4, 99, 123), fill=lerp(LEATHER_DARK, (0, 0, 0), 0.4))
    for y in (24, 64, 104):
        d.rounded_rectangle((88, y - 3, 111, y + 3), radius=3, fill=RING_DARK)
        d.rounded_rectangle((88, y - 3, 111, y + 1), radius=3, fill=RING)
        d.line((91, y - 2, 108, y - 2), fill=RING_LIGHT)
        d.ellipse((86, y - 2, 90, y + 2), fill=lerp(PAGE_SHADE, (0, 0, 0), 0.25))
        d.ellipse((109, y - 2, 113, y + 2), fill=lerp(PAGE_SHADE, (0, 0, 0), 0.25))


def panel(img: Image.Image):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = PANEL
    d.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=3, fill=(198, 198, 198), outline=(0, 0, 0))
    d.line((x0 + 1, y0 + 2, x0 + 1, y1 - 3), fill=(255, 255, 255))
    d.line((x0 + 2, y0 + 1, x1 - 3, y0 + 1), fill=(255, 255, 255))
    d.line((x1 - 2, y0 + 2, x1 - 2, y1 - 3), fill=(85, 85, 85))
    d.line((x0 + 2, y1 - 2, x1 - 3, y1 - 2), fill=(85, 85, 85))
    for row in range(3):
        for col in range(9):
            slot(d, INVENTORY_X + col * 18, INVENTORY_Y + row * 18)
    for col in range(9):
        slot(d, INVENTORY_X + col * 18, HOTBAR_Y)


def slot(d: ImageDraw.ImageDraw, x, y):
    d.rectangle((x - 1, y - 1, x + 16, y + 16), fill=(139, 139, 139))
    d.line((x - 1, y - 1, x + 15, y - 1), fill=(55, 55, 55))
    d.line((x - 1, y - 1, x - 1, y + 15), fill=(55, 55, 55))
    d.line((x, y + 16, x + 16, y + 16), fill=(255, 255, 255))
    d.line((x + 16, y, x + 16, y + 16), fill=(255, 255, 255))


def arrow(d: ImageDraw.ImageDraw, x, y, right: bool, color):
    for i in range(5):
        ax = x + 1 + i if not right else x + 10 - i
        d.line((ax, y + 4 - i, ax, y + 5 + i), fill=color)
    if right:
        d.rectangle((x + 1, y + 3, x + 5, y + 6), fill=color)
    else:
        d.rectangle((x + 6, y + 3, x + 10, y + 6), fill=color)


def sort_icon(d: ImageDraw.ImageDraw, x, y, hovered: bool):
    d.rounded_rectangle((x, y, x + 11, y + 11), radius=2, fill=(160, 160, 160) if not hovered else (190, 200, 230),
                        outline=(55, 55, 55))
    d.line((x + 1, y + 1, x + 10, y + 1), fill=(240, 240, 240))
    for i, w in enumerate((3, 5, 7)):
        d.line((x + 2, y + 3 + i * 3, x + 2 + w, y + 3 + i * 3), fill=(50, 50, 60))


def sprites(img: Image.Image):
    d = ImageDraw.Draw(img)
    for i, color in enumerate((INK, INK_HOVER, INK_DISABLED)):
        arrow(d, 200 + i * 12, 0, False, color)
        arrow(d, 200 + i * 12, 10, True, color)
    sort_icon(d, 200, 20, False)
    sort_icon(d, 212, 20, True)


def gui() -> Image.Image:
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    cover(img)
    spine(img)
    page(img, PAGES[0], True)
    page(img, PAGES[1], False)
    spine_rings = Image.new("RGBA", img.size, (0, 0, 0, 0))
    spine(spine_rings)
    ring_mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(ring_mask)
    for y in (24, 64, 104):
        md.rectangle((86, y - 3, 113, y + 3), fill=255)
    img.paste(spine_rings, (0, 0), ring_mask)
    panel(img)
    sprites(img)
    return img


def item() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((6, 0, 12, 4), fill=(250, 214, 64), outline=(160, 120, 30))
    d.rectangle((8, 1, 10, 3), fill=(120, 170, 230))
    d.rectangle((2, 2, 14, 15), fill=LEATHER, outline=LEATHER_DARK)
    d.line((3, 3, 13, 3), fill=LEATHER_LIGHT)
    d.line((3, 3, 3, 14), fill=LEATHER_LIGHT)
    d.rectangle((2, 2, 4, 15), fill=LEATHER_DARK)
    for y in (5, 9, 13):
        d.line((1, y, 5, y), fill=RING)
        d.point((1, y), fill=RING_DARK)
    d.rectangle((7, 7, 12, 10), fill=STITCH)
    d.line((8, 8, 11, 8), fill=LEATHER_DARK)
    return img


def main():
    (TEXTURES / "gui").mkdir(parents=True, exist_ok=True)
    (TEXTURES / "item").mkdir(parents=True, exist_ok=True)
    gui().save(TEXTURES / "gui" / "card_binder.png")
    item().save(TEXTURES / "item" / "card_binder.png")
    print("wrote", TEXTURES / "gui" / "card_binder.png", "and", TEXTURES / "item" / "card_binder.png")


if __name__ == "__main__":
    main()
