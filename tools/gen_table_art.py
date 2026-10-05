#!/usr/bin/env python3
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
ASSETS = ROOT / "common" / "src" / "main" / "resources" / "assets" / "cobblemontcg"
TEXTURES = ASSETS / "textures" / "block"
MODELS = ASSETS / "models" / "block"
RENDER = ROOT / "docs" / "renders" / "items" / "card_dealer_table.png"

NAME = "card_dealer_table"

OUTLINE = (52, 32, 20)
WOOD_DARK = (78, 50, 30)
WOOD = (104, 68, 40)
WOOD_MID = (126, 84, 50)
WOOD_LIGHT = (150, 104, 64)
WOOD_SHINE = (172, 124, 78)
GOLD = (230, 190, 40)
GOLD_DARK = (164, 128, 30)
FELT_DARK = (22, 76, 44)
FELT = (30, 100, 60)
FELT_LIGHT = (40, 118, 72)
RED = (200, 40, 40)
BLUE = (48, 92, 200)
GREEN = (60, 160, 70)
CARD_YELLOW = (240, 206, 72)
CARD_BACK = (17, 33, 109)
CARD_BACK_LIGHT = (40, 64, 150)
PAPER = (240, 236, 224)
PAPER_SHADE = (196, 190, 176)
GLASS_DEEP = (34, 40, 50)
GLASS = (52, 62, 74)
GLASS_SHINE = (176, 214, 226)
FOIL = (196, 198, 208)


def texture():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def planks(img, rng, box=(0, 0, 16, 16), rows=4):
    x0, y0, x1, y1 = box
    px = img.load()
    for y in range(y0, y1):
        row = (y - y0) % rows
        for x in range(x0, x1):
            if row == rows - 1:
                c = WOOD_DARK
            elif row == 0:
                c = WOOD_LIGHT
            else:
                c = rng.choice((WOOD_MID, WOOD_MID, WOOD_MID, WOOD))
            px[x, y] = c + (255,)
    for i, y in enumerate(range(y0, y1, rows)):
        x = x0 + (5 + i * 7) % (x1 - x0)
        for yy in range(y, min(y + rows - 1, y1)):
            px[x, yy] = WOOD_DARK + (255,)


def wood():
    img = texture()
    planks(img, random.Random(1))
    return img


def panel(img, rng, box):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=WOOD_DARK)
    d.rectangle((x0 + 1, y0 + 1, x1 - 2, y1 - 2), fill=WOOD_MID)
    px = img.load()
    for x in range(x0 + 1, x1 - 1):
        px[x, y0 + 1] = WOOD_SHINE + (255,)
        px[x, y1 - 2] = WOOD + (255,)
    for y in range(y0 + 1, y1 - 1):
        px[x0 + 1, y] = WOOD_LIGHT + (255,)
        px[x1 - 2, y] = WOOD + (255,)
    for y in range(y0 + 2, y1 - 2):
        for x in range(x0 + 2, x1 - 2):
            if rng.random() < 0.18:
                px[x, y] = WOOD_LIGHT + (255,)
            elif rng.random() < 0.12:
                px[x, y] = WOOD + (255,)


def edges(img):
    px = img.load()
    for x in range(16):
        px[x, 0] = (GOLD if x % 4 != 3 else GOLD_DARK) + (255,)
        px[x, 1] = WOOD + (255,)
        px[x, 14] = WOOD_MID + (255,)
        px[x, 15] = OUTLINE + (255,)


def side():
    img = texture()
    rng = random.Random(2)
    planks(img, rng)
    edges(img)
    panel(img, rng, (1, 3, 15, 13))
    return img


def front():
    img = texture()
    rng = random.Random(3)
    planks(img, rng)
    edges(img)
    d = ImageDraw.Draw(img)
    d.rectangle((1, 3, 14, 12), fill=WOOD_DARK)
    d.rectangle((2, 4, 13, 11), fill=GLASS_DEEP)
    d.line((2, 4, 13, 4), fill=WOOD_LIGHT)
    px = img.load()
    for y in range(5, 11):
        for x in range(2, 14):
            px[x, y] = (GLASS if (x + y) % 5 else GLASS_DEEP) + (255,)
    for x0, body in ((3, RED), (7, BLUE), (11, GREEN)):
        for x in range(x0, x0 + 2):
            px[x, 5] = FOIL + (255,)
            px[x, 6] = body + (255,)
            px[x, 7] = GOLD + (255,)
    for x in range(2, 14):
        px[x, 8] = WOOD_LIGHT + (255,)
    for x in range(3, 13):
        if x % 3 == 0:
            continue
        px[x, 9] = CARD_YELLOW + (255,)
        px[x, 10] = (RED, BLUE, GREEN, GOLD)[x % 4] + (255,)
    for x, y in ((12, 5), (11, 6), (13, 6), (4, 9), (5, 10)):
        px[x, y] = GLASS_SHINE + (255,)
    px[7, 12] = GOLD + (255,)
    px[8, 12] = GOLD_DARK + (255,)
    return img


