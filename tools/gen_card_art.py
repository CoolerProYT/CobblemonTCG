#!/usr/bin/env python3
"""
Draws the card textures: original illustrations in a layout inspired by the 1999 Base Set.
No official card art, scans, logos or set symbols are used. Replace any file with your own
drawing of the same size and name, no code changes needed.

Writes into common/src/main/resources/assets/cobblemontcg/textures/tcg/:
  frame/pokemon_<type>.png, trainer.png, energy.png
                            card frame, face and art window background (256x352)
  holo_overlay.png(.mcmeta) animated foil over the art window, holo prints only (208x144 per frame)
  <set>/<number>.png        everything specific to one card: name, HP, attacks, weakness /
                            resistance / retreat, number, rarity; trainer and energy art (256x352)
  <set>/illustration/<number>.png
                            the Pokemon in the art window, Pokemon cards only (208x144)
  <set>/evolution/<number>.png
                            the previous stage in the portrait window, evolution cards only (32x32)
  card_back.png             back of every card (256x352)
  pack/<set>_<wrapper>.png  booster pack fronts listed in the set json (240x368)
  pack/back.png             back of every pack (240x368)
  pack/default.png          pack without set data (240x368)
and the mod icon common/src/main/resources/cobblemontcg.png.

Card text (attacks, costs, damage, rules) is read from tools/<set>_text.json.

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
from art.cards import card_layers  # noqa: E402
from art.wrapper import WRAPPERS, make_card_back, make_pack_back, make_wrapper  # noqa: E402

NAMESPACE = "cobblemontcg"
TOOLS = Path(__file__).resolve().parent
RESOURCES = TOOLS.parent / "common" / "src" / "main" / "resources"
TCG = RESOURCES / "assets" / NAMESPACE / "textures" / "tcg"


def rgba(c, a=255):
    return (*c, a)


def make_icon(frames: dict) -> Image.Image:
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((4, 4, 123, 123), radius=22, fill=rgba((28, 30, 52)))
    for i, kind in enumerate(("pokemon_grass", "pokemon_water", "pokemon_fire")):
        card = frames[kind].resize((40, 55), Image.LANCZOS)
        rotated = card.rotate(25 - i * 25, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(rotated, (12 + i * 26, 8 + abs(i - 1) * 6))
    pack = make_wrapper(next(iter(WRAPPERS))).resize((42, 64), Image.LANCZOS)
    img.alpha_composite(pack, (43, 56))
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

    frames = {f"pokemon_{kind}": L.pokemon_frame(kind) for kind in L.TYPE_COLORS}
    frames["trainer"] = L.trainer_frame()
    frames["energy"] = L.energy_frame()
    for name, img in frames.items():
        save(img, TCG / "frame" / f"{name}.png")

    overlay, meta = L.holo_overlay()
    save(overlay, TCG / "holo_overlay.png")
    (TCG / "holo_overlay.png.mcmeta").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    save(make_card_back(), TCG / "card_back.png")
    save(make_pack_back(), TCG / "pack" / "back.png")
    save(make_wrapper(next(iter(WRAPPERS))), TCG / "pack" / "default.png")
    save(make_icon(frames), RESOURCES / f"{NAMESPACE}.png")

    for csv_path in sorted(TOOLS.glob("*.csv")):
        set_name = csv_path.stem
        set_file = RESOURCES / "data" / NAMESPACE / "tcg" / "sets" / f"{set_name}.json"
        set_def = json.loads(set_file.read_text(encoding="utf-8"))
        total = set_def["total"]
        for wrapper in set_def.get("wrappers", []):
            if wrapper in WRAPPERS:
                save(make_wrapper(wrapper), TCG / "pack" / f"{set_name}_{wrapper}.png")
            else:
                print(f"warning: no artwork for wrapper {wrapper!r}, add it to tools/art/wrapper.py")
        text_file = TOOLS / f"{set_name}_text.json"
        texts = {e["number"]: e for e in json.loads(text_file.read_text(encoding="utf-8"))} if text_file.exists() else {}
        cards = list(read_cards(csv_path))
        by_name = {c["name"]: c["number"] for c in cards if c["supertype"] == "pokemon"}
        written = 0
        for card in cards:
            if only and card["number"] not in only:
                continue
            path = TCG / set_name / f"{card['number']}.png"
            if args.skip_existing_art and path.exists():
                continue
            layers = card_layers(card, total, texts.get(card["number"], {}), by_name)
            save(layers["card"], path)
            for name in ("illustration", "evolution"):
                if name in layers:
                    save(layers[name], TCG / set_name / name / f"{card['number']}.png")
            written += 1
        print(f"{set_name}: {written} card textures")


if __name__ == "__main__":
    main()
