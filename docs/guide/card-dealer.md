# Card Dealer & traders

## The Card Dealer

The Card Dealer is a villager profession. Its job site block is the **Card Dealer Table**:

<RecipeCard id="card_dealer_table" />

Place the table near an unemployed villager (not a nitwit) and it becomes a Card Dealer, the same way a lectern makes a librarian. The table can be mined with an axe.

### What it sells

A Card Dealer sells **one booster pack for 5 emeralds**, 3 times before it has to restock at its table. The wrapper of each offer is random.

It unlocks newer sets as it levels up, like the real sets came out one after the other:

| Villager level | Unlocks | Price |
| --- | --- | --- |
| Novice | Base Set packs | 5 emeralds |
| Apprentice (about 5 pack purchases) | Jungle packs | 5 emeralds |

The sets and their order come from the [`shop.sets`](./configuration) setting, oldest first, one set per villager level from Novice to Master (up to 5 sets). Add a datapack set to that list to have Card Dealers sell it at the next level.

## Wandering traders

A wandering trader may offer **one booster pack of a random `shop.sets` set for 8 emeralds**. The pack offer joins the trader's common pool, so not every trader has it, and like all wandering trader offers it never restocks.

## Changing prices and stock

| Setting | Default |
| --- | --- |
| `shop.cardDealer.enabled` | `true` |
| `shop.cardDealer.price` | `5` emeralds |
| `shop.cardDealer.maxUses` | `3` packs per restock |
| `shop.wanderingTrader.enabled` | `true` |
| `shop.wanderingTrader.price` | `8` emeralds |
| `shop.wanderingTrader.maxUses` | `1` pack |

These are read when a villager gets new offers, so a change applies to villagers that level up or traders that spawn after it. Offers that already exist keep their price and stock. Prices still go up and down with the villager's reputation and demand, like any vanilla trade.

## Selling packs with CobbleDollars

Running [CobbleDollars](https://modrinth.com/mod/cobbledollars)? Its merchants can sell packs too. See [CobbleDollars](./cobbledollars).
