#!/usr/bin/env python3
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


def read_text(set_name: str) -> dict[int, dict]:
    path = TOOLS / f"{set_name}_text.json"
    if not path.exists():
        return {}
    return {e["number"]: e for e in json.loads(path.read_text(encoding="utf-8"))}


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
    if card.get("pokedex"):
        data["pokedex"] = card["pokedex"]
    if card.get("evolves_from_pokedex"):
        data["evolves_from_pokedex"] = card["evolves_from_pokedex"]
    return data


def frame_name(card: dict) -> str:
    return f"pokemon_{card['type']}" if card["supertype"] == "pokemon" else card["supertype"]


CARD_PX = (256, 352)
ART_PX = (24, 40, 232, 184)
PACK_PX = (240, 368)

DISPLAY = {
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55, 0.55, 0.55]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "fixed": {"rotation": [0, 180, 0], "scale": [1, 1, 1]},
}


def r(v: float) -> float:
    return round(v, 4)


def body(width_px: int, height_px: int, thickness: float, front: str, back: str) -> dict:
    w = 16 * width_px / height_px
    x0, x1 = 8 - w / 2, 8 + w / 2
    z0, z1 = 8 - thickness / 2, 8 + thickness / 2
    edge = {"uv": [0, 1, 0.1, 15], "texture": back}
    return {
        "from": [r(x0), 0, r(z0)], "to": [r(x1), 16, r(z1)],
        "faces": {
            "south": {"uv": [0, 0, 16, 16], "texture": front},
            "north": {"uv": [0, 0, 16, 16], "texture": back},
            "east": edge, "west": edge,
            "up": {"uv": [4, 0.2, 12, 0.3], "texture": back},
            "down": {"uv": [4, 15.7, 12, 15.8], "texture": back},
        },
    }


def plane(x0_px, y0_px, x1_px, y1_px, z: float, texture: str, size_px=CARD_PX) -> dict:
    k = 16 / size_px[1]
    left = 8 - 16 * size_px[0] / size_px[1] / 2
    return {
        "from": [r(left + x0_px * k), r(16 - y1_px * k), r(z)], "to": [r(left + x1_px * k), r(16 - y0_px * k), r(z)],
        "faces": {"south": {"uv": [0, 0, 16, 16], "texture": texture}},
    }


def template(textures: dict, elements: list) -> dict:
    return {"gui_light": "front", "ambientocclusion": False, "textures": textures, "elements": elements, "display": DISPLAY}


CARD_THICKNESS = 0.2
PACK_THICKNESS = 0.8
MASCOT_Y_PX = 96
LAYER_GAP = 0.03
EVOLUTION_PX = (14, 13, 46, 37)


def write_templates() -> None:
    front_z = 8 + CARD_THICKNESS / 2
    back = f"{NAMESPACE}:tcg/card_back"
    for pokemon in (False, True):
        for evolution in ((False, True) if pokemon else (False,)):
            for holo in (False, True):
                elements = [body(*CARD_PX, CARD_THICKNESS, "#frame", "#back")]
                textures = {"back": back, "particle": "#frame"}
                if holo:
                    elements.append(plane(*ART_PX, front_z + LAYER_GAP, "#holo"))
                    textures["holo"] = f"{NAMESPACE}:tcg/holo_overlay"
                if pokemon:
                    elements.append(plane(*ART_PX, front_z + LAYER_GAP * 2, "#illustration"))
                elements.append(plane(0, 0, *CARD_PX, front_z + LAYER_GAP * 3, "#art"))
                if evolution:
                    portrait = plane(*EVOLUTION_PX, front_z + LAYER_GAP * 4, "#evolution")
                    portrait["faces"]["south"]["uv"] = [0, 0, 16, 12]
                    elements.append(portrait)
                name = "card" + ("_evolution" if evolution else "_pokemon" if pokemon else "") + ("_holo" if holo else "")
                write_json(MODELS / "tcg" / f"{name}.json", template(textures, elements))
    write_json(MODELS / "tcg" / "card_face_down.json", template(
        {"back": back, "particle": back}, [body(*CARD_PX, CARD_THICKNESS, "#back", "#back")]))
    pack_front_z = 8 + PACK_THICKNESS / 2
    write_json(MODELS / "tcg" / "pack.json", template(
        {"back": f"{NAMESPACE}:tcg/pack/back", "particle": "#front"}, [
            body(*PACK_PX, PACK_THICKNESS, "#front", "#back"),
            plane(0, MASCOT_Y_PX, PACK_PX[0], MASCOT_Y_PX + 208, pack_front_z + LAYER_GAP, "#mascot", PACK_PX),
            plane(0, 0, *PACK_PX, pack_front_z + LAYER_GAP * 2, "#overlay", PACK_PX),
        ]))


