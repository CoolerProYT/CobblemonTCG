# Cobblemon: TCG

A trading card mod for Minecraft 1.21.1 (Fabric and NeoForge). Open booster packs and collect cards.
The first set is the 1999 Base Set: 102 cards, with real pack odds.

## Disclaimer

This is an unofficial fan project. It is not affiliated with, endorsed, sponsored or approved by
Nintendo, The Pokémon Company, Game Freak or Creatures Inc. Pokémon and all related names are
trademarks of their respective owners. The mod contains card metadata and game text (names,
numbers, types, HP, rarities, attacks, costs, damage, weakness / resistance / retreat and rules
text). All textures are original fan illustrations drawn for this mod; no official card scans,
card art, flavour text, pack wrappers, set logos, card backs or expansion symbols are included.

## Features

- **Booster packs**: a pack holds 11 cards, like a real Base Set pack: 1 rare slot (holo rare
  about 1 in 3 packs, configurable), 3 uncommons and 7 commons (basic Energy is part of the
  commons). No card appears twice in the same pack. Like the real set, every pack comes in one of
  three wrappers (Charizard, Blastoise or Venusaur art), picked at random.
- **Opening animation**: right-click a pack and it tears open; swipe the cards away one by one
  (drag, click, or Space / arrow keys). Commons come first and the rare last, with a burst of light
  and a sound for rares and holos, then a summary of every pull. The cards are already in your
  inventory when the animation starts, so closing it early never loses anything.
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

`config/cobblemontcg-client.toml`:

| Key | Default | Description |
| --- | --- | --- |
| `packOpening.animation` | `true` | Show the opening animation; when off, cards go straight to the inventory |

## Data packs

Everything about a set is data driven, so new sets need no code.

### Sets: `data/<namespace>/tcg/sets/<set>.json`

```json
{
  "name": "Base Set",
  "total": 102,
  "model_data_base": 1000,
  "wrappers": ["charizard", "blastoise", "venusaur"],
  "pack_slots": [
    { "count": 1, "rarities": { "rare_holo": 1, "rare": 2 }, "use_config_holo_chance": true },
    { "count": 3, "rarities": { "uncommon": 1 } },
    { "count": 7, "rarities": { "common": 1 } }
  ]
}
```

`wrappers` lists the pack designs; each name needs a texture at
`assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>.png` (and a model, written by
`tools/gen_cards.py`). Each slot rolls a rarity from its weight table, then a card of that rarity. With
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

Cards follow the layout of a 1999 Base Set card (yellow border, face coloured by type, stage line,
name and HP, framed art window, Pokémon Powers and attacks with energy costs and damage,
weakness / resistance / retreat, level, number and rarity symbol), drawn from scratch.

Cards and packs are thin 3D models with a real back: a held, dropped or framed card shows the card
back, and a pack shows the back of the wrapper. In the opening animation each card is dealt face
down and flips over. A card model stacks up to three 256×352 layers on its front:

| Layer | Texture | Shared |
| --- | --- | --- |
| Frame | `assets/cobblemontcg/textures/tcg/frame/<pokemon_<type>\|trainer\|energy>.png` | per type: border, face, art window background, labels |
| Holo foil (holo prints only) | `assets/cobblemontcg/textures/tcg/holo_overlay.png` (+ `.mcmeta`), 208×144 per frame | all cards, animated, covers the art window only |
| Card art | `assets/cobblemontcg/textures/tcg/<set>/<number>.png` | one per card: name, HP, illustration, attacks, number, rarity |

The texture is the whole card (63 × 88 mm); the art window is x 24 to 231, y 40 to 183.
On a holo print the foil shows through wherever the card art is transparent, so leave the art
window background transparent to keep the holo effect, or paint over it for a full-art card.
Replace any texture with your own drawing of the same size and name (for example in a resource
pack), no code changes needed.

| Other texture | Size |
| --- | --- |
| `assets/cobblemontcg/textures/tcg/card_back.png` (back of every card, and cards without data) | 256×352 |
| `assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>.png` (pack fronts) | 240×368 |
| `assets/cobblemontcg/textures/tcg/pack/back.png` (back of every pack) | 240×368 |
| `assets/cobblemontcg/textures/tcg/pack/default.png` (pack without set data) | 240×368 |

The model templates live in `assets/cobblemontcg/models/item/tcg/` (`card.json`, `card_holo.json`,
`card_face_down.json`, `pack.json`) and are written by `tools/gen_cards.py`.

## Tools

Requires Python 3.10+, Pillow 10.1+ and numpy (`pip install pillow numpy`).

- `tools/<set>.csv`: the card list (`number,name,supertype,type,hp,rarity`).
- `tools/<set>_text.json`: game text drawn on the cards (stage, evolves from, level, Pokédex number,
  Pokémon Powers, attacks, weakness, resistance, retreat cost, trainer and energy rules).
  For `base1` it was taken from the community card database
  [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data).
- `tools/fonts/`: Cabin by Pablo Impallari and Rodrigo Fuenzalida, under the SIL Open Font License
  (`tools/fonts/OFL.txt`), used only to draw the textures.
- `python tools/gen_cards.py`: writes the card JSONs, one model per card print and the
  `custom_model_data` overrides in `models/item/tcg_card.json` for every CSV, plus one model per
  pack wrapper and their overrides in `models/item/booster_pack.json`.
- `python tools/gen_card_art.py [--skip-existing-art] [--only 4,58]`: draws the frames, holo foil,
  card art, pack fronts and back (`tools/art/wrapper.py`), card back and mod icon (about 1.5 minutes). `--skip-existing-art` keeps card art you have
  already replaced. The illustrations live in `tools/art/pokemon_base1.py` and
  `tools/art/trainers_base1.py`, one small function per card, lit and shaded by
  `tools/art/canvas.py`; the layout is in `tools/art/layout.py`, the per-card text in
  `tools/art/cards.py`.

Card stacks use `custom_model_data = model_data_base + number * 2` for the regular print and `+ 1`
for the holo print, so give every set its own `model_data_base` range. Packs use
`model_data_base + wrapper index`.

## Building

```
./gradlew build
./gradlew :fabric:runClient
./gradlew :neoforge:runClient
```
