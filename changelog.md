## 1.1.0

### Four new sets
- **Fossil** (`cobblemontcg:base3`, 62 cards): Aerodactyl, Lapras and Gengar wrappers.
- **Base Set 2** (`cobblemontcg:base4`, 130 cards): Mewtwo, Gyarados and Ninetales wrappers.
- **Team Rocket** (`cobblemontcg:base5`, 83 cards, with the secret Dark Raichu): Dark Charizard, Dark Blastoise and Dark Dragonite wrappers.
- **Wizards Black Star Promos** (`cobblemontcg:basep`, 53 cards): Pikachu, Mew and Ho-Oh wrappers. The real promos were never sold in packs, so each card has a regular rarity to fit the usual 11 card pack.
- Every card has a regular and a holo print and shows Cobblemon's model of the Pokémon. Entei, Celebi and Suicune use drawn art until Cobblemon adds their models.
- Each set has its own card style: Fossil in sepia sandstone with a fossil spiral mark, Base Set 2 in orange gold with a 2, Team Rocket at night in dark maroon with a red R, and the promos in slate and silver with starlight and a black star.

### Card Display Stand
- A new block for selling cards to other players. Put a card on it, set a price of any item in any amount, and other players buy copies from a shop screen. Payments wait in the stand's till until you collect them.
- Only its owner can break it. Crouch and right-click with an empty hand to take your cards back.
- JEI: drag any item from JEI onto the price slot to ask for it.
- Jade: shows the card, its stock, price and seller when you look at a stand.

### Card Dealer
- Unlocks a set per villager level in release order: Base Set (Novice), Jungle (Apprentice), Fossil (Journeyman), Base Set 2 (Expert), and both Team Rocket and the Black Star Promos at Master. `shop.sets` now takes up to 6 sets.

### Rewards
- Catching a Pokémon first printed in Fossil (Aerodactyl, Lapras, Gengar, Dragonite...) gives a Fossil pack, and one that only appears in the promos (Mew and the Johto Pokémon) a Black Star Promos pack, instead of a Base Set pack. Base Set 2 and Team Rocket have no new species.

### Other changes
- Every set has its own creative tab with its packs and cards. The main tab keeps the Card Binder, the Card Dealer Table, the Card Display Stand and datapack sets.
- New Metal type (Scizor).
- Trainer cards show their kind (Stadium, Rocket's Secret Machine) above their rules.

### Note for existing configs
`shop.sets` in `config/cobblemontcg-common.toml` is not changed for you. Set it to `["cobblemontcg:base1", "cobblemontcg:base2", "cobblemontcg:base3", "cobblemontcg:base4", "cobblemontcg:base5", "cobblemontcg:basep"]` to have Card Dealers sell the new packs.
