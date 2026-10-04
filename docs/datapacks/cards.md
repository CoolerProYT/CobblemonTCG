# Card files

`data/<namespace>/tcg/cards/<set>/<number>.json`, one file per card. Base Set's Charizard:

```json
{ "id": "base1-4", "number": 4, "name": "Charizard", "supertype": "pokemon", "type": "fire", "hp": 120, "rarity": "rare_holo", "pokedex": 6, "evolves_from_pokedex": 5 }
```

| Field | Required | Description |
| --- | --- | --- |
| `id` | yes | A unique name, like `base1-4` |
| `number` | yes | Number in the set. Two cards with the same number replace each other |
| `name` | yes | Card name, shown in the tooltip |
| `supertype` | yes | `pokemon`, `trainer` or `energy` |
| `type` | no | `grass`, `fire`, `water`, `lightning`, `psychic`, `fighting` or `colorless` |
| `hp` | no | Hit points |
| `rarity` | yes | `common`, `uncommon`, `rare` or `rare_holo` |
| `pokedex` | no | National Pokédex number: Cobblemon's model of this Pokémon is drawn in the art window |
| `evolves_from_pokedex` | no | National Pokédex number of the previous stage, drawn in the evolution portrait |

A card can evolve from a Pokémon of an earlier set, like Jungle's Clefable from Base Set's Clefairy: `evolves_from_pokedex` is only a Pokédex number.

Attacks, Pokémon Powers, weakness and retreat cost are not part of the card file: they are printed on the card texture. The [set pages](/sets/) of this wiki read them from `tools/<set>_text.json`.