def top():
    img = texture()
    rng = random.Random(4)
    px = img.load()
    for y in range(16):
        for x in range(16):
            if x in (0, 15) or y in (0, 15):
                c = WOOD_LIGHT if (x == 0 or y == 0) else WOOD
            elif x in (1, 14) or y in (1, 14):
                c = OUTLINE
            else:
                r = rng.random()
                c = FELT_LIGHT if r < 0.12 else FELT_DARK if r < 0.24 else FELT
            px[x, y] = c + (255,)
    for i in range(2, 14):
        if i % 2 == 0:
            for x, y in ((i, 2), (i, 13), (2, i), (13, i)):
                px[x, y] = GOLD_DARK + (255,)
    return img


def props():
    img = texture()
    d = ImageDraw.Draw(img)
    px = img.load()
    d.rectangle((0, 0, 12, 4), fill=WOOD_MID)
    d.line((0, 4, 12, 4), fill=WOOD_DARK)
    for x0, art in ((1, RED), (5, BLUE), (9, GREEN)):
        d.rectangle((x0, 0, x0 + 2, 3), fill=CARD_YELLOW)
        px[x0 + 1, 1] = art + (255,)
        px[x0 + 1, 2] = art + (255,)
    px[10, 1] = (255, 255, 255, 255)

    d.rectangle((0, 6, 3, 11), fill=RED)
    d.line((0, 6, 3, 6), fill=FOIL)
    d.line((0, 11, 3, 11), fill=FOIL)
    d.line((0, 8, 3, 8), fill=GOLD)
    px[1, 9] = (255, 150, 60, 255)
    px[2, 10] = (255, 150, 60, 255)

    d.rectangle((5, 6, 7, 9), fill=CARD_BACK)
    px[6, 7] = CARD_BACK_LIGHT + (255,)
    px[6, 8] = GOLD + (255,)

    for x in range(5, 9):
        px[x, 11] = PAPER + (255,)
        px[x, 12] = PAPER_SHADE + (255,)
    return img


def tex(name):
    return f"cobblemontcg:block/{NAME}_{name}"


def faces(uvs, texture_of, cull=None):
    out = {}
    for face, uv in uvs.items():
        entry = {"uv": uv, "texture": texture_of[face] if isinstance(texture_of, dict) else texture_of}
        if cull and face in cull:
            entry["cullface"] = face
        out[face] = entry
    return out


def model():
    side_rows = lambda y0, y1: {f: [0, y0, 16, y1] for f in ("north", "south", "east", "west")}
    elements = [
        {
            "from": [0, 0, 0], "to": [16, 2, 16],
            "faces": {**faces(side_rows(14, 16), "#side", cull=("north", "south", "east", "west")),
                      "down": {"uv": [0, 0, 16, 16], "texture": "#wood", "cullface": "down"},
                      "up": {"uv": [0, 0, 16, 16], "texture": "#wood"}},
        },
        {
            "from": [1, 2, 1], "to": [15, 12, 15],
            "faces": {"north": {"uv": [1, 3, 15, 13], "texture": "#front"},
                      "south": {"uv": [1, 3, 15, 13], "texture": "#side"},
                      "east": {"uv": [1, 3, 15, 13], "texture": "#side"},
                      "west": {"uv": [1, 3, 15, 13], "texture": "#side"}},
        },
        {
            "from": [0, 12, 0], "to": [16, 14, 16],
            "faces": {**faces(side_rows(0, 2), "#side", cull=("north", "south", "east", "west")),
                      "up": {"uv": [0, 0, 16, 16], "texture": "#top"},
                      "down": {"uv": [0, 0, 16, 16], "texture": "#wood"}},
        },
        {
            "from": [1.5, 14, 11], "to": [14.5, 15, 12],
            "faces": faces({"north": [1, 4, 14, 5], "south": [1, 4, 14, 5], "east": [4, 4, 5, 5],
                            "west": [4, 4, 5, 5], "up": [1, 4, 14, 5]}, "#wood"),
        },
        {
            "from": [1.5, 14, 12], "to": [14.5, 19, 13],
            "rotation": {"origin": [8, 14, 12], "axis": "x", "angle": 22.5},
            "faces": faces({"north": [0, 0, 13, 5], "south": [1, 8, 14, 13], "east": [4, 8, 5, 13],
                            "west": [4, 8, 5, 13], "up": [1, 8, 14, 9]},
                           {"north": "#props", "south": "#wood", "east": "#wood", "west": "#wood", "up": "#wood"}),
        },
        {
            "from": [3, 14, 3], "to": [7, 14.5, 9],
            "rotation": {"origin": [5, 14, 6], "axis": "y", "angle": 22.5},
            "faces": faces({"up": [0, 6, 4, 12], "north": [0, 6, 4, 6.5], "south": [0, 11, 4, 11.5],
                            "east": [0, 6, 0.5, 12], "west": [3.5, 6, 4, 12]}, "#props"),
        },
        {
            "from": [9.5, 14, 3.5], "to": [12.5, 15.5, 7.5],
            "rotation": {"origin": [11, 14, 5.5], "axis": "y", "angle": -22.5},
            "faces": faces({"up": [5, 6, 8, 10], "north": [5, 11, 8, 12.5], "south": [5, 11, 8, 12.5],
                            "east": [5, 11, 9, 12.5], "west": [5, 11, 9, 12.5]}, "#props"),
        },
    ]
    return {
        "parent": "minecraft:block/block",
        "textures": {"particle": tex("top"), "top": tex("top"), "front": tex("front"), "side": tex("side"),
                     "wood": tex("wood"), "props": tex("props")},
        "elements": elements,
    }


