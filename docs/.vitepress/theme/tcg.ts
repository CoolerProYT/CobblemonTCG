import { withBase } from 'vitepress'
// @ts-ignore
import raw from '../data/data.json'

export type Rarity = 'common' | 'uncommon' | 'rare' | 'rare_holo'
export type Supertype = 'pokemon' | 'trainer' | 'energy'

export interface Attack {
  name: string
  cost: string[]
  damage: string
  text?: string
}

export interface Card {
  number: number
  name: string
  supertype: Supertype
  type: string | null
  hp: number | null
  rarity: Rarity
  pokedex: number | null
  evolvesFromPokedex: number | null
  subtypes: string[]
  level: string | null
  evolvesFrom: string | null
  powers: { name: string; text: string }[]
  attacks: Attack[]
  weakness: { type: string; value: string }[]
  resistance: { type: string; value: string }[]
  retreat: number | null
  rules: string[]
  illustration: boolean
  evolution: boolean
  /** Frame texture under tcg/, from the card's item model */
  frame: string | null
}

export interface PackSlot {
  count: number
  rarities: Partial<Record<Rarity, number>>
  useConfigHoloChance: boolean
}

export interface CardSet {
  id: string
  path: string
  name: string
  total: number
  modelDataBase: number
  wrappers: string[]
  wrapperPokedex: Record<string, number>
  packSlots: PackSlot[]
  cards: Card[]
}

export interface RewardRule {
  trigger: string
  set: string
  amount: number
  chance: number
  conditions: Record<string, unknown>
}

export interface Recipe {
  id: string
  type: string
  result: { id: string; count: number }
  pattern?: string[]
  key?: Record<string, string>
  ingredients?: string[]
}

export const data = raw as unknown as {
  names: Record<string, string>
  sets: CardSet[]
  rewards: { file: string; rules: RewardRule[] }[]
  recipes: Recipe[]
}

/** Default of `packs.holoChance`. */
export const DEFAULT_HOLO_CHANCE = 0.333

export const RARITIES: Rarity[] = ['common', 'uncommon', 'rare', 'rare_holo']

export const RARITY_NAMES: Record<Rarity, string> = {
  common: 'Common',
  uncommon: 'Uncommon',
  rare: 'Rare',
  rare_holo: 'Rare Holo',
}

/** The rarity symbols printed on the cards. */
export const RARITY_SYMBOLS: Record<Rarity, string> = {
  common: '●',
  uncommon: '◆',
  rare: '★',
  rare_holo: '★',
}

export const SUPERTYPE_NAMES: Record<Supertype, string> = {
  pokemon: 'Pokémon',
  trainer: 'Trainer',
  energy: 'Energy',
}

export const TYPES = ['grass', 'fire', 'water', 'lightning', 'psychic', 'fighting', 'colorless']

export const TYPE_COLORS: Record<string, string> = {
  grass: '#60aa46',
  fire: '#e25632',
  water: '#4082d6',
  lightning: '#f6c828',
  psychic: '#965cb0',
  fighting: '#ba6838',
  colorless: '#c8c4b8',
}

export function capitalize(word: string): string {
  return word.charAt(0).toUpperCase() + word.slice(1)
}

export function findSet(id: string): CardSet | undefined {
  return data.sets.find((set) => set.id === id || set.path === id)
}

export function setName(id: string): string {
  return findSet(id)?.name ?? id
}

/** Public URL of a texture copied from the mod's `textures/tcg/` folder. */
export function tcgTexture(path: string): string {
  return withBase(`/tcg/${path}`)
}

export function frameTexture(card: Card): string {
  if (card.frame) return tcgTexture(card.frame)
  if (card.supertype === 'pokemon') return tcgTexture(`frame/pokemon_${card.type ?? 'colorless'}.png`)
  return tcgTexture(`frame/${card.supertype}.png`)
}

export function percent(fraction: number, digits = 1): string {
  const scale = 10 ** digits
  const value = Math.round(fraction * 100 * scale) / scale
  return `${Number.isInteger(value) ? value : value.toFixed(digits)}%`
}

