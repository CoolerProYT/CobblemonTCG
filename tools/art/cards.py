"""
Builds the per-card art layer (everything that differs between cards). The frame layer
(border, face, art window background, static labels) comes from layout.py and is shared per type.
"""
import math

from PIL import Image, ImageDraw

from . import layout as L
from .canvas import Sprite
from .pokemon_base1 import DRAW as POKEMON
from .trainers_base1 import DRAW as TRAINERS

HP_RED = (200, 40, 36)


def frame_name(card: dict) -> str:
    if card["supertype"] == "pokemon":
        return f"pokemon_{card['type']}"
    return card["supertype"]


def illustration(drawings: dict, number: int) -> Image.Image:
    w, h = L.ART[2] - L.ART[0] + 1, L.ART[3] - L.ART[1] + 1
    sprite = Sprite(w, h)
    drawings[number](sprite)
    return sprite.render()


def _footer(img, card, total):
    label = f"{card['number']}/{total}"
    L.text(img, (197, L.FOOTER_Y), label, 8, L.TEXT, anchor="ra")
    L.rarity_symbol(img, card["rarity"], 205, L.FOOTER_Y + 4)


def _attack_row(img, y, costs, face):
    """Energy cost symbols, a name bar and two lines of text, without real attack text."""
    d = ImageDraw.Draw(img)
    for i, kind in enumerate(costs):
        L.paste_symbol(img, kind, 56 + i * 11, y, 10)
    x0 = 56 + len(costs) * 11 + 4
    dark = L.mix(face, (0, 0, 0), 0.45)
    d.rounded_rectangle((x0, y - 3, x0 + 54, y + 2), radius=2, fill=L.rgba(dark))
    d.rounded_rectangle((176, y - 4, 198, y + 3), radius=2, fill=L.rgba(L.mix(face, (0, 0, 0), 0.2)))
    for dy in (8, 13):
        d.line((x0, y + dy, 198, y + dy), fill=L.rgba(L.mix(face, (0, 0, 0), 0.22)))


def pokemon_card(card: dict, total: int) -> Image.Image:
    kind = card["type"]
    face = L.FACE_COLORS[kind]
    img = Image.new("RGBA", (L.SIZE, L.SIZE), (0, 0, 0, 0))

    L.text(img, (50, L.NAME_Y + 1), card["name"], 15, L.TEXT, bold=True, max_width=100)
    if card["hp"]:
        L.text(img, (187, L.NAME_Y + 2), str(card["hp"]), 14, HP_RED, bold=True, anchor="ra")
        width = ImageDraw.Draw(img).textlength(str(card["hp"]), font=L.font(14))
        L.text(img, (186 - width, L.NAME_Y + 7), "HP", 8, HP_RED, anchor="ra")
    L.paste_symbol(img, kind, 199, L.NAME_Y + 9, 13)

    img.alpha_composite(illustration(POKEMON, card["number"]), (L.ART[0], L.ART[1]))

    # length / weight strip: decorative dashes only
    d = ImageDraw.Draw(img)
    d.line((70, 127, 186, 127), fill=L.rgba((176, 150, 80)))

    hp = card["hp"] or 40
    big = 4 if hp >= 100 else 3 if hp >= 60 else 2
    _attack_row(img, L.ATTACK_ROWS[0], [kind], face)
    _attack_row(img, L.ATTACK_ROWS[1], [kind] * (big - 1) + ["colorless"], face)

    cell = (L.WRR[2] - L.WRR[0]) / 3
    weak = L.WEAKNESS.get(kind)
    if weak:
        L.paste_symbol(img, weak, L.WRR[0] + cell * 0.5, L.WRR[1] + 11, 8)
    res = L.RESISTANCE.get(kind)
    if res:
        L.paste_symbol(img, res, L.WRR[0] + cell * 1.5, L.WRR[1] + 11, 8)
    retreat = max(1, min(4, hp // 35))
    for i in range(retreat):
        L.paste_symbol(img, "colorless", L.WRR[0] + cell * 2.5 + (i - (retreat - 1) / 2) * 9, L.WRR[1] + 11, 8)

    _footer(img, card, total)
    return img


def trainer_card(card: dict, total: int) -> Image.Image:
    img = Image.new("RGBA", (L.SIZE, L.SIZE), (0, 0, 0, 0))
    L.text(img, (50, L.NAME_Y + 1), card["name"], 14, L.TEXT, bold=True, max_width=118)
    L.text(img, (206, L.NAME_Y + 4), "TRAINER", 8, (190, 40, 40), bold=True, anchor="ra")
    img.alpha_composite(illustration(TRAINERS, card["number"]), (L.ART[0], L.ART[1]))
    _footer(img, card, total)
    return img


def energy_card(card: dict, total: int) -> Image.Image:
    kind = card["type"] or "colorless"
    img = Image.new("RGBA", (L.SIZE, L.SIZE), (0, 0, 0, 0))
    special = not card["name"].lower().endswith(" energy") or card["rarity"] != "common"

    # sunburst in the type colour behind the symbol
    burst = Image.new("RGBA", (L.SIZE * L.SS, L.SIZE * L.SS), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    cx, cy = 128 * L.SS, (112 if special else 128) * L.SS
    col = L.TYPE_COLORS[kind]
    for i in range(24):
        a0, a1 = math.radians(i * 15), math.radians(i * 15 + 7.5)
        r = 140 * L.SS
        bd.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))],
                   fill=L.rgba(L.mix(col, (255, 255, 255), 0.55)))
    burst = burst.resize((L.SIZE, L.SIZE), Image.LANCZOS)
    clip = Image.new("L", (L.SIZE, L.SIZE), 0)
    ImageDraw.Draw(clip).rectangle((51, 29, 204, 231), fill=255)
    burst.putalpha(Image.composite(burst.getchannel("A"), Image.new("L", clip.size, 0), clip))
    img.alpha_composite(burst)

    L.text(img, (128, L.NAME_Y + 1), card["name"], 14, L.TEXT, bold=True, anchor="ma", max_width=150)
    if special:
        L.paste_symbol(img, kind, 112, 100, 64)
        L.paste_symbol(img, kind, 144, 112, 64)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((60, 168, 196, 226), radius=3, fill=L.rgba((248, 246, 238)), outline=L.rgba((180, 170, 140)))
        for y in range(178, 222, 9):
            d.line((68, y, 188, y), fill=L.rgba((200, 196, 184)))
    else:
        L.paste_symbol(img, kind, 128, 128, 112)
    _footer(img, card, total)
    return img


def card_art(card: dict, total: int) -> Image.Image:
    if card["supertype"] == "pokemon":
        return pokemon_card(card, total)
    if card["supertype"] == "trainer":
        return trainer_card(card, total)
    return energy_card(card, total)