def card_model(set_name: str, card: dict, holo: bool) -> dict:
    base = f"{NAMESPACE}:tcg/{set_name}"
    textures = {"frame": f"{NAMESPACE}:tcg/frame/{set_name}/{frame_name(card)}", "art": f"{base}/{card['number']}"}
    parent = "card"
    if card["supertype"] == "pokemon":
        textures["illustration"] = f"{base}/illustration/{card['number']}"
        parent = "card_pokemon"
        if card.get("evolves_from_pokedex"):
            textures["evolution"] = f"{base}/evolution/{card['number']}"
            parent = "card_evolution"
    return {"parent": f"{NAMESPACE}:item/tcg/{parent}" + ("_holo" if holo else ""), "textures": textures}


def pack_textures(base: str) -> dict:
    return {"front": base, "mascot": f"{base}_mascot", "overlay": f"{base}_overlay"}


def generate_wrappers(set_name: str, set_def: dict) -> list[tuple[int, str]]:
    folder = MODELS / "booster_pack"
    overrides = []
    for i, wrapper in enumerate(set_def.get("wrappers", [])):
        write_json(folder / f"{set_name}_{wrapper}.json", {
            "parent": f"{NAMESPACE}:item/tcg/pack",
            "textures": pack_textures(f"{NAMESPACE}:tcg/pack/{set_name}_{wrapper}"),
        })
        overrides.append((int(set_def["model_data_base"]) + i, f"{NAMESPACE}:item/booster_pack/{set_name}_{wrapper}"))
    return overrides


def dex_numbers(csv_paths: list[Path]) -> dict[str, int]:
    dex = {}
    for csv_path in csv_paths:
        text = read_text(csv_path.stem)
        for card in read_cards(csv_path):
            number = text.get(card["number"], {}).get("dex")
            if card["supertype"] == "pokemon" and number:
                dex.setdefault(card["name"], number)
    return dex


def generate_set(csv_path: Path, dex_by_name: dict[str, int]) -> list[tuple[int, str]]:
    set_name = csv_path.stem
    set_file = DATA / "sets" / f"{set_name}.json"
    if not set_file.exists():
        raise FileNotFoundError(f"{set_file} is missing, create the set definition first")
    set_def = json.loads(set_file.read_text(encoding="utf-8"))
    base = int(set_def["model_data_base"])

    cards = read_cards(csv_path)
    text = read_text(set_name)
    for card in cards:
        entry = text.get(card["number"], {})
        if card["supertype"] == "pokemon":
            card["pokedex"] = entry.get("dex")
            card["evolves_from_pokedex"] = dex_by_name.get(entry.get("evolvesFrom"))
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
        overrides.append((base + number * 2, f"{NAMESPACE}:item/tcg/{set_name}/{number}"))
        overrides.append((base + number * 2 + 1, f"{NAMESPACE}:item/tcg/{set_name}/{number}_holo"))

    print(f"{set_name}: {len(cards)} cards, custom_model_data {base + 2}..{base + cards[-1]['number'] * 2 + 1}")
    return overrides


def main() -> None:
    write_templates()
    overrides = []
    pack_overrides = []
    csv_paths = sorted(TOOLS.glob("*.csv"))
    dex_by_name = dex_numbers(csv_paths)
    for csv_path in csv_paths:
        overrides.extend(generate_set(csv_path, dex_by_name))
        set_def = json.loads((DATA / "sets" / f"{csv_path.stem}.json").read_text(encoding="utf-8"))
        pack_overrides.extend(generate_wrappers(csv_path.stem, set_def))

    values = [value for value, _ in overrides]
    if len(values) != len(set(values)):
        raise ValueError("custom_model_data ranges of two sets overlap, change model_data_base in a set json")

    overrides.sort()
    write_json(MODELS / "tcg_card.json", {
        "parent": f"{NAMESPACE}:item/tcg/card_face_down",
        "overrides": [{"predicate": {"custom_model_data": value}, "model": model} for value, model in overrides],
    })
    print(f"tcg_card.json: {len(overrides)} overrides")

    pack_overrides.sort()
    write_json(MODELS / "booster_pack.json", {
        "parent": f"{NAMESPACE}:item/tcg/pack",
        "textures": pack_textures(f"{NAMESPACE}:tcg/pack/default"),
        "overrides": [{"predicate": {"custom_model_data": value}, "model": model} for value, model in pack_overrides],
    })
    print(f"booster_pack.json: {len(pack_overrides)} wrapper overrides")


if __name__ == "__main__":
    main()
