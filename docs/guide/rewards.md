# Pokémon rewards

Playing Cobblemon earns you packs. The mod listens to Cobblemon's catch, level-up and Pokédex events and hands out packs by a set of rules. These are the rules the mod ships with; a [datapack can change or replace them](/datapacks/rewards).

## Catching Pokémon

<RewardTable file="capture" />

Pokémon that appear in Jungle but not in Base Set (Scyther, Snorlax, Eevee and its evolutions, and the rest of the list) give **Jungle** packs; every other species gives **Base Set** packs.

## Levelling up

<RewardTable file="level_up" />

Every Pokémon pays for each of these levels as it reaches them, so training a new Pokémon earns packs again. A Pokémon caught above a level does not pay for it.

## Filling the Pokédex

<RewardTable file="dex_progress" />

The percentage counts the species you own out of every species in Cobblemon's Pokédex.

## Milestones pay once

Pokédex milestones and first catches are paid **once per player**. A milestone is used up when its rule rolls its chance, win or lose, so a first catch that missed its 25% does not try again. Claimed milestones are saved on the player.

Level rewards are paid once per Pokémon, and the any-catch and shiny rules pay out every time.

Every reward pack is announced in chat.

## Daily limit

A player can get at most **10 reward packs per day** (UTC). Packs from commands, villagers and traders do not count. When the limit stops a Pokédex or first-catch milestone, the milestone stays open and pays on a later event once the limit resets. Level rewards are not held over: a Pokémon that reaches a level while you are at the limit does not pay for it later.

## Turning rewards off

| Setting | Default | |
| --- | --- | --- |
| `rewards.enabled` | `true` | All reward packs |
| `rewards.dailyPackCap` | `10` | Reward packs per player per day, `0` for no limit |
| `rewards.triggers.capture` | `true` | Packs for catching Pokémon |
| `rewards.triggers.levelUp` | `true` | Packs for level milestones |
| `rewards.triggers.dexProgress` | `true` | Packs for Pokédex milestones |
