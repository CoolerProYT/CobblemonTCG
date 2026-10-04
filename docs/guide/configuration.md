# Configuration

Config files are in the `config` folder and use [CoolerConfig](https://github.com/CoolerProYT/CoolerConfig), bundled with the mod.

## Common: `cobblemontcg-common.toml`

Read by the server (or by your game in single player).

### Packs

| Key | Default | Range | Description |
| --- | --- | --- | --- |
| `packs.holoChance` | `0.333` | 0 to 1 | Chance that the rare slot of a pack is a holo rare. About 1 in 3, like the real Base Set |
| `packs.packSize` | `11` | 1 to 64 | Cards per pack. Extra cards come from, and missing cards are taken from, the last slot of the set (commons) |

### Effects

| Key | Default | Description |
| --- | --- | --- |
| `effects.soundsEnabled` | `true` | Play a sound when a pack is opened |

### Rewards

| Key | Default | Description |
| --- | --- | --- |
| `rewards.enabled` | `true` | Allow reward triggers to give packs. Commands always work |
| `rewards.dailyPackCap` | `10` | Reward packs a player can get per day (UTC), `0` for no limit. Commands are not limited |
| `rewards.triggers.capture` | `true` | Packs for catching Pokémon |
| `rewards.triggers.levelUp` | `true` | Packs for Pokémon level milestones |
| `rewards.triggers.dexProgress` | `true` | Packs for Pokédex milestones |

The rules themselves (which events, what chance, which set) are in [reward rule files](/datapacks/rewards).

### Shop

| Key | Default | Range | Description |
| --- | --- | --- | --- |
| `shop.sets` | `["cobblemontcg:base1", "cobblemontcg:base2"]` | | Sets villagers sell, oldest first. The Card Dealer unlocks one per villager level, Novice to Master (up to 5 sets) |
| `shop.cardDealer.enabled` | `true` | | Card Dealer villagers sell booster packs |
| `shop.cardDealer.price` | `5` | 1 to 64 | Emeralds per pack at the Card Dealer |
| `shop.cardDealer.maxUses` | `3` | 1 to 64 | Packs a Card Dealer sells before restocking |
| `shop.wanderingTrader.enabled` | `true` | | Wandering traders can offer a booster pack |
| `shop.wanderingTrader.price` | `8` | 1 to 64 | Emeralds per pack at the wandering trader |
| `shop.wanderingTrader.maxUses` | `1` | 1 to 64 | Packs a wandering trader sells (they never restock) |

Shop settings apply to villagers that get new offers after the change; offers that already exist are kept.

## Client: `cobblemontcg-client.toml`

| Key | Default | Description |
| --- | --- | --- |
| `packOpening.animation` | `true` | Show the opening animation. When off, the cards go straight to your inventory |
