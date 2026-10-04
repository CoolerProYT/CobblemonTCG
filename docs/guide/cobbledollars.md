# CobbleDollars

[CobbleDollars](https://modrinth.com/mod/cobbledollars) is optional: the mod does not need it and uses none of its code. Its merchants can still sell booster packs through CobbleDollars' own shop config. Tested with CobbleDollars 2.0.0+Beta-6.1 for 1.21.1.

## Adding packs to the shop

Add this category to the list in `config/cobbledollars/default_shop.json`:

```json
{
  "name": "Cobblemon TCG",
  "offers": [
    {
      "item": "cobblemontcg:booster_pack",
      "price": "2500",
      "components": {
        "cobblemontcg:booster_pack": { "set": "cobblemontcg:base1", "variant": "charizard" },
        "minecraft:custom_model_data": 1000
      }
    }
  ]
}
```

The `cobblemontcg:booster_pack` component is required: a pack without it does not open. `variant` is the wrapper, and `custom_model_data` picks its texture. They have to match:

| Set | `set` | `variant` → `custom_model_data` |
| --- | --- | --- |
| Base Set | `cobblemontcg:base1` | `charizard` 1000, `blastoise` 1001, `venusaur` 1002 |
| Jungle | `cobblemontcg:base2` | `scyther` 2000, `wigglytuff` 2001, `flareon` 2002 |

Add one offer per wrapper to sell them all. For a datapack set, `custom_model_data` is the set's `model_data_base` plus the wrapper's position in its `wrappers` list (starting at 0).
