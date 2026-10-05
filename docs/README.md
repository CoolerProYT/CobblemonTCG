# Cobblemon: TCG wiki

VitePress site for the mod. Sets, cards, pack odds, reward rules, recipes and textures are read from the mod itself, so the wiki always matches the mod in this branch.

```bash
cd docs
npm install
npm run dev     # syncs data, then serves http://localhost:5173/CobblemonTCG/
npm run build   # syncs data, then builds to .vitepress/dist
```

`npm run sync` (run automatically by `dev` and `build`) writes `.vitepress/data/data.json` from `common/src/main/resources` and `tools/<set>_text.json`, and copies the mod's card and pack textures to `public/tcg/` and its logo to `public/items/`. All three are git-ignored.

## Item icons

Recipe slots show item icons hosted at `https://storage.googleapis.com/coolerpromc/textures/<namespace>/<item>.png`
(1024×1024): vanilla items under `minecraft/`, the mod's under `cobblemontcg/`. A new or redrawn mod item needs its
icon uploaded there: the item texture from `textures/item/` scaled up with nearest-neighbour, or for a block its
inventory render (the Card Dealer Table's is `renders/items/card_dealer_table.png`, drawn by `tools/gen_table_art.py`).

```bash
gcloud storage cp renders/items/card_dealer_table.png gs://coolerpromc/textures/cobblemontcg/card_dealer_table.png
```

## Cobblemon renders

In game the cards show Cobblemon's own models, drawn at runtime. The wiki shows the same renders, exported from the game into `renders/` (committed) and copied over the drawn art by `npm run sync`. Re-export them when a set gets new Pokémon cards or Cobblemon adds a species that had none:

```bash
# from the repository root: runs the NeoForge dev client, joins the world "wiki-renders", saves every render and quits
./gradlew :neoforge:runClient -PexportArt=docs/renders
```

The first time, create a world named `wiki-renders` in the dev client (any settings, a superflat world loads fastest); Quick Play only opens existing worlds. Headless (CI, a server), run it under `xvfb-run`. Species Cobblemon has not implemented get no render and keep the drawn art.
