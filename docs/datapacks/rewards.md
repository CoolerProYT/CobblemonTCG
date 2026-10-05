# Reward rules

`data/<namespace>/tcg/rewards/*.json`. A file holds one rule or a list of rules. When the rule's trigger fires and its conditions pass, the player gets `amount` packs of `set` with probability `chance`.

```json
{
  "trigger": "cobblemontcg:capture",
  "set": "cobblemontcg:base1",
  "amount": 1,
  "chance": 0.05,
  "conditions": { "min_level": 20, "species": ["pikachu"], "shiny": true }
}
```

| Field | Required | Description |
| --- | --- | --- |
| `trigger` | yes | What fires the rule, see below |
| `set` | yes | Set id of the packs |
| `amount` | no | Packs given, default `1` |
| `chance` | no | 0 to 1, default `1` |
| `conditions` | no | All must pass |

Rules only fire when `rewards.enabled` and the trigger's toggle are on, and are limited by `rewards.dailyPackCap` ([config](/guide/configuration#rewards)). Packs get a random wrapper.

## Triggers

| Trigger | When | Conditions |
| --- | --- | --- |
| `cobblemontcg:capture` | the player catches a Pokémon | `species`, `exclude_species`, `shiny`, `min_level`, `first_catch_of_species` |
| `cobblemontcg:level_up` | one of the player's Pokémon levels up | `level`, `per_pokemon`, `species`, `exclude_species`, `shiny` |
| `cobblemontcg:dex_progress` | the player owns a new species in the Pokédex | `dex_every`, `dex_percent` |

## Conditions

| Condition | Passes when |
| --- | --- |
| `species: ["pikachu"]` | the Pokémon is any of these species |
| `exclude_species: [...]` | the Pokémon is none of these, so two rules can split the species between them |
| `shiny: true` | the Pokémon is shiny (`false`: not shiny) |
| `min_level: 20` | the caught Pokémon is level 20 or higher |
| `first_catch_of_species: true` | the player has never owned this species before |
| `level: 25` | a Pokémon of the player reached level 25 or higher; on a level up it must have just crossed 25 |
| `per_pokemon: true` | with `level`: the level pays for every Pokémon that reaches it, not once per player |
| `dex_every: 10` | the player now owns a multiple of 10 species |
| `dex_percent: 50` | the player owns at least 50% of the species in Cobblemon's Pokédex |

### Milestones

`level` (without `per_pokemon`), `dex_every`, `dex_percent` and `first_catch_of_species: true` are milestones: each pays out at most once per player, and claimed milestones are saved on the player. A milestone is claimed when its rule rolls its chance, win or lose. When no pack can be given because of the daily cap it stays open for the next event. Other rules, like shiny catches, pay out every time. A `per_pokemon` level is not stored: a Pokémon crosses each level only once.

## Default rules

The mod ships three files in `data/cobblemontcg/tcg/rewards/`. Override a file with the same path in a datapack to change it, or replace it with `[]` to remove its rules. What they do is listed on [Pokémon rewards](/guide/rewards).

| File | Rules |
| --- | --- |
| `capture.json` | Any catch: 5% chance of 1 pack. First catch of a species: 25% chance of 1 pack. Shiny catch: 1 pack. Jungle-only Pokémon give Jungle packs, every other species Base Set packs |
| `level_up.json` | For every Pokémon: level 10, 50% chance of 1 Base Set pack; level 25, 1 Base Set pack; level 50, 1 Jungle pack; level 100, 2 Jungle packs |
| `dex_progress.json` | Every 10 species owned: 1 Base Set pack. 25%: 1 Base Set pack. 50%: 1 Jungle pack. 75% and 100%: 2 Jungle packs |

## For mod developers

Other mods can add their own triggers through `RewardTriggerRegistry`; rules then use the new trigger id like the built-in ones.
