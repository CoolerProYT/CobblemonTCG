# Cobblemon: TCG

A trading card addon for [Cobblemon](https://cobblemon.com) on Minecraft 1.21.1 (Fabric and NeoForge).
Open booster packs and collect cards. The first set is the 1999 Base Set: 102 cards, with real pack odds.

**Requires Cobblemon 1.8.1 or newer**: the game will not start if Cobblemon is missing.

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
- **Card Dealer**: a villager profession whose job site is the Card Dealer Table (2 paper, 1
  booster pack, 5 planks: paper / pack / paper on top, planks below in a table shape). The novice
  trade sells a booster pack for 5 emeralds, 3 times per restock (configurable).
- **Creative tab** "Cobblemon: TCG" with every pack and card.

## Configuration

`config/cobblemontcg-common.toml` (requires [CoolerConfig](https://github.com/CoolerProYT/CoolerConfig), bundled):

| Key | Default | Description |
| --- | --- | --- |
| `packs.holoChance` | `0.333` | Chance that the rare slot is a holo rare |
| `packs.packSize` | `11` | Cards per pack; the difference is applied to the last slots (commons) |
| `effects.soundsEnabled` | `true` | Pack opening sounds |
| `rewards.enabled` | `true` | Allow reward triggers to hand out packs |
| `rewards.dailyPackCap` | `10` | Reward packs per player per day (UTC), `0` = unlimited. Commands are not limited |
| `rewards.triggers.capture` | `true` | Packs for catching Pokémon (Cobblemon) |
| `rewards.triggers.levelUp` | `true` | Packs for level milestones (Cobblemon) |
| `rewards.triggers.dexProgress` | `true` | Packs for Pokédex milestones (Cobblemon) |
| `shop.setId` | `cobblemontcg:base1` | Set of the booster packs villagers sell |
| `shop.cardDealer.enabled` | `true` | Card Dealer villagers sell booster packs |
| `shop.cardDealer.price` | `5` | Emeralds per pack at the Card Dealer |
| `shop.cardDealer.maxUses` | `3` | Packs a Card Dealer sells before restocking |

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
  "wrapper_pokedex": { "charizard": 6, "blastoise": 9, "venusaur": 3 },
  "pack_slots": [
    { "count": 1, "rarities": { "rare_holo": 1, "rare": 2 }, "use_config_holo_chance": true },
    { "count": 3, "rarities": { "uncommon": 1 } },
    { "count": 7, "rarities": { "common": 1 } }
  ]
}
```

`wrappers` lists the pack designs; each name needs textures at
`assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>.png`, `<set>_<wrapper>_mascot.png` and
`<set>_<wrapper>_overlay.png` (and a model, written by
`tools/gen_cards.py`). Each slot rolls a rarity from its weight table, then a card of that rarity. With
`use_config_holo_chance`, the `rare_holo` chance comes from `packs.holoChance` instead.

### Cards: `data/<namespace>/tcg/cards/<set>/<number>.json`

```json
{ "id": "base1-4", "number": 4, "name": "Charizard", "supertype": "pokemon", "type": "fire", "hp": 120, "rarity": "rare_holo", "pokedex": 6, "evolves_from_pokedex": 5 }
```

`supertype` is `pokemon`, `trainer` or `energy`; `rarity` is `common`, `uncommon`, `rare` or `rare_holo`.
`type`, `hp`, `pokedex` and `evolves_from_pokedex` are optional. The last two are National Pokédex
numbers, used to draw Cobblemon's models on the card.

### Reward rules: `data/<namespace>/tcg/rewards/*.json`

A file holds one rule or a list of rules. When the rule's trigger fires and its conditions pass, the
player gets `amount` packs of `set` with probability `chance` (default `1`):

```json
{
  "trigger": "cobblemontcg:capture",
  "set": "cobblemontcg:base1",
  "amount": 1,
  "chance": 0.05,
  "conditions": { "min_level": 20, "species": ["pikachu"], "shiny": true }
}
```

Rules only fire when `rewards.enabled` and the trigger's toggle are on, and are limited by
`rewards.dailyPackCap`.

#### Pokémon rewards

These triggers come from Cobblemon's events:

| Trigger | When | Conditions |
| --- | --- | --- |
| `cobblemontcg:capture` | the player catches a Pokémon | `species`, `shiny`, `min_level`, `first_catch_of_species` |
| `cobblemontcg:level_up` | one of the player's Pokémon levels up | `level`, `species`, `shiny` |
| `cobblemontcg:dex_progress` | the player owns a new species in the Pokédex | `dex_every`, `dex_percent` |

- `species`: species names like `pikachu` (any of them matches).
- `first_catch_of_species: true`: the player has never owned this species before.
- `level: 25`: a Pokémon of the player reached level 25 or higher.
- `dex_every: 10`: the player now owns a multiple of 10 species.
- `dex_percent: 50`: the player owns at least 50% of the species in Cobblemon's Pokédex.

`level`, `dex_every`, `dex_percent` and `first_catch_of_species: true` are milestones: each pays out
at most once per player (claimed milestones are saved on the player). A milestone is claimed when its
rule rolls its chance, win or lose; when no pack can be given because of the daily cap it stays open for
the next event. Other rules (like shiny catches) pay out every time.

Default rules shipped in `data/cobblemontcg/tcg/rewards/` (override a file with the same path in a
data pack, or replace it with `[]`, to change or remove them):

| File | Rule |
| --- | --- |
| `capture.json` | first catch of a species: 10% chance of 1 pack; shiny catch: 1 pack |
| `level_up.json` | level 10, 25, 50 and 100: 1 pack each |
| `dex_progress.json` | 25% and 50% of the Pokédex: 1 pack; 75% and 100%: 2 packs |

Other mods can add triggers through `RewardTriggerRegistry`.

## Art

Cards follow the layout of a 1999 Base Set card (yellow border, face coloured by type, stage line,
name and HP, framed art window, Pokémon Powers and attacks with energy costs and damage,
weakness / resistance / retreat, level, number and rarity symbol), drawn from scratch.

Cards and packs are thin 3D models with a real back: a held, dropped or framed card shows the card
back, and a pack shows the back of the wrapper. In the opening animation each card is dealt face
down and flips over. A card model stacks these layers on its front, back to front:

| Layer | Texture | Shared |
| --- | --- | --- |
| Frame | `assets/cobblemontcg/textures/tcg/frame/<pokemon_<type>\|trainer\|energy>.png`, 256×352 | per type: border, face, art window background, labels |
| Holo foil (holo prints only) | `assets/cobblemontcg/textures/tcg/holo_overlay.png` (+ `.mcmeta`), 208×144 per frame | all cards, animated, covers the art window only |
| Illustration (Pokémon only) | `assets/cobblemontcg/textures/tcg/<set>/illustration/<number>.png`, 208×144 | one per card: the Pokémon in the art window |
| Card text | `assets/cobblemontcg/textures/tcg/<set>/<number>.png`, 256×352 | one per card: name, HP, attacks, number, rarity; trainer and energy art |
| Evolution portrait (evolution cards only) | `assets/cobblemontcg/textures/tcg/<set>/evolution/<number>.png`, 32×32 (picture in the top 32×24) | one per card: the previous stage |

### Cobblemon models

The client draws Cobblemon's own models into the illustration and evolution portrait of every card that
has a `pokedex` / `evolves_from_pokedex` number, and into the mascot of every pack wrapper listed in
the set's `wrapper_pokedex`, posed like in Cobblemon's Pokédex. This happens a few
cards per tick after joining a world (Cobblemon's species arrive then) and again after a resource
reload. Until then, and for species Cobblemon has not implemented, the drawn art is shown.
Nothing from Cobblemon is copied into this mod.

The texture is the whole card (63 × 88 mm); the art window is x 24 to 231, y 40 to 183.
On a holo print the foil shows through wherever the card art is transparent, so leave the art
window background transparent to keep the holo effect, or paint over it for a full-art card.
Replace any texture with your own drawing of the same size and name (for example in a resource
pack), no code changes needed.

| Other texture | Size |
| --- | --- |
| `assets/cobblemontcg/textures/tcg/card_back.png` (back of every card, and cards without data) | 256×352 |
| `assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>.png` (pack front: foil and light burst) | 240×368 |
| `assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>_mascot.png` (pack mascot, drawn from y 96 of the pack) | 240×208 |
| `assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>_overlay.png` (set name plate, badges, seals and foil sheen, over the mascot) | 240×368 |
| `assets/cobblemontcg/textures/tcg/pack/back.png` (back of every pack) | 240×368 |
| `assets/cobblemontcg/textures/tcg/pack/default.png`, `default_mascot.png`, `default_overlay.png` (pack without set data) | as above |

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
./gradlew :neoforge:runClient   # dev client, with Cobblemon
```

The NeoForge dev runs include Cobblemon. The Fabric dev client does not start: the mod requires
Cobblemon, and Cobblemon's Fabric build does not run in a Fabric dev environment, so test on NeoForge.
