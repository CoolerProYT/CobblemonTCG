# Booster packs

A booster pack holds **11 cards**, like a real 1999 pack:

| Slot | Cards | What you get |
| --- | --- | --- |
| Rare | 1 | A holo rare about 1 pack in 3 (the [`packs.holoChance`](./configuration) setting), otherwise a non-holo rare |
| Uncommon | 3 | Uncommons |
| Common | 7 | Commons, basic Energy included |

No card appears twice in the same pack. A pack stacks up to 16.

## Wrappers

Like the real sets, every pack comes in one of three wrappers, picked at random. The wrapper is only the look: every wrapper of a set has the same odds.

**Base Set**

<PackWrappers set="base1" :width="120" />

**Jungle**

<PackWrappers set="base2" :width="120" back />

In game, the Pokémon on the wrapper is Cobblemon's own model of it, drawn into the pack like on the cards. The art above is the fallback the mod shows until Cobblemon's models are ready.

## Opening a pack

Right-click a pack in either hand.

1. **The pack.** Click (or press Space) to tear it open.
2. **The cards.** They are dealt face down and flip over one at a time. Swipe the top card away to see the next: drag it to the side, click it, or press Space, Enter, D or the right arrow. Commons come first and the rare last. A counter at the bottom shows how many are left.
3. **The rare.** A holo rare gets a burst of light and its own sound; nearby players hear it too, and see sparkles above you.
4. **The summary.** Every pull of the pack on one screen. Click or press Esc to close.

The cards go into your inventory as soon as the pack opens, before the animation starts. If your inventory is full, the rest drop at your feet. Closing the screen early, or disconnecting, never loses a card.

::: tip Skip the animation
Set `packOpening.animation = false` in `config/cobblemontcg-client.toml` and the cards go straight to your inventory. It only changes your own client.
:::

## Odds

The exact odds of every set are on its page: [Base Set](/sets/base1#pack-odds), [Jungle](/sets/base2#pack-odds). With the default settings:

<PackOdds set="base1" />
