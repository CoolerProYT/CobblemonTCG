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
  item/booster_pack/<set>_<wrapper>.png
                                booster pack wrappers listed in the set json (charizard, blastoise, venusaur)
  item/booster_pack.png         pack without set data
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
from art.wrapper import WRAPPERS, make_card_back, make_wrapper  # noqa: E402

NAMESPACE = "cobblemontcg"
TOOLS = Path(__file__).resolve().parent
RESOURCES = TOOLS.parent / "common" / "src" / "main" / "resources"
TEXTURES = RESOURCES / "assets" / NAMESPACE / "textures"


def rgba(c, a=255):
    return (*c, a)


def make_icon(frames: dict) -> Image.Image:
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((4, 4, 123, 123), radius=22, fill=rgba((28, 30, 52)))
    for i, kind in enumerate(("pokemon_grass", "pokemon_water", "pokemon_fire")):
        card = frames[kind].crop((L.CARD[0], 0, L.CARD[2] + 1, 256)).resize((40, 56), Image.LANCZOS)
        rotated = card.rotate(25 - i * 25, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(rotated, (12 + i * 26, 8 + abs(i - 1) * 6))
    img.alpha_composite(make_wrapper("charizard").resize((64, 64), Image.LANCZOS), (32, 58))
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

    save(make_wrapper(next(iter(WRAPPERS))), TEXTURES / "item" / "booster_pack.png")
    save(make_card_back(), TEXTURES / "item" / "tcg_card.png")
    save(make_icon(frames), RESOURCES / f"{NAMESPACE}.png")

    for csv_path in sorted(TOOLS.glob("*.csv")):
        set_name = csv_path.stem
        set_file = RESOURCES / "data" / NAMESPACE / "tcg" / "sets" / f"{set_name}.json"
        set_def = json.loads(set_file.read_text(encoding="utf-8"))
        total = set_def["total"]
        for wrapper in set_def.get("wrappers", []):
            if wrapper in WRAPPERS:
                save(make_wrapper(wrapper), TEXTURES / "item" / "booster_pack" / f"{set_name}_{wrapper}.png")
            else:
                print(f"warning: no artwork for wrapper {wrapper!r}, add it to tools/art/wrapper.py")
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
