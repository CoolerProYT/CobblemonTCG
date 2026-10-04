# Datapacks

Everything about a set lives in JSON, so sets, cards and reward rules can be added or changed with a datapack. Run `/reload` to apply changes.

| What | Where | Page |
| --- | --- | --- |
| A set: name, size, wrappers, pack slots | `data/<namespace>/tcg/sets/<set>.json` | [Set files](./sets) |
| A card: name, type, HP, rarity, Pokédex number | `data/<namespace>/tcg/cards/<set>/<number>.json` | [Card files](./cards) |
| When packs are handed out | `data/<namespace>/tcg/rewards/*.json` | [Reward rules](./rewards) |

The set id comes from the file path: `data/foo/tcg/sets/bar.json` is the set `foo:bar`, and its cards go in `data/foo/tcg/cards/bar/`.

## Adding a new set

A set needs a datapack and a resource pack:

1. **Datapack**: a [set file](./sets) and one [card file](./cards) per card.
2. **Resource pack**: the [textures](./textures) of every card and wrapper, plus their item models and `custom_model_data` overrides. Without those the cards show the card back.
3. **Shop**: add the set id to [`shop.sets`](/guide/configuration#shop) to have Card Dealers sell it at their next level.
4. **Rewards**: add [reward rules](./rewards) if catching Pokémon should give its packs.

The mod's own sets are built this way. In the repository, `tools/gen_cards.py` writes the card files, the models and the overrides from a card list (`tools/<set>.csv`), and `tools/gen_card_art.py` draws the textures:

| File | Content |
| --- | --- |
| `tools/<set>.csv` | The card list: `number,name,supertype,type,hp,rarity` |
| `tools/<set>_text.json` | The game text drawn on the cards: stage, evolves from, level, Pokémon Powers, attacks, weakness, resistance, retreat, trainer and energy rules |

```bash
pip install pillow numpy          # Python 3.10+, Pillow 10.1+
python tools/gen_cards.py         # card JSONs, models and overrides for every CSV
python tools/gen_card_art.py      # frames, holo foil, card art, packs, card back (about 3 minutes)
python tools/gen_card_art.py --skip-existing-art --set base2 --only 4,58
```

`--skip-existing-art` keeps card art you have already replaced, and `--set` and `--only` redraw one set or some card numbers.

## Changing the odds of a set

Override the set file at the same path, `data/cobblemontcg/tcg/sets/base1.json`, with your own `pack_slots`. For only the holo rate or the pack size, the [config](/guide/configuration#packs) is enough.
