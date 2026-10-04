# Cobblemon: TCG wiki

VitePress site for the mod. Sets, cards, pack odds, reward rules, recipes and textures are read from the mod itself, so the wiki always matches the mod in this branch.

```bash
cd docs
npm install
npm run dev     # syncs data, then serves http://localhost:5173/CobblemonTCG/
npm run build   # syncs data, then builds to .vitepress/dist
```

`npm run sync` (run automatically by `dev` and `build`) writes `.vitepress/data/data.json` from `common/src/main/resources` and `tools/<set>_text.json`, and copies the mod's card and pack textures to `public/tcg/` and its item icons to `public/items/`. All three are git-ignored.

## Cobblemon renders

In game the cards show Cobblemon's own models, drawn at runtime. The wiki shows the same renders, exported from the game into `renders/` (committed) and copied over the drawn art by `npm run sync`. Re-export them when a set gets new Pokémon cards or Cobblemon adds a species that had none:

```bash
# from the repository root: runs the NeoForge dev client, joins the world "wiki-renders", saves every render and quits
./gradlew :neoforge:runClient -PexportArt=docs/renders
```

The first time, create a world named `wiki-renders` in the dev client (any settings, a superflat world loads fastest); Quick Play only opens existing worlds. Headless (CI, a server), run it under `xvfb-run`. Species Cobblemon has not implemented get no render and keep the drawn art.