SHADE = {"up": 1.0, "down": 0.5, "north": 0.8, "south": 0.8, "east": 0.6, "west": 0.6}


def rotate(point, rotation):
    if not rotation:
        return point
    o = rotation["origin"]
    a = math.radians(rotation["angle"])
    x, y, z = (point[i] - o[i] for i in range(3))
    c, s = math.cos(a), math.sin(a)
    if rotation["axis"] == "x":
        y, z = y * c - z * s, y * s + z * c
    elif rotation["axis"] == "y":
        x, z = x * c + z * s, -x * s + z * c
    else:
        x, y = x * c - y * s, x * s + y * c
    return (x + o[0], y + o[1], z + o[2])


def face_frame(face, f, t):
    x1, y1, z1 = f
    x2, y2, z2 = t
    return {
        "north": ((x2, y2, z1), (-1, 0, 0), (0, -1, 0), (x2 - x1, y2 - y1)),
        "south": ((x1, y2, z2), (1, 0, 0), (0, -1, 0), (x2 - x1, y2 - y1)),
        "east": ((x2, y2, z2), (0, 0, -1), (0, -1, 0), (z2 - z1, y2 - y1)),
        "west": ((x1, y2, z1), (0, 0, 1), (0, -1, 0), (z2 - z1, y2 - y1)),
        "up": ((x1, y2, z1), (1, 0, 0), (0, 0, 1), (x2 - x1, z2 - z1)),
        "down": ((x1, y1, z2), (1, 0, 0), (0, 0, -1), (x2 - x1, z2 - z1)),
    }[face]


NORMALS = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}


def render(model_json, images, size=256, pitch=30):
    p = math.radians(pitch)
    h = math.cos(p) / math.sqrt(2)
    forward = (h, -math.sin(p), h)
    right = (-1 / math.sqrt(2), 0.0, 1 / math.sqrt(2))
    up = (math.sin(p) / math.sqrt(2), math.sqrt(2) * h, math.sin(p) / math.sqrt(2))
    dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    centre = (8, 9, 8)
    scale = size / 26.0
    project = lambda p: (size / 2 + dot([p[i] - centre[i] for i in range(3)], right) * scale,
                         size / 2 - dot([p[i] - centre[i] for i in range(3)], up) * scale)

    quads = []
    for element in model_json["elements"]:
        rot = element.get("rotation")
        for face, spec in element["faces"].items():
            normal = rotate(NORMALS[face], {**rot, "origin": (0, 0, 0)}) if rot else NORMALS[face]
            if dot(normal, forward) >= 0:
                continue
            image = images[model_json["textures"][spec["texture"][1:]].split("_")[-1]]
            u1, v1, u2, v2 = spec["uv"]
            corner, du, dv, (w, h) = face_frame(face, element["from"], element["to"])
            light = SHADE[face]
            steps_u = max(1, round(abs(u2 - u1)))
            steps_v = max(1, round(abs(v2 - v1)))
            for i in range(steps_u):
                for j in range(steps_v):
                    a, b = i / steps_u, j / steps_v
                    c, d_ = (i + 1) / steps_u, (j + 1) / steps_v
                    pts = []
                    for (s, t) in ((a, b), (c, b), (c, d_), (a, d_)):
                        p = tuple(corner[k] + du[k] * s * w + dv[k] * t * h for k in range(3))
                        pts.append(rotate(p, rot))
                    tu = min(15, int(u1 + (u2 - u1) * (a + c) / 2))
                    tv = min(15, int(v1 + (v2 - v1) * (b + d_) / 2))
                    colour = image.getpixel((tu, tv))
                    if colour[3] == 0:
                        continue
                    shaded = tuple(round(colour[k] * light) for k in range(3)) + (255,)
                    depth = sum(dot(p, forward) for p in pts) / 4
                    quads.append((depth, [project(p) for p in pts], shaded))

    ss = 4
    out = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    for _, pts, colour in sorted(quads, key=lambda q: -q[0]):
        d.polygon([(x * ss, y * ss) for x, y in pts], fill=colour, outline=colour)
    return out.resize((size, size), Image.LANCZOS)


def main():
    images = {"top": top(), "front": front(), "side": side(), "wood": wood(), "props": props()}
    TEXTURES.mkdir(parents=True, exist_ok=True)
    for name, image in images.items():
        image.save(TEXTURES / f"{NAME}_{name}.png")
    model_json = model()
    (MODELS / f"{NAME}.json").write_text(json.dumps(model_json, indent=2) + "\n", encoding="utf-8", newline="\n")
    RENDER.parent.mkdir(parents=True, exist_ok=True)
    render(model_json, images, size=1024).save(RENDER)
    print(f"Wrote {len(images)} textures, the model and {RENDER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
