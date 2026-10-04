"""
Builds the per-card layer (everything that differs between cards): stage line, name, HP,
illustration, Pokemon Powers and attacks, weakness / resistance / retreat, level, number and
rarity. The frame layer (border, face, art window background, static labels) comes from
layout.py and is shared per type.

Game text (attack names, costs, damage, rules) comes from tools/<set>_text.json. Drawings come from
art/pokemon_<set>.py and art/trainers_<set>.py, one function per card number.
"""
import math

from PIL import Image, ImageDraw

from . import finish as F
from . import layout as L
from .canvas import Sprite
from . import pokemon_base1, pokemon_base2, trainers_base1, trainers_base2

# set -> card number -> drawing
POKEMON = {"base1": pokemon_base1.DRAW, "base2": pokemon_base2.DRAW}
TRAINERS = {"base1": trainers_base1.DRAW, "base2": trainers_base2.DRAW}

HP_RED = (198, 34, 30)
POWER_RED = (188, 34, 30)


def frame_name(card: dict) -> str:
    if card["supertype"] == "pokemon":
        return f"pokemon_{card['type']}"
    return card["supertype"]


def illustration(drawings: dict, number: int, w=None, h=None) -> Image.Image:
    w = w or L.ART[2] - L.ART[0] + 1
    h = h or L.ART[3] - L.ART[1] + 1
    sprite = Sprite(w, h)
    drawings[number](sprite)
    return sprite.render()


def _footer(img, card, total, face):
    small = F.font("Regular", 6)
    muted = L.mix(L.TEXT, face, 0.3)
    F.draw(img, (L.FACE[0] + 9, L.FOOTER_Y), "Cobblemon: TCG", small, muted)
    F.draw(img, ((L.FACE[0] + L.FACE[2]) / 2 + 6, L.FOOTER_Y), "Fan-made card, not official", small, muted, anchor="ma")
    F.draw(img, (L.FACE[2] - 18, L.FOOTER_Y - 0.5), f"{card['number']}/{total}", F.font("Bold", 6.5), L.TEXT, anchor="ra")
    L.rarity_symbol(img, card["rarity"], L.FACE[2] - 10, L.FOOTER_Y + 4, 7)


def _symbol(img, kind, cx, cy, size):
    L.paste_symbol(img, kind, cx, cy, size)


# ---------------------------------------------------------------- pokemon

def _header(img, card, text, by_name):  # noqa: ARG001 (by_name kept for custom sets)
    face = L.FACE_COLORS[card["type"]]
    stage = (text.get("subtypes") or ["Basic"])[0]
    evolves = text.get("evolvesFrom")
    x = L.FACE[0] + 7
    if evolves:
        # portrait of the previous stage, like the little window on real evolution cards; the
        # creature itself is its own layer on top (evolution_portrait), so it can be swapped out
        box = L.EVOLUTION_BOX
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle((box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1), fill=L.rgba((232, 198, 92)))
        bw, bh = box[2] - box[0] + 1, box[3] - box[1] + 1
        img.alpha_composite(L.background(card["type"]).resize((bw, bh), Image.LANCZOS), box[:2])
        d.rectangle((box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1), outline=L.rgba((150, 116, 40)))
        x = box[2] + 6
        label = stage.upper()
        f = F.font("Bold", 6.5)
        lw = F.length(label, f)
        d.rounded_rectangle((x, L.STAGE_Y - 1, x + lw + 6, L.STAGE_Y + 7), radius=2, fill=(30, 26, 28, 255))
        F.draw(img, (x + 3, L.STAGE_Y - 0.5), label, f, (255, 255, 255))
        F.draw(img, (x + lw + 10, L.STAGE_Y - 0.5), f"Evolves from {evolves}", F.font("Italic", 6.5), L.mix(L.TEXT, face, 0.15))
    else:
        F.draw(img, (x, L.STAGE_Y - 0.5), "Basic Pokémon", F.font("Italic", 7), L.mix(L.TEXT, face, 0.15))

    hp = card["hp"]
    right = L.FACE[2] - 22
    hp_font = F.font("Bold", 15)
    hp_w = F.length(str(hp), hp_font) if hp else 0
    if hp:
        F.draw(img, (right, L.NAME_Y), str(hp), hp_font, HP_RED, anchor="rs")
        F.draw(img, (right - hp_w - 2, L.NAME_Y - 1), "HP", F.font("Bold", 8), HP_RED, anchor="rs")
    L.paste_symbol(img, card["type"], L.FACE[2] - 11, L.NAME_Y - 6, 15)
    name_font = F.fit("Bold", 15, card["name"], right - hp_w - 16 - x)
    F.draw(img, (x, L.NAME_Y), card["name"], name_font, L.TEXT, anchor="ls")


def _body_blocks(text):
    blocks = []
    for power in text.get("powers", []):
        blocks.append(("power", power))
    for attack in text.get("attacks", []):
        blocks.append(("attack", attack))
    return blocks


