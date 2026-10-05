#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art import layout as L
from art.cards import card_layers, frame_name
from art.wrapper import DEFAULT, SETS, make_card_back, make_pack_back, make_wrapper, make_wrapper_layers

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
    pack = make_wrapper(*DEFAULT).resize((42, 64), Image.LANCZOS)
    img.alpha_composite(pack, (43, 56))
    return img


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def save_pack(layers: dict, name: str) -> None:
    save(layers["base"], TCG / "pack" / f"{name}.png")
    save(layers["mascot"], TCG / "pack" / f"{name}_mascot.png")
    save(layers["overlay"], TCG / "pack" / f"{name}_overlay.png")


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
    parser.add_argument("--set", default="")
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    only = {int(n) for n in args.only.split(",") if n}

    frames = {f"pokemon_{kind}": L.pokemon_frame(kind) for kind in L.TYPE_COLORS}

    overlay, meta = L.holo_overlay()
    save(overlay, TCG / "holo_overlay.png")
    (TCG / "holo_overlay.png.mcmeta").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    save(make_card_back(), TCG / "card_back.png")
    save(make_pack_back(), TCG / "pack" / "back.png")
    save_pack(make_wrapper_layers(*DEFAULT), "default")
    save(make_icon(frames), RESOURCES / f"{NAMESPACE}.png")

    csv_paths = sorted(TOOLS.glob("*.csv"))
    everywhere = {}
    for csv_path in csv_paths:
        for c in read_cards(csv_path):
            if c["supertype"] == "pokemon":
                everywhere.setdefault(c["name"], (csv_path.stem, c["number"]))

    for csv_path in csv_paths:
        set_name = csv_path.stem
        set_file = RESOURCES / "data" / NAMESPACE / "tcg" / "sets" / f"{set_name}.json"
        set_def = json.loads(set_file.read_text(encoding="utf-8"))
        total = set_def["total"]
        for wrapper in set_def.get("wrappers", []):
            if wrapper in SETS.get(set_name, ("", {}))[1]:
                save_pack(make_wrapper_layers(set_name, wrapper), f"{set_name}_{wrapper}")
            else:
                print(f"warning: no artwork for wrapper {wrapper!r}, add it to tools/art/wrapper.py")
        text_file = TOOLS / f"{set_name}_text.json"
        texts = {e["number"]: e for e in json.loads(text_file.read_text(encoding="utf-8"))} if text_file.exists() else {}
        cards = list(read_cards(csv_path))
        for kind in sorted({frame_name(c) for c in cards} if not args.set or args.set == set_name else ()):
            if kind.startswith("pokemon_"):
                frame = L.pokemon_frame(kind[len("pokemon_"):], set_name)
            else:
                frame = L.trainer_frame(set_name) if kind == "trainer" else L.energy_frame(set_name)
            save(frame, TCG / "frame" / set_name / f"{kind}.png")
        by_name = {**everywhere, **{c["name"]: (set_name, c["number"]) for c in cards if c["supertype"] == "pokemon"}}
        written = 0
        for card in cards:
            card["set"], card["set_title"] = set_name, set_def["name"]
            if (args.set and set_name != args.set) or (only and card["number"] not in only):
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