/** "1 in N" for small chances, which reads better than 0.4%. */
export function oneIn(fraction: number): string {
  if (fraction <= 0) return 'never'
  if (fraction >= 1) return 'every pack'
  const n = 1 / fraction
  return `1 in ${n >= 10 ? Math.round(n) : n.toFixed(1).replace(/\.0$/, '')}`
}

/** Weights of one slot, after `use_config_holo_chance` (mirrors PackRoller.applyHoloChance). */
export function slotWeights(slot: PackSlot, holoChance: number): Partial<Record<Rarity, number>> {
  const weights = { ...slot.rarities }
  if (!slot.useConfigHoloChance || weights.rare_holo === undefined) return weights
  const others = Object.entries(weights)
    .filter(([rarity]) => rarity !== 'rare_holo')
    .reduce((sum, [, weight]) => sum + (weight ?? 0), 0)
  if (others <= 0) return weights
  const chance = Math.min(Math.max(holoChance, 0), 1)
  for (const rarity of Object.keys(weights) as Rarity[]) {
    weights[rarity] = rarity === 'rare_holo' ? chance : ((1 - chance) * (weights[rarity] ?? 0)) / others
  }
  return weights
}

/** Chance of each rarity in one roll of the slot. */
export function slotChances(slot: PackSlot, holoChance: number): Partial<Record<Rarity, number>> {
  const weights = slotWeights(slot, holoChance)
  const total = Object.values(weights).reduce((sum, weight) => sum + (weight ?? 0), 0)
  const chances: Partial<Record<Rarity, number>> = {}
  for (const [rarity, weight] of Object.entries(weights) as [Rarity, number][]) {
    chances[rarity] = total > 0 ? weight / total : 0
  }
  return chances
}

/** Expected number of cards of each rarity in one pack. */
export function cardsPerPack(set: CardSet, holoChance: number): Record<Rarity, number> {
  const result: Record<Rarity, number> = { common: 0, uncommon: 0, rare: 0, rare_holo: 0 }
  for (const slot of set.packSlots) {
    const chances = slotChances(slot, holoChance)
    for (const rarity of RARITIES) result[rarity] += slot.count * (chances[rarity] ?? 0)
  }
  return result
}

/**
 * Chance that one pack holds a given card of this rarity. A pack never repeats a card, so a rarity
 * expected k times in a pack of N such cards shows each one with chance k / N.
 */
export function cardChance(set: CardSet, rarity: Rarity, holoChance: number): number {
  const count = set.cards.filter((card) => card.rarity === rarity).length
  if (count === 0) return 0
  return Math.min(cardsPerPack(set, holoChance)[rarity] / count, 1)
}

export function itemName(id: string): string {
  if (data.names[id]) return data.names[id]
  if (id === '#minecraft:planks') return 'Any Planks'
  const path = id.replace(/^#/, '').split(':').pop() ?? id
  return path
    .split('_')
    .map((word) => (['of', 'the'].includes(word) ? word : capitalize(word)))
    .join(' ')
}

/**
 * Hosted item icons, one 1024px PNG per item id at <namespace>/<path>.png: vanilla items (Mojang's textures are
 * not bundled here) and the mod's own (uploaded from textures/item, and the table's render from tools/gen_table_art.py).
 */
const ICONS = 'https://storage.googleapis.com/coolerpromc/textures'
const HOSTED_NAMESPACES = ['minecraft', 'cobblemontcg']

const TAG_ICONS: Record<string, string> = {
  '#minecraft:planks': 'minecraft:oak_planks',
}

export function itemIcon(id: string): string | null {
  const itemId = TAG_ICONS[id] ?? id
  const [namespace, path] = itemId.includes(':') ? itemId.split(':') : ['minecraft', itemId]
  if (!HOSTED_NAMESPACES.includes(namespace)) return null
  return `${ICONS}/${namespace}/${path}.png`
}
