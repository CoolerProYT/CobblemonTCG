# Cobblemon: TCG

A trading card mod for Minecraft 1.21.1 (Fabric and NeoForge). Open booster packs and collect cards.
The first set is the 1999 Base Set: 102 cards, with real pack odds.

## Disclaimer

This is an unofficial fan project. It is not affiliated with, endorsed, sponsored or approved by
Nintendo, The Pokémon Company, Game Freak or Creatures Inc. Pokémon and all related names are
trademarks of their respective owners. The mod contains card metadata only (names, numbers, types,
HP, rarities). All textures are original fan illustrations drawn for this mod; no official card
scans, card art, card text, pack wrappers, set logos or expansion symbols are included.

## Features

- **Booster packs**: right-click to open. A pack holds 11 cards, like a real Base Set pack:
  1 rare slot (holo rare about 1 in 3 packs, configurable), 3 uncommons and 7 commons
  (basic Energy is part of the commons). No card appears twice in the same pack.
- **Cards**: 102 Base Set cards, each with a regular and a holo print. Holo prints have an animated
  shimmer. Tooltips show number, rarity, card type, HP, energy type and holo.
- **Commands** (operators only):
  - `/tcg give pack <set> [amount]`
  - `/tcg give card <set> <number> [holo]`

  `<set>` accepts `cobblemontcg:base1` or just `base1`.
- **Creative tab** "Cobblemon: TCG" with every pack and card.

## Configuration

`config/cobblemontcg-common.toml` (requires [CoolerConfig](https://github.com/CoolerProYT/CoolerConfig), bundled):

| Key | Default | Description |
| --- | --- | --- |
| `packs.holoChance` | `0.333` | Chance that the rare slot is a holo rare |
| `packs.packSize` | `11` | Cards per pack; the difference is applied to the last slots (commons) |
| `effects.soundsEnabled` | `true` | Pack opening sounds |
| `rewards.enabled` | `false` | Allow reward triggers to hand out packs |
| `rewards.dailyPackCap` | `10` | Reward packs per player per day (UTC), `0` = unlimited. Commands are not limited |

## Data packs

Everything about a set is data driven, so new sets need no code.

### Sets: `data/<namespace>/tcg/sets/<set>.json`

```json
{
  "name": "Base Set",
  "total": 102,
  "model_data_base": 1000,
  "wrappers": ["default"],
  "pack_slots": [
    { "count": 1, "rarities": { "rare_holo": 1, "rare": 2 }, "use_config_holo_chance": true },
    { "count": 3, "rarities": { "uncommon": 1 } },
    { "count": 7, "rarities": { "common": 1 } }
  ]
}
```

Each slot rolls a rarity from its weight table, then a card of that rarity. With
`use_config_holo_chance`, the `rare_holo` chance comes from `packs.holoChance` instead.

### Cards: `data/<namespace>/tcg/cards/<set>/<number>.json`

```json
{ "id": "base1-4", "number": 4, "name": "Charizard", "supertype": "pokemon", "type": "fire", "hp": 120, "rarity": "rare_holo" }
```

`supertype` is `pokemon`, `trainer` or `energy`; `rarity` is `common`, `uncommon`, `rare` or `rare_holo`.
`type` and `hp` are optional.

### Reward rules: `data/<namespace>/tcg/rewards/*.json`

No rules ship with the mod. A file holds one rule or a list of rules:

```json
{
  "trigger": "cobblemontcg:capture",
  "set": "cobblemontcg:base1",
  "amount": 1,
  "chance": 0.05,
  "conditions": { "min_level": 20, "species": ["pikachu"], "shiny": true }
}
```

Rules only fire when `rewards.enabled` is true and are limited by `rewards.dailyPackCap`.
Triggers are registered in code through `RewardTriggerRegistry`; none are registered yet.

## Art

Cards follow the layout of a 1999 Base Set card (yellow border, face coloured by type, name and HP,
framed art window, attack rows, weakness / resistance / retreat, number and rarity symbol), drawn
from scratch. Each card model stacks up to three 256×256 layers:

| Layer | Texture | Shared |
| --- | --- | --- |
| Frame | `assets/cobblemontcg/textures/tcg/frame/<pokemon_<type>\|trainer\|energy>.png` | per type: border, face, art window background, labels |
| Holo foil (holo prints only) | `assets/cobblemontcg/textures/tcg/holo_overlay.png` (+ `.mcmeta`) | all cards, animated |
| Card art | `assets/cobblemontcg/textures/tcg/<set>/<number>.png` | one per card: name, HP, illustration, costs, number, rarity |

The card sits in the middle of the texture (x 36 to 219); the art window is x 51 to 204, y 29 to 120.
On a holo print the foil shows through wherever the card art is transparent, so leave the art
window background transparent to keep the holo effect, or paint over it for a full-art card.
Replace any texture with your own drawing of the same size and name, no code changes needed.

| Other texture | Size |
| --- | --- |
| `assets/cobblemontcg/textures/item/booster_pack.png` (pack wrapper) | 32×32 |
| `assets/cobblemontcg/textures/item/tcg_card.png` (card back, cards without a model) | 32×32 |

## Tools

Requires Python 3.10+, Pillow 10.1+ and numpy (`pip install pillow numpy`).

- `tools/<set>.csv`: the card list (`number,name,supertype,type,hp,rarity`).
- `python tools/gen_cards.py`: writes the card JSONs, one model per card print and the
  `custom_model_data` overrides in `models/item/tcg_card.json` for every CSV.
- `python tools/gen_card_art.py [--skip-existing-art] [--only 4,58]`: draws the frames, holo foil,
  card art, pack wrapper, card back and mod icon. `--skip-existing-art` keeps card art you have
  already replaced. The illustrations live in `tools/art/pokemon_base1.py` and
  `tools/art/trainers_base1.py`, one small function per card; the layout is in `tools/art/layout.py`.

Card stacks use `custom_model_data = model_data_base + number * 2` for the regular print and `+ 1`
for the holo print, so give every set its own `model_data_base` range.

## Building

```
./gradlew build
./gradlew :fabric:runClient
./gradlew :neoforge:runClient
```
