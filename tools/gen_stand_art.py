#!/usr/bin/env python3
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw

from gen_table_art import render

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
ASSETS = ROOT / "common" / "src" / "main" / "resources" / "assets" / "cobblemontcg"
TEXTURES = ASSETS / "textures"
MODELS = ASSETS / "models"
RENDER = ROOT / "docs" / "renders" / "items" / "card_display_stand.png"

NAME = "card_display_stand"

OUTLINE = (40, 18, 14)
WOOD_DARK = (64, 28, 22)
WOOD = (96, 42, 30)
WOOD_MID = (118, 56, 38)
WOOD_LIGHT = (142, 72, 48)
WOOD_SHINE = (168, 96, 64)
GOLD_DEEP = (128, 92, 20)
GOLD_DARK = (172, 132, 32)
GOLD = (228, 188, 52)
GOLD_SHINE = (255, 234, 130)
VELVET_DARK = (92, 14, 26)
VELVET = (128, 22, 36)
VELVET_LIGHT = (158, 36, 50)

BOARD_FROM = [3.5, 4, 9]
BOARD_TO = [12.5, 16, 10]
BOARD_ROTATION = {"origin": [8, 4, 10], "axis": "x", "angle": 22.5}


def texture():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def grain(img, rng, box=(0, 0, 16, 16)):
    x0, y0, x1, y1 = box
    px = img.load()
    for y in range(y0, y1):
        base = (WOOD_MID, WOOD, WOOD_MID, WOOD_LIGHT)[y % 4]
        for x in range(x0, x1):
            r = rng.random()
            c = WOOD_LIGHT if r < 0.08 else WOOD if r < 0.18 else base
            px[x, y] = c + (255,)
    for _ in range(3):
        x, y = rng.randrange(x0 + 1, x1 - 1), rng.randrange(y0, y1)
        px[x, y] = WOOD_DARK + (255,)
        if x + 1 < x1:
            px[x + 1, y] = WOOD + (255,)


def wood():
    img = texture()
    grain(img, random.Random(11))
    return img


def bands(img, rng):
    grain(img, rng, (0, 0, 16, 12))
    px = img.load()
    for x in range(16):
        px[x, 12] = (GOLD if x % 4 != 3 else GOLD_DARK) + (255,)
        px[x, 13] = WOOD_SHINE + (255,)
        px[x, 14] = (WOOD_MID if x % 5 else WOOD_LIGHT) + (255,)
        px[x, 15] = WOOD_DARK + (255,)


def side():
    img = texture()
    bands(img, random.Random(12))
    return img


def front():
    img = texture()
    bands(img, random.Random(13))
    d = ImageDraw.Draw(img)
    d.rectangle((5, 13, 10, 14), fill=GOLD)
    d.line((5, 13, 10, 13), fill=GOLD_SHINE)
    d.point((5, 14), fill=GOLD_DARK)
    d.point((10, 14), fill=GOLD_DARK)
    d.line((7, 14, 8, 14), fill=GOLD_DEEP)
    return img


def velvet(img, rng, box):
    x0, y0, x1, y1 = box
    px = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r = rng.random()
            c = VELVET_LIGHT if r < 0.12 else VELVET_DARK if r < 0.26 else VELVET
            px[x, y] = c + (255,)


def top():
    img = texture()
    rng = random.Random(14)
    grain(img, rng)
    velvet(img, rng, (3, 3, 13, 13))
    px = img.load()
    for i in range(2, 14):
        for x, y in ((i, 2), (i, 13), (2, i), (13, i)):
            px[x, y] = (GOLD if (x + y) % 3 else GOLD_DARK) + (255,)
    for i in (2, 13):
        for j in (2, 13):
            px[i, j] = GOLD_SHINE + (255,)
    return img


def board():
    img = texture()
    rng = random.Random(15)
    grain(img, rng)
    velvet(img, rng, (4, 3, 11, 13))
    px = img.load()
    for y in range(2, 14):
        px[3, y] = GOLD + (255,)
        px[11, y] = GOLD_DARK + (255,)
    for x in range(3, 12):
        px[x, 2] = GOLD_SHINE + (255,)
        px[x, 13] = GOLD_DARK + (255,)
    for x in range(4, 11):
        px[x, 3] = VELVET_DARK + (255,)
    return img


