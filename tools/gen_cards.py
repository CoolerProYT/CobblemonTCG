#!/usr/bin/env python3
"""
Generates card data and item models from the set CSVs in this folder.

For every tools/<set>.csv (e.g. base1.csv) it writes:
  data/cobblemontcg/tcg/cards/<set>/<number>.json         card data
  assets/cobblemontcg/models/item/tcg/<set>/<number>.json        regular print model
  assets/cobblemontcg/models/item/tcg/<set>/<number>_holo.json   holo print model
and finally assets/cobblemontcg/models/item/tcg_card.json with one
custom_model_data override per model, for all sets.

The set itself (name, pack slots, model_data_base) lives in
data/cobblemontcg/tcg/sets/<set>.json and is read, not written, by this script.
Card art is expected at assets/cobblemontcg/textures/tcg/<set>/<number>.png, frames at\ntextures/tcg/frame/<pokemon_type|trainer|energy>.png (see gen_card_art.py).

Usage: python tools/gen_cards.py
"""
import csv
import json
import shutil
from pathlib import Path

NAMESPACE = "cobblemontcg"
TOOLS = Path(__file__).resolve().parent
RESOURCES = TOOLS.parent / "common" / "src" / "main" / "resources"
DATA = RESOURCES / "data" / NAMESPACE / "tcg"
MODELS = RESOURCES / "assets" / NAMESPACE / "models" / "item"

SUPERTYPES = {"pokemon", "trainer", "energy"}
RARITIES = {"common", "uncommon", "rare", "rare_holo"}


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_cards(csv_path: Path) -> list[dict]:
    cards = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            supertype = row["supertype"].strip()
            rarity = row["rarity"].strip()
            if supertype not in SUPERTYPES:
                raise ValueError(f"{csv_path.name}: card {row['number']} has unknown supertype {supertype!r}")
            if rarity not in RARITIES:
                raise ValueError(f"{csv_path.name}: card {row['number']} has unknown rarity {rarity!r}")
            cards.append({
                "number": int(row["number"]),
                "name": row["name"].strip(),
                "supertype": supertype,
                "type": row["type"].strip() or None,
                "hp": int(row["hp"]) if row["hp"].strip() else None,
                "rarity": rarity,
            })
    return cards


def card_json(set_name: str, card: dict) -> dict:
    data = {
        "id": f"{set_name}-{card['number']}",
        "number": card["number"],
        "name": card["name"],
        "supertype": card["supertype"],
    }
    if card["type"]:
        data["type"] = card["type"]
    if card["hp"]:
        data["hp"] = card["hp"]
    data["rarity"] = card["rarity"]
    return data


def frame_name(card: dict) -> str:
    return f"pokemon_{card['type']}" if card["supertype"] == "pokemon" else card["supertype"]


def card_model(set_name: str, card: dict, holo: bool) -> dict:
    """Frame (shared per type), then the holo foil for holo prints, then the card's own art on top."""
    layers = [f"{NAMESPACE}:tcg/frame/{frame_name(card)}"]
    if holo:
        layers.append(f"{NAMESPACE}:tcg/holo_overlay")
    layers.append(f"{NAMESPACE}:tcg/{set_name}/{card['number']}")
    return {"parent": "minecraft:item/generated", "textures": {f"layer{i}": tex for i, tex in enumerate(layers)}}


def generate_set(csv_path: Path) -> list[tuple[int, str]]:
    set_name = csv_path.stem
    set_file = DATA / "sets" / f"{set_name}.json"
    if not set_file.exists():
        raise FileNotFoundError(f"{set_file} is missing, create the set definition first")
    set_def = json.loads(set_file.read_text(encoding="utf-8"))
    base = int(set_def["model_data_base"])

    cards = read_cards(csv_path)
    if len(cards) != set_def["total"]:
        print(f"warning: {set_name}.csv has {len(cards)} cards, set declares {set_def['total']}")

    for folder in (DATA / "cards" / set_name, MODELS / "tcg" / set_name):
        if folder.exists():
            shutil.rmtree(folder)

    overrides = []
    for card in cards:
        number = card["number"]
        write_json(DATA / "cards" / set_name / f"{number}.json", card_json(set_name, card))
        write_json(MODELS / "tcg" / set_name / f"{number}.json", card_model(set_name, card, False))
        write_json(MODELS / "tcg" / set_name / f"{number}_holo.json", card_model(set_name, card, True))
        # Must match TcgSet#modelData: base + number * 2 (+1 for holo)
        overrides.append((base + number * 2, f"{NAMESPACE}:item/tcg/{set_name}/{number}"))
        overrides.append((base + number * 2 + 1, f"{NAMESPACE}:item/tcg/{set_name}/{number}_holo"))

    print(f"{set_name}: {len(cards)} cards, custom_model_data {base + 2}..{base + cards[-1]['number'] * 2 + 1}")
    return overrides


def main() -> None:
    overrides = []
    for csv_path in sorted(TOOLS.glob("*.csv")):
        overrides.extend(generate_set(csv_path))

    values = [value for value, _ in overrides]
    if len(values) != len(set(values)):
        raise ValueError("custom_model_data ranges of two sets overlap, change model_data_base in a set json")

    # Overrides are matched in order and the last match wins, so they must be sorted ascending.
    overrides.sort()
    write_json(MODELS / "tcg_card.json", {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": f"{NAMESPACE}:item/tcg_card"},
        "overrides": [{"predicate": {"custom_model_data": value}, "model": model} for value, model in overrides],
    })
    print(f"tcg_card.json: {len(overrides)} overrides")


if __name__ == "__main__":
    main()
