# Cobblemon: TCG wiki

VitePress site for the mod. Sets, cards, pack odds, reward rules, recipes and textures are read from the mod itself, so the wiki always matches the mod in this branch.

```bash
cd docs
npm install
npm run dev     # syncs data, then serves http://localhost:5173/CobblemonTCG/
npm run build   # syncs data, then builds to .vitepress/dist
```

`npm run sync` (run automatically by `dev` and `build`) writes `.vitepress/data/data.json` from `common/src/main/resources` and `tools/<set>_text.json`, and copies the mod's card and pack textures to `public/tcg/` and its item icons to `public/items/`. All three are git-ignored. Vanilla item icons load from the hosted renders at `https://storage.googleapis.com/coolerpromc/textures/`, set in `.vitepress/theme/tcg.ts`.

A new set shows up in the data on its own; give it a page in `sets/` (copy `sets/base2.md`) and a sidebar entry in `.vitepress/config.mts`.

The `Docs` workflow (`.github/workflows/docs.yml`) builds the site and deploys it to GitHub Pages on every push to the repository's default branch. One-time setup: repository Settings > Pages > Source: "GitHub Actions".
