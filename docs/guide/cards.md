# Cards

<div class="tcg-row">
  <TcgCard set="base1" :number="4" :width="220" />
  <TcgCard set="base1" :number="4" :holo="false" :width="220" />
  <TcgCard set="base1" :number="96" :width="220" />
</div>

Cards follow the layout of a 1999 Base Set card: yellow border, a face coloured by the Pokémon's type, the stage line, name and HP, a framed art window, Pokémon Powers and attacks with their Energy cost and damage, weakness, resistance and retreat cost, then the level, number and rarity symbol. Every card is drawn from scratch for the mod, no official scans or card art.

## Tooltips

Hover over a card to see its number in the set, rarity, card type, HP, Energy type and whether it is a holo.

## Rarity

| Symbol | Rarity |
| --- | --- |
| ● | Common |
| ◆ | Uncommon |
| ★ | Rare |
| ★ (holo) | Rare Holo |

## Holo prints

Every card exists as a regular and a holo print. Packs give the holo print of **Rare Holo** cards only; the holo prints of other cards can only be given with [`/tcg give card <set> <number> true`](./commands).

A holo print has an animated foil that shimmers behind the art. Holo and regular prints of the same card do not stack together.

## Cobblemon on the cards

Each Pokémon card shows **Cobblemon's own model** of that Pokémon in the art window, posed like in Cobblemon's Pokédex, and evolution cards show the previous stage in the small portrait at the top left. Pack wrappers get the same treatment for their mascot.

The models are drawn a few cards per tick after you join a world, and again after a resource reload. Until then, and for species Cobblemon has not added yet, the card shows its drawn art. The cards on this wiki use the same renders, exported from the game. Nothing from Cobblemon is copied into the mod.

## In the world

Cards and packs are thin 3D items with a real back. A held, dropped or framed card shows the card back, and a pack shows the back of its wrapper.

<div class="tcg-row">
  <TcgCard set="base1" back :width="140" />
  <BoosterPack back :width="128" />
</div>
