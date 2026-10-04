// Reads the mod's sets, cards, reward rules, recipes and textures into the wiki, so the pages always
// match the mod. Run by `npm run dev` and `npm run build`; the outputs are git-ignored.
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { basename, dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const docs = join(dirname(fileURLToPath(import.meta.url)), '..')
const root = join(docs, '..')
const resources = join(root, 'common/src/main/resources')
const assets = join(resources, 'assets/cobblemontcg')
const data = join(resources, 'data/cobblemontcg')
const tools = join(root, 'tools')

const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'))
const jsonFiles = (dir) => (existsSync(dir) ? readdirSync(dir).filter((f) => f.endsWith('.json')).sort() : [])
const list = (value) => (value === undefined ? [] : Array.isArray(value) ? value : [value])

const lang = readJson(join(assets, 'lang/en_us.json'))
const names = {}
for (const [key, value] of Object.entries(lang)) {
  const match = key.match(/^(item|block)\.cobblemontcg\.([a-z0-9_]+)$/)
  if (match) names[`cobblemontcg:${match[2]}`] = value
}

// Game text (attacks, powers, rules...) lives next to the card list the textures are drawn from.
const gameText = (set) => {
  const file = join(tools, `${set}_text.json`)
  return existsSync(file) ? Object.fromEntries(readJson(file).map((card) => [card.number, card])) : {}
}

const sets = jsonFiles(join(data, 'tcg/sets')).map((file) => {
  const id = basename(file, '.json')
  const json = readJson(join(data, 'tcg/sets', file))
  const text = gameText(id)
  const cards = jsonFiles(join(data, 'tcg/cards', id))
    .map((card) => readJson(join(data, 'tcg/cards', id, card)))
    .sort((a, b) => a.number - b.number)
    .map((card) => {
      const extra = text[card.number] ?? {}
      return {
        number: card.number,
        name: card.name,
        supertype: card.supertype,
        type: card.type ?? null,
        hp: card.hp ?? null,
        rarity: card.rarity,
        pokedex: card.pokedex ?? null,
        evolvesFromPokedex: card.evolves_from_pokedex ?? null,
        subtypes: extra.subtypes ?? [],
        level: extra.level ?? null,
        evolvesFrom: extra.evolvesFrom ?? null,
        powers: extra.powers ?? [],
        attacks: extra.attacks ?? [],
        weakness: extra.weakness ?? [],
        resistance: extra.resistance ?? [],
        retreat: extra.retreat ?? null,
        rules: extra.rules ?? [],
        illustration: existsSync(join(assets, 'textures/tcg', id, 'illustration', `${card.number}.png`)),
        evolution: existsSync(join(assets, 'textures/tcg', id, 'evolution', `${card.number}.png`)),
      }
    })
  return {
    id: `cobblemontcg:${id}`,
    path: id,
    name: json.name,
    total: json.total,
    modelDataBase: json.model_data_base,
    wrappers: json.wrappers ?? [],
    wrapperPokedex: json.wrapper_pokedex ?? {},
    packSlots: (json.pack_slots ?? []).map((slot) => ({
      count: slot.count,
      rarities: slot.rarities,
      useConfigHoloChance: slot.use_config_holo_chance ?? false,
    })),
    cards,
  }
})

const rewards = jsonFiles(join(data, 'tcg/rewards')).map((file) => ({
  file,
  rules: list(readJson(join(data, 'tcg/rewards', file))).map((rule) => ({
    trigger: rule.trigger,
    set: rule.set,
    amount: rule.amount ?? 1,
    chance: rule.chance ?? 1,
    conditions: rule.conditions ?? {},
  })),
}))

const ingredient = (value) => {
  if (typeof value === 'string') return value
  if (Array.isArray(value)) return ingredient(value[0])
  if (value?.item) return value.item
  if (value?.tag) return `#${value.tag}`
  return '?'
}

const recipes = jsonFiles(join(data, 'recipe')).map((file) => {
  const json = readJson(join(data, 'recipe', file))
  const recipe = { id: `cobblemontcg:${basename(file, '.json')}`, type: json.type, result: { id: json.result?.id, count: json.result?.count ?? 1 } }
  if (json.pattern) {
    recipe.pattern = json.pattern
    recipe.key = Object.fromEntries(Object.entries(json.key).map(([symbol, value]) => [symbol, ingredient(value)]))
  } else {
    recipe.ingredients = (json.ingredients ?? []).map(ingredient)
  }
  return recipe
})

// Textures are copied from the mod, so the wiki never shows art the mod does not ship.
const publicTcg = join(docs, 'public/tcg')
rmSync(publicTcg, { recursive: true, force: true })
cpSync(join(assets, 'textures/tcg'), publicTcg, { recursive: true, filter: (src) => !src.endsWith('.mcmeta') })
// Renders of Cobblemon's models, exported from the game (see README.md), replace the drawn art like in game.
// Species Cobblemon has not implemented have no render and keep the drawn art.
const renders = join(docs, 'renders/cobblemontcg/tcg')
if (existsSync(renders)) cpSync(renders, publicTcg, { recursive: true })

const publicItems = join(docs, 'public/items')
rmSync(publicItems, { recursive: true, force: true })
mkdirSync(publicItems, { recursive: true })
const textures = {}
const copyIcon = (id, source) => {
  if (!existsSync(source)) return
  cpSync(source, join(publicItems, `${id}.png`))
  textures[`cobblemontcg:${id}`] = `/items/${id}.png`
}
for (const file of readdirSync(join(assets, 'textures/item')).filter((f) => f.endsWith('.png'))) {
  copyIcon(basename(file, '.png'), join(assets, 'textures/item', file))
}
// Block items have no flat texture; the table's front stands in for it.
copyIcon('card_dealer_table', join(assets, 'textures/block/card_dealer_table_front.png'))
copyIcon('card_dealer', join(assets, 'textures/entity/villager/profession/card_dealer.png'))
cpSync(join(assets, 'textures/gui/card_binder.png'), join(publicItems, 'card_binder_gui.png'))
// The mod's icon doubles as the wiki's logo and favicon.
cpSync(join(resources, 'cobblemontcg.png'), join(publicItems, 'icon.png'))

mkdirSync(join(docs, '.vitepress/data'), { recursive: true })
writeFileSync(join(docs, '.vitepress/data/data.json'), JSON.stringify({ names, textures, sets, rewards, recipes }, null, 2))
console.log(
  `Synced ${sets.length} sets (${sets.reduce((n, s) => n + s.cards.length, 0)} cards), ${rewards.length} reward files, ${recipes.length} recipes, ${Object.keys(textures).length} icons.`,
)
