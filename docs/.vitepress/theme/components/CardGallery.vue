<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { capitalize, type Card, cardChance, DEFAULT_HOLO_CHANCE, findSet, oneIn, RARITIES, RARITY_NAMES, RARITY_SYMBOLS, SUPERTYPE_NAMES, TYPES } from '../tcg'
import CardDetails from './CardDetails.vue'
import EnergyIcon from './EnergyIcon.vue'
import TcgCard from './TcgCard.vue'

const props = defineProps<{ set: string }>()
const cardSet = computed(() => findSet(props.set)!)

const query = ref('')
const rarity = ref('')
const kind = ref('')

const kinds = computed(() => {
  const present = new Set(cardSet.value.cards.map((card) => (card.supertype === 'pokemon' ? card.type : card.supertype)))
  return [...TYPES, 'trainer', 'energy'].filter((k) => present.has(k))
})

const cards = computed(() => {
  const q = query.value.trim().toLowerCase()
  return cardSet.value.cards.filter((card) => {
    if (rarity.value && card.rarity !== rarity.value) return false
    if (kind.value) {
      const cardKind = card.supertype === 'pokemon' ? card.type : card.supertype
      if (cardKind !== kind.value) return false
    }
    if (!q) return true
    return (
      card.name.toLowerCase().includes(q) ||
      String(card.number) === q ||
      card.attacks.some((attack) => attack.name.toLowerCase().includes(q)) ||
      card.powers.some((power) => power.name.toLowerCase().includes(q))
    )
  })
})

function kindName(k: string) {
  return k === 'trainer' || k === 'energy' ? SUPERTYPE_NAMES[k] : `${capitalize(k)} Pokémon`
}

function reset() {
  query.value = ''
  rarity.value = ''
  kind.value = ''
}

// The open card, kept in the URL hash (#card-4) so a card can be linked to.
const selected = ref<Card | null>(null)
const holo = ref(false)
const dialog = ref<HTMLDialogElement | null>(null)

function open(card: Card) {
  selected.value = card
  holo.value = card.rarity === 'rare_holo'
  history.replaceState(history.state, '', `#card-${card.number}`)
}

function close() {
  dialog.value?.close()
}

function onClose() {
  selected.value = null
  if (location.hash.startsWith('#card-')) history.replaceState(history.state, '', location.pathname + location.search)
}

function step(delta: number) {
  if (!selected.value) return
  const list = cards.value
  const index = list.findIndex((card) => card.number === selected.value!.number)
  const next = list[(index + delta + list.length) % list.length]
  if (next) open(next)
}

function onKey(event: KeyboardEvent) {
  if (!selected.value) return
  if (event.key === 'ArrowRight') step(1)
  if (event.key === 'ArrowLeft') step(-1)
}

watch(selected, async (card, previous) => {
  if (card && !previous) {
    await nextTick()
    dialog.value?.showModal()
  }
})

onMounted(() => {
  window.addEventListener('keydown', onKey)
  const match = location.hash.match(/^#card-(\d+)$/)
  const card = match && cardSet.value.cards.find((c) => c.number === Number(match[1]))
  if (card) open(card)
})

onBeforeUnmount(() => window.removeEventListener('keydown', onKey))

const pullChance = computed(() => (selected.value ? cardChance(cardSet.value, selected.value.rarity, DEFAULT_HOLO_CHANCE) : 0))
</script>

<template>
  <div class="gallery">
    <div class="filters">
      <input v-model="query" type="search" placeholder="Search name, number or attack" aria-label="Search cards" />
      <select v-model="rarity" aria-label="Rarity">
        <option value="">All rarities</option>
        <option v-for="r in RARITIES" :key="r" :value="r">{{ RARITY_SYMBOLS[r] }} {{ RARITY_NAMES[r] }}</option>
      </select>
      <select v-model="kind" aria-label="Card type">
        <option value="">All types</option>
        <option v-for="k in kinds" :key="k" :value="k">{{ kindName(k) }}</option>
      </select>
      <span class="count">{{ cards.length }} / {{ cardSet.cards.length }} cards</span>
    </div>

    <div v-if="cards.length" class="grid">
      <button v-for="card in cards" :key="card.number" class="cell" type="button" @click="open(card)">
        <TcgCard :set="cardSet.id" :number="card.number" width="100%" :tilt="false" />
        <span class="caption">
          <span class="num">{{ card.number }}</span>
          <span class="name">{{ card.name }}</span>
          <EnergyIcon v-if="card.type && card.supertype === 'pokemon'" :type="card.type" />
          <span class="rarity" :class="card.rarity" :title="RARITY_NAMES[card.rarity]">{{ RARITY_SYMBOLS[card.rarity] }}</span>
        </span>
      </button>
    </div>
    <p v-else class="empty">No cards match. <button type="button" class="link" @click="reset">Clear filters</button></p>

    <dialog ref="dialog" class="viewer" :aria-label="selected?.name" @close="onClose" @click.self="close">
      <div v-if="selected" class="viewer-body">
        <div class="viewer-card">
          <TcgCard :key="`${selected.number}-${holo}`" :set="cardSet.id" :number="selected.number" :holo="holo" width="100%" />
          <label class="toggle"><input v-model="holo" type="checkbox" /> Holo print</label>
        </div>
        <div class="viewer-info">
          <h3>{{ selected.name }}</h3>
          <CardDetails :set="cardSet" :card="selected" />
          <p class="chance">
            In a {{ cardSet.name }} pack: {{ oneIn(pullChance) }}
            <span class="hint">(default holo chance)</span>
          </p>
        </div>
        <div class="viewer-nav">
          <button type="button" aria-label="Previous card" @click="step(-1)">‹</button>
          <button type="button" aria-label="Close" @click="close">✕</button>
          <button type="button" aria-label="Next card" @click="step(1)">›</button>
        </div>
      </div>
    </dialog>
  </div>
</template>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin: 16px 0;
}

.filters input,
.filters select {
  padding: 6px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 14px;
}

.filters input {
  flex: 1 1 220px;
}

.count {
  font-size: 13px;
  color: var(--vp-c-text-2);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));
  gap: 18px 14px;
}

.cell {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 0;
  border: 0;
  background: none;
  text-align: left;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.cell:hover,
.cell:focus-visible {
  transform: translateY(-3px);
}

.caption {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  line-height: 1.3;
}

.num {
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
}

.name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.rarity {
  color: var(--vp-c-text-2);
}

.rarity.rare_holo {
  background: linear-gradient(120deg, #f59e0b, #ec4899, #8b5cf6);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.empty {
  color: var(--vp-c-text-2);
}

.link {
  color: var(--vp-c-brand-1);
  text-decoration: underline;
}

.viewer {
  width: min(860px, calc(100vw - 32px));
  max-height: calc(100vh - 32px);
  padding: 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
}

.viewer::backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}

.viewer-body {
  display: grid;
  grid-template-columns: minmax(200px, 300px) 1fr;
  gap: 24px;
  padding: 24px;
}

.viewer-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  cursor: pointer;
}

.viewer-info h3 {
  margin: 0 0 6px;
  font-size: 24px;
  font-weight: 700;
}

.chance {
  margin-top: 12px;
  font-size: 14px;
}

.hint {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.viewer-nav {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.viewer-nav button {
  width: 40px;
  height: 36px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  font-size: 18px;
}

.viewer-nav button:hover {
  border-color: var(--vp-c-brand-1);
}

@media (max-width: 640px) {
  .viewer-body {
    grid-template-columns: 1fr;
    padding: 16px;
  }

  .viewer-card {
    width: min(240px, 100%);
    margin: 0 auto;
  }

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}
</style>
