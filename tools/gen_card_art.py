#!/usr/bin/env python3
"""
Draws the card textures: original illustrations in a layout inspired by the 1999 Base Set.
No official card art, scans, logos or set symbols are used. Replace any file with your own
drawing of the same size and name, no code changes needed.

Writes into common/src/main/resources/assets/cobblemontcg/textures/:
  tcg/frame/pokemon_<type>.png, trainer.png, energy.png
                                card frame, face and art window background (layer 0)
  tcg/holo_overlay.png(.mcmeta) animated foil over the art window (holo prints only)
  tcg/<set>/<number>.png        everything specific to one card: name, HP, illustration,
                                costs, number, rarity (last layer)
  item/booster_pack.png         booster pack wrapper ("default" variant)
  item/tcg_card.png             card back, used when a card has no model
and the mod icon common/src/main/resources/cobblemontcg.png.

Card textures are 256x256 with the card (184x256) in the middle.

Usage: python tools/gen_card_art.py [--skip-existing-art] [--only 4,58]
  --skip-existing-art  keep card textures that already exist, so your own drawings are never overwritten
  --only               only redraw these card numbers
"""
import argparse
import csv
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art import layout as L  # noqa: E402
from art.cards import card_art  # noqa: E402

NAMESPACE = "cobblemontcg"
TOOLS = Path(__file__).resolve().parent
RESOURCES = TOOLS.parent / "common" / "src" / "main" / "resources"
TEXTURES = RESOURCES / "assets" / NAMESPACE / "textures"


def rgba(c, a=255):
    return (*c, a)


def make_booster_pack() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    left, right, top, bottom = 7, 24, 2, 29
    for y in range(top + 2, bottom - 1):
        t = (y - top) / (bottom - top)
        draw.line((left, y, right, y), fill=rgba(L.mix((36, 52, 140), (128, 44, 150), t)))
    for x in range(left, right + 1):  # crimped seals
        shade = (190, 190, 205) if x % 2 == 0 else (140, 140, 160)
        draw.line((x, top, x, top + 1 + (x % 2)), fill=rgba(shade))
        draw.line((x, bottom - 1 - (x % 2), x, bottom), fill=rgba(shade))
    draw.line((left, top + 2, left, bottom - 2), fill=rgba((20, 24, 70)))
    draw.line((right, top + 2, right, bottom - 2), fill=rgba((20, 24, 70)))
    draw.line((left + 2, top + 4, left + 2, bottom - 6), fill=rgba((150, 160, 240)))
    for i, (dx, color) in enumerate(((-3, (240, 200, 70)), (0, (240, 240, 240)), (3, (90, 200, 240)))):
        x0 = 13 + dx
        draw.rectangle((x0, 11 - (1 if i == 1 else 0), x0 + 5, 19 - (1 if i == 1 else 0)), fill=rgba(color), outline=rgba((30, 30, 50)))
    draw.polygon([(16, 21), (17, 23), (19, 23), (17.5, 24.5), (18, 27), (16, 25.5), (14, 27), (14.5, 24.5), (13, 23), (15, 23)], fill=rgba((255, 230, 120)))
    return img


def make_card_back() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((7, 2, 24, 29), radius=2, fill=rgba((214, 210, 196)))
    draw.rectangle((9, 4, 22, 27), fill=rgba((26, 92, 88)))
    for y in range(4, 28):
        for x in range(9, 23):
            if (x + y) % 4 == 0:
                img.putpixel((x, y), rgba((36, 112, 106)))
    draw.polygon([(15.5, 9), (20, 15.5), (15.5, 22), (11, 15.5)], fill=rgba((230, 196, 90)), outline=rgba((120, 80, 30)))
    draw.ellipse((14, 14, 17, 17), fill=rgba((26, 92, 88)))
    return img


def make_icon(frames: dict) -> Image.Image:
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((4, 4, 123, 123), radius=22, fill=rgba((28, 30, 52)))
    for i, kind in enumerate(("pokemon_grass", "pokemon_water", "pokemon_fire")):
        card = frames[kind].crop((L.CARD[0], 0, L.CARD[2] + 1, 256)).resize((40, 56), Image.LANCZOS)
        rotated = card.rotate(25 - i * 25, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(rotated, (12 + i * 26, 8 + abs(i - 1) * 6))
    img.alpha_composite(make_booster_pack().resize((64, 64), Image.NEAREST), (32, 58))
    return img


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def read_cards(csv_path: Path):
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            yield {
                "number": int(row["number"]),
                "name": row["name"].strip(),
                "supertype": row["supertype"].strip(),
                "type": row["type"].strip() or None,
                "hp": int(row["hp"]) if row["hp"].strip() else None,
                "rarity": row["rarity"].strip(),
            }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-existing-art", action="store_true")
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    only = {int(n) for n in args.only.split(",") if n}

    frames = {f"pokemon_{kind}": L.pokemon_frame(kind) for kind in L.WEAKNESS}
    frames["trainer"] = L.trainer_frame()
    frames["energy"] = L.energy_frame()
    for name, img in frames.items():
        save(img, TEXTURES / "tcg" / "frame" / f"{name}.png")

    overlay, meta = L.holo_overlay()
    save(overlay, TEXTURES / "tcg" / "holo_overlay.png")
    (TEXTURES / "tcg" / "holo_overlay.png.mcmeta").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    save(make_booster_pack(), TEXTURES / "item" / "booster_pack.png")
    save(make_card_back(), TEXTURES / "item" / "tcg_card.png")
    save(make_icon(frames), RESOURCES / f"{NAMESPACE}.png")

    for csv_path in sorted(TOOLS.glob("*.csv")):
        set_name = csv_path.stem
        set_file = RESOURCES / "data" / NAMESPACE / "tcg" / "sets" / f"{set_name}.json"
        total = json.loads(set_file.read_text(encoding="utf-8"))["total"]
        written = 0
        for card in read_cards(csv_path):
            if only and card["number"] not in only:
                continue
            path = TEXTURES / "tcg" / set_name / f"{card['number']}.png"
            if args.skip_existing_art and path.exists():
                continue
            save(card_art(card, total), path)
            written += 1
        print(f"{set_name}: {written} card textures")


if __name__ == "__main__":
    main()