def tex(name):
    return f"cobblemontcg:block/{NAME}_{name}"


def faces(uvs, texture_of):
    return {face: {"uv": uv, "texture": texture_of[face] if isinstance(texture_of, dict) else texture_of} for face, uv in uvs.items()}


def box_uvs(f, t):
    x1, y1, z1 = f
    x2, y2, z2 = t
    return {
        "north": [16 - x2, 16 - y2, 16 - x1, 16 - y1],
        "south": [x1, 16 - y2, x2, 16 - y1],
        "east": [16 - z2, 16 - y2, 16 - z1, 16 - y1],
        "west": [z1, 16 - y2, z2, 16 - y1],
        "up": [x1, z1, x2, z2],
        "down": [x1, 16 - z2, x2, 16 - z1],
    }


def element(f, t, textures, rotation=None, uv_override=None):
    uvs = box_uvs(f, t)
    uvs.update(uv_override or {})
    out = {"from": f, "to": t, "faces": faces({k: uvs[k] for k in textures}, textures)}
    if rotation:
        out["rotation"] = rotation
    return out


def block_elements():
    sides = {"north": "#front", "south": "#side", "east": "#side", "west": "#side"}
    return [
        element([2, 0, 2], [14, 1, 14], {**sides, "north": "#side", "up": "#wood", "down": "#wood"}),
        element([2.5, 1, 2.5], [13.5, 3, 13.5], sides),
        element([2, 3, 2], [14, 4, 14], {**{k: "#side" for k in sides}, "up": "#top", "down": "#wood"}),
        element(BOARD_FROM, BOARD_TO, {"north": "#board", "south": "#wood", "east": "#wood", "west": "#wood", "up": "#wood"},
                BOARD_ROTATION, {"north": [3, 2, 12, 14], "south": [3, 2, 12, 14], "east": [0, 2, 1, 14], "west": [0, 2, 1, 14],
                                 "up": [3, 0, 12, 1]}),
        element([3.5, 4, 7.5], [12.5, 5, 9], {"north": "#side", "east": "#wood", "west": "#wood", "up": "#wood"},
                uv_override={"north": [3.5, 12, 12.5, 13]}),
    ]


def block_model():
    return {
        "parent": "minecraft:block/block",
        "textures": {"particle": tex("wood"), "wood": tex("wood"), "side": tex("side"), "front": tex("front"),
                     "top": tex("top"), "board": tex("board")},
        "elements": block_elements(),
    }


def item_model():
    card = element([4.25, 5, 8.4], [11.75, 15.5, 8.7], {"north": "#card", "east": "#card", "west": "#card", "up": "#card"},
                   BOARD_ROTATION, {"north": [0, 0, 16, 16], "east": [0, 1, 0.3, 15], "west": [0, 1, 0.3, 15], "up": [4, 0, 12, 0.3]})
    return {
        "parent": "minecraft:block/block",
        "textures": {**block_model()["textures"], "card": "cobblemontcg:tcg/card_back"},
        "elements": block_elements() + [card],
    }


GUI_W, GUI_H = 176, 202
POCKET = (14, 18, 36, 50)
INVENTORY_X, INVENTORY_Y, HOTBAR_Y = 8, 120, 178


def panel(img):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, GUI_W - 1, GUI_H - 1), radius=4, fill=(198, 198, 198), outline=(0, 0, 0))
    d.line((1, 2, 1, GUI_H - 3), fill=(255, 255, 255))
    d.line((2, 1, GUI_W - 3, 1), fill=(255, 255, 255))
    d.line((2, 2, 2, 3), fill=(255, 255, 255))
    d.line((GUI_W - 2, 2, GUI_W - 2, GUI_H - 3), fill=(85, 85, 85))
    d.line((2, GUI_H - 2, GUI_W - 3, GUI_H - 2), fill=(85, 85, 85))
    for row in range(3):
        for col in range(9):
            slot(d, INVENTORY_X + col * 18, INVENTORY_Y + row * 18)
    for col in range(9):
        slot(d, INVENTORY_X + col * 18, HOTBAR_Y)


