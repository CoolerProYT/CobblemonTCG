# Textures & art

Every texture can be replaced by a resource pack with a drawing of the same size and name, no code changes needed. All textures are original fan illustrations drawn for the mod.

## Card layers

A card model stacks these layers on its front, back to front:

| Layer | Texture | Size | Shared |
| --- | --- | --- | --- |
| Frame | `tcg/frame/<pokemon_<type>\|trainer\|energy>.png` | 256×352 | per type: border, face, art window background, labels |
| Holo foil (holo prints only) | `tcg/holo_overlay.png` (+ `.mcmeta`) | 208×144 per frame | all cards, animated, covers the art window only |
| Illustration (Pokémon only) | `tcg/<set>/illustration/<number>.png` | 208×144 | one per card: the Pokémon in the art window |
| Card text | `tcg/<set>/<number>.png` | 256×352 | one per card: name, HP, attacks, number, rarity; trainer and energy art |
| Evolution portrait (evolution cards only) | `tcg/<set>/evolution/<number>.png` | 32×32, picture in the top 32×24 | one per card: the previous stage |

All paths are under `assets/cobblemontcg/textures/`. The texture is the whole card (63 × 88 mm); the art window is x 24 to 231, y 40 to 183.

On a holo print the foil shows through wherever the card art is transparent, so leave the art window background transparent to keep the holo effect, or paint over it for a full-art card.

<div class="tcg-row">
  <TcgCard set="base2" :number="10" :width="180" />
  <TcgCard set="base2" :number="26" :width="180" />
</div>

The cards on this wiki are stacked from the same layers.

## Cobblemon models

The client draws Cobblemon's own models into the illustration and evolution portrait of every card that has a `pokedex` / `evolves_from_pokedex` number, and into the mascot of every wrapper listed in the set's `wrapper_pokedex`, posed like in Cobblemon's Pokédex. This happens a few cards per tick after joining a world and again after a resource reload. Until then, and for species Cobblemon has not implemented, the drawn art is shown.

## Other textures

| Texture | Size |
| --- | --- |
| `tcg/card_back.png` (back of every card, and cards without data) | 256×352 |
| `tcg/pack/<set>_<wrapper>.png` (pack front: foil and light burst) | 240×368 |
| `tcg/pack/<set>_<wrapper>_mascot.png` (pack mascot, drawn from y 96 of the pack) | 240×208 |
| `tcg/pack/<set>_<wrapper>_overlay.png` (set name plate, badges, seals and foil sheen, over the mascot) | 240×368 |
| `tcg/pack/back.png` (back of every pack) | 240×368 |
| `tcg/pack/default.png`, `default_mascot.png`, `default_overlay.png` (pack without set data) | as above |

<div class="tcg-row">
  <BoosterPack :width="120" caption />
  <BoosterPack back :width="120" caption />
</div>

## Models

The model templates live in `assets/cobblemontcg/models/item/tcg/` (`card.json`, `card_holo.json`, `card_face_down.json`, `pack.json` and the Pokémon and evolution variants). `tools/gen_cards.py` writes one model per card print and per wrapper, and the `custom_model_data` overrides in `models/item/tcg_card.json` and `models/item/booster_pack.json`.
