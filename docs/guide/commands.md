# Commands

All commands need operator permission (level 2) and give the item to the player running them.

| Command | Gives |
| --- | --- |
| `/tcg give pack <set> [amount]` | `amount` booster packs of `set` (1 to 6400, default 1), each with a random wrapper |
| `/tcg give card <set> <number> [holo]` | One card. `holo` is `true` or `false` (default `false`) |

`<set>` is the set id, like `cobblemontcg:base1`, or just `base1`. Tab completion lists the loaded sets.

| Set | Id |
| --- | --- |
| Base Set | `base1` |
| Jungle | `base2` |

Examples:

```
/tcg give pack base2 5
/tcg give card base1 4 true
```

The second gives a holo Charizard. Every card page in [Sets](/sets/) shows its give command.

Packs from commands are not limited by `rewards.dailyPackCap`, and are given even when rewards are turned off.