def slot(d, x, y):
    d.rectangle((x - 1, y - 1, x + 16, y + 16), fill=(139, 139, 139))
    d.line((x - 1, y - 1, x + 15, y - 1), fill=(55, 55, 55))
    d.line((x - 1, y - 1, x - 1, y + 15), fill=(55, 55, 55))
    d.line((x, y + 16, x + 16, y + 16), fill=(255, 255, 255))
    d.line((x + 16, y, x + 16, y + 16), fill=(255, 255, 255))


def gilded_slot(d, x, y):
    d.rectangle((x - 2, y - 2, x + 17, y + 17), outline=GOLD_DARK)
    d.line((x - 2, y - 2, x + 16, y - 2), fill=GOLD)
    slot(d, x, y)


def pocket(img):
    d = ImageDraw.Draw(img)
    x, y, w, h = POCKET
    d.rectangle((x - 2, y - 2, x + w + 1, y + h + 1), fill=WOOD_DARK)
    d.rectangle((x - 1, y - 1, x + w, y + h), outline=GOLD_DARK)
    d.line((x - 1, y - 1, x + w, y - 1), fill=GOLD)
    rng = random.Random(21)
    px = img.load()
    for yy in range(y, y + h):
        shade = (yy - y) / h
        for xx in range(x, x + w):
            r = rng.random()
            c = VELVET_LIGHT if r < 0.06 else VELVET_DARK if r < 0.16 + shade * 0.25 else VELVET
            px[xx, yy] = c + (255,)
    cw, ch = 30, 42
    cx, cy = x + (w - cw) // 2, y + (h - ch) // 2
    d.rounded_rectangle((cx, cy, cx + cw - 1, cy + ch - 1), radius=2, outline=VELVET_DARK)
    d.line((x, y, x + w - 1, y), fill=VELVET_DARK)


def amount_field(d, x, y, w, h):
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=(0, 0, 0), outline=(160, 160, 160))
    d.line((x, y, x + w - 2, y), fill=(55, 55, 55))
    d.line((x, y, x, y + h - 2), fill=(55, 55, 55))


def divider(d, y):
    d.line((58, y, 168, y), fill=(160, 160, 160))
    d.line((58, y + 1, 168, y + 1), fill=(232, 232, 232))


def owner_gui():
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    panel(img)
    pocket(img)
    d = ImageDraw.Draw(img)
    gilded_slot(d, 60, 32)
    amount_field(d, 95, 32, 38, 16)
    divider(d, 62)
    gilded_slot(d, 60, 76)
    return img


def buyer_gui():
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    panel(img)
    pocket(img)
    d = ImageDraw.Draw(img)
    divider(d, 44)
    gilded_slot(d, 60, 62)
    return img


def main():
    images = {"wood": wood(), "side": side(), "front": front(), "top": top(), "board": board()}
    (TEXTURES / "block").mkdir(parents=True, exist_ok=True)
    for name, image in images.items():
        image.save(TEXTURES / "block" / f"{NAME}_{name}.png")
    write_json(MODELS / "block" / f"{NAME}.json", block_model())
    model = item_model()
    write_json(MODELS / "item" / f"{NAME}.json", model)

    owner_gui().save(TEXTURES / "gui" / f"{NAME}_owner.png")
    buyer_gui().save(TEXTURES / "gui" / f"{NAME}_buyer.png")

    preview = dict(images)
    preview["back"] = Image.open(TEXTURES / "tcg" / "card_back.png").convert("RGBA").resize((16, 16), Image.LANCZOS)
    RENDER.parent.mkdir(parents=True, exist_ok=True)
    render(model, preview, size=1024).save(RENDER)
    print(f"Wrote {len(images)} block textures, both models, both GUIs and {RENDER.relative_to(ROOT)}")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