def _layout_body(img, card, text, size, draw_it):
    """Lays out powers and attacks at a text size; returns the total height."""
    x0, y0, x1, y1 = L.BODY
    face = L.FACE_COLORS[card["type"]]
    blocks = _body_blocks(text)
    heights = []
    y = 0.0
    for i, (kind, b) in enumerate(blocks):
        start = y
        if kind == "power":
            if draw_it:
                F.draw(img, (x0 + 4, y0 + y), "Pokémon Power:", F.font("Bold", size + 1), POWER_RED)
                pw = F.length("Pokémon Power: ", F.font("Bold", size + 1))
                F.draw(img, (x0 + 4 + pw, y0 + y), b["name"], F.font("Bold", size + 2), POWER_RED)
            y += size + 4
            y += F.paragraph(img, (x0 + 4, y0 + y, x1 - 4, 10_000), F.energy_text(b["text"]), "Regular", size, L.TEXT,
                             _symbol, draw_it=draw_it)
        else:
            cost = b["cost"] or []
            row_h = size + 7
            if draw_it:
                cy = y0 + y + row_h / 2
                sym = 11
                for j, kind_ in enumerate(cost[:4]):
                    L.paste_symbol(img, kind_, x0 + 9 + j * (sym + 1), cy, sym)
                if not cost:
                    F.draw(img, (x0 + 4, cy), "—", F.font("Bold", size + 2), L.TEXT, anchor="lm")
                name_x = x0 + 12 + max(len(cost), 1) * 12
                dmg_w = 30
                name_font = F.fit("Bold", size + 4, b["name"], x1 - dmg_w - name_x - 4)
                F.draw(img, ((name_x + x1 - dmg_w) / 2, cy), b["name"], name_font, L.TEXT, anchor="mm")
                if b.get("damage"):
                    F.draw(img, (x1 - 6, cy), b["damage"].replace("×", "x"), F.font("Bold", size + 6), L.TEXT, anchor="rm")
            y += row_h
            if b.get("text"):
                y += 1
                y += F.paragraph(img, (x0 + 4, y0 + y, x1 - 4, 10_000), F.energy_text(b["text"]), "Regular", size, L.TEXT,
                                 _symbol, draw_it=draw_it)
        y += 3
        if draw_it and i < len(blocks) - 1:
            ImageDraw.Draw(img).line((x0 + 10, y0 + y, x1 - 10, y0 + y), fill=L.rgba(L.mix(face, (0, 0, 0), 0.3)))
        y += 3
        heights.append(y - start)
    return y


def evolution_portrait(prev: tuple[str, int]) -> Image.Image:
    """The previous stage, close up, for the portrait window (32x32 texture, picture in the top 32x24).
    prev is the (set, number) of a card showing it, which may be in an earlier set."""
    box = L.EVOLUTION_BOX
    bw, bh = box[2] - box[0] + 1, box[3] - box[1] + 1
    out = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    set_name, number = prev
    drawings = POKEMON.get(set_name, {})
    if number in drawings:
        art = illustration(drawings, number, bw * 2, bh * 2)
        out.alpha_composite(art.crop((bw * 0.5, bh * 0.25, bw * 1.5, bh * 1.25)).resize((bw, bh), Image.LANCZOS))
    return out


def pokemon_card(card: dict, total: int, text: dict, by_name: dict) -> Image.Image:
    kind = card["type"]
    face = L.FACE_COLORS[kind]
    img = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))

    _header(img, card, text, by_name)

    dex = text.get("dex")
    strip = f"No. {dex:03d}   {card['name']}   {card['set_title']}" if dex else card["name"]
    F.draw(img, ((L.STRIP[0] + L.STRIP[2]) / 2, (L.STRIP[1] + L.STRIP[3]) / 2 + 0.5), strip, F.font("Italic", 7),
           (70, 52, 20), anchor="mm")

    # powers and attacks: pick the largest text that fits, then centre vertically
    avail = L.BODY[3] - L.BODY[1]
    size = 8.0
    while size > 5.5 and _layout_body(Image.new("RGBA", (L.W, L.H)), card, text, size, False) > avail:
        size -= 0.25
    used = _layout_body(Image.new("RGBA", (L.W, L.H)), card, text, size, False)
    body = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
    _layout_body(body, card, text, size, True)
    img.alpha_composite(body, (0, max(0, round((avail - used) / 2))))

    cell = (L.WRR[2] - L.WRR[0]) / 3
    cy = L.WRR[1] + 12.5
    for i, key in enumerate(("weakness", "resistance")):
        entries = text.get(key) or []
        cx = L.WRR[0] + cell * i + cell / 2
        for e in entries[:1]:
            L.paste_symbol(img, e["type"], cx - 5, cy, 8)
            F.draw(img, (cx + 1, cy), e["value"].replace("×", "x"), F.font("Bold", 7), L.TEXT, anchor="lm")
    retreat = text.get("retreat", 0)
    for i in range(retreat):
        L.paste_symbol(img, "colorless", L.WRR[0] + cell * 2.5 + (i - (retreat - 1) / 2) * 9, cy, 8)

    level = text.get("level")
    if level:
        F.draw(img, (L.FLAVOR[2] - 6, (L.FLAVOR[1] + L.FLAVOR[3]) / 2), f"LV. {level}   #{dex}", F.font("Bold", 7), L.TEXT, anchor="rm")

    _footer(img, card, total, face)
    return F.grain(img, 3, seed=card["number"])


