# Set files

`data/<namespace>/tcg/sets/<set>.json`. The Base Set file:

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

| Field | Required | Description |
| --- | --- | --- |
| `name` | yes | Shown on packs (`Base Set Booster Pack`), tooltips and in commands |
| `total` | yes | Printed card count, shown as `4/102` |
| `model_data_base` | yes | Start of the set's `custom_model_data` range. Give every set its own range: Base Set uses 1000, Jungle 2000 |
| `wrappers` | no | The pack designs, picked at random for each pack. Default `["default"]` |
| `wrapper_pokedex` | no | National Pokédex number per wrapper: Cobblemon's model of that Pokémon is drawn as the pack's mascot |
| `pack_slots` | yes | What a pack holds, see below |

## Pack slots

Each slot rolls `count` cards. For every card it picks a rarity from the `rarities` weights, then a random card of that rarity. A card never appears twice in a pack: a rarity that has no unused cards left is skipped.

| Field | Description |
| --- | --- |
| `count` | Cards rolled by this slot |
| `rarities` | Weight per rarity: `common`, `uncommon`, `rare`, `rare_holo` |
| `use_config_holo_chance` | When `true`, `rare_holo` gets exactly the [`packs.holoChance`](/guide/configuration#packs) chance and the other rarities share the rest by their weights |

With `packs.packSize` different from the slot total, the difference is added to or taken from the last slots.

Cards of a `rare_holo` rarity come out of packs as holo prints; all others as regular prints.

## Models and textures

Card stacks use `custom_model_data = model_data_base + number * 2` for the regular print and `+ 1` for the holo print. Packs use `model_data_base + wrapper index`. Every wrapper needs textures at `assets/cobblemontcg/textures/tcg/pack/<set>_<wrapper>.png`, `_mascot.png` and `_overlay.png`; see [Textures & art](./textures).