# ---------------------------------------------------------------- trainers and energy

def _rules(img, text, box, size=9.0):
    rules = [r for r in text.get("rules", []) if not r.startswith("This card stays in play")]
    s = "\n".join(F.energy_text(r) for r in rules)
    F.paragraph(img, box, s, "Regular", size, L.TEXT, _symbol, min_size=6)


def trainer_card(card: dict, total: int, text: dict) -> Image.Image:
    img = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
    face = L.FACE_COLORS["trainer"]
    img.alpha_composite(illustration(TRAINERS[card["set"]], card["number"]), (L.ART[0], L.ART[1]))
    F.draw(img, (L.FACE[2] - 7, L.STAGE_Y - 1), "TRAINER", F.font("Bold", 8), (196, 30, 36), anchor="ra")
    name_font = F.fit("Bold", 16, card["name"], L.FACE[2] - L.FACE[0] - 20)
    F.draw(img, (L.FACE[0] + 7, L.NAME_Y), card["name"], name_font, L.TEXT, anchor="ls")
    x0, y0, x1, y1 = L.RULES
    F.draw(img, ((x0 + x1) / 2, y0 + 6), "Trainer", F.font("Bold", 9), (196, 30, 36), anchor="ma")
    ImageDraw.Draw(img).line((x0 + 30, y0 + 19, x1 - 30, y0 + 19), fill=(200, 200, 208, 255))
    _rules(img, text, (x0 + 8, y0 + 24, x1 - 8, y1 - 6), 9.5)
    _footer(img, card, total, face)
    return F.grain(img, 3, seed=card["number"])


def energy_card(card: dict, total: int, text: dict) -> Image.Image:
    kind = card["type"] or "colorless"
    img = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
    face = L.FACE_COLORS["energy"]
    special = "Special" in (text.get("subtypes") or [])

    # sunburst in the type colour behind the symbol
    burst = Image.new("RGBA", (L.W * L.SS, L.H * L.SS), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    cx, cy = L.W / 2 * L.SS, (130 if special else 176) * L.SS
    col = L.TYPE_COLORS[kind]
    for i in range(28):
        a0, a1 = math.radians(i * 360 / 28), math.radians(i * 360 / 28 + 6.4)
        r = 260 * L.SS
        bd.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))],
                   fill=L.rgba(L.mix(col, (255, 255, 255), 0.5), 200))
    burst = burst.resize((L.W, L.H), Image.LANCZOS)
    clip = Image.new("L", (L.W, L.H), 0)
    ImageDraw.Draw(clip).rounded_rectangle((L.FACE[0] + 10, L.FACE[1] + 27, L.FACE[2] - 10, L.FACE[3] - 23), radius=3, fill=255)
    img.alpha_composite(F.clip_to(burst, clip))

    name_font = F.fit("Bold", 16, card["name"], L.FACE[2] - L.FACE[0] - 40)
    F.draw(img, (L.W / 2, L.NAME_Y - 2), card["name"], name_font, L.TEXT, anchor="ms")
    if special:
        L.paste_symbol(img, kind, L.W / 2 - 26, 118, 72)
        L.paste_symbol(img, kind, L.W / 2 + 26, 140, 72)
        d = ImageDraw.Draw(img, "RGBA")
        box = (L.FACE[0] + 22, 214, L.FACE[2] - 22, 306)
        d.rounded_rectangle(box, radius=3, fill=(250, 248, 240, 245), outline=(180, 170, 140, 255))
        _rules(img, text, (box[0] + 8, box[1] + 10, box[2] - 8, box[3] - 8), 10)
    else:
        L.paste_symbol(img, kind, L.W / 2, 176, 132)
    _footer(img, card, total, face)
    return F.grain(img, 3, seed=card["number"])


def card_layers(card: dict, total: int, text: dict, by_name: dict) -> dict:
    """Every texture of one card: 'card' always, plus 'illustration' (the Pokemon in the art
    window, 208x144) and 'evolution' (the previous stage in the portrait window) for Pokemon.
    Those two are separate layers so the mod can swap in Cobblemon's models at runtime.
    card holds 'set' (e.g. base1) and 'set_title' (e.g. Base Set) next to the CSV columns;
    by_name maps a Pokemon name to the (set, number) of a card that shows it."""
    layers = {"card": card_art(card, total, text, by_name)}
    if card["supertype"] == "pokemon":
        layers["illustration"] = illustration(POKEMON[card["set"]], card["number"])
        prev = by_name.get(text.get("evolvesFrom"))
        if prev is not None:
            layers["evolution"] = evolution_portrait(prev)
    return layers


def card_art(card: dict, total: int, text: dict, by_name: dict) -> Image.Image:
    if card["supertype"] == "pokemon":
        return pokemon_card(card, total, text, by_name)
    if card["supertype"] == "trainer":
        return trainer_card(card, total, text)
    return energy_card(card, total, text)
