<script setup lang="ts">
import { computed, ref } from 'vue'
import { cardChance, cardsPerPack, DEFAULT_HOLO_CHANCE, findSet, oneIn, percent, RARITIES, RARITY_NAMES, RARITY_SYMBOLS, type Rarity, slotChances } from '../tcg'

const props = defineProps<{ set: string }>()
const cardSet = computed(() => findSet(props.set)!)

// Mirrors `packs.holoChance`, so readers can see what a changed config does.
const holoChance = ref(DEFAULT_HOLO_CHANCE)
const hasConfigHolo = computed(() => cardSet.value.packSlots.some((slot) => slot.useConfigHoloChance))

const slots = computed(() =>
  cardSet.value.packSlots.map((slot) => ({
    count: slot.count,
    config: slot.useConfigHoloChance,
    chances: Object.entries(slotChances(slot, holoChance.value)).filter(([, chance]) => chance > 0) as [Rarity, number][],
  })),
)

const rows = computed(() => {
  const perPack = cardsPerPack(cardSet.value, holoChance.value)
  return RARITIES.map((rarity) => ({
    rarity,
    cards: cardSet.value.cards.filter((card) => card.rarity === rarity).length,
    perPack: perPack[rarity],
    each: cardChance(cardSet.value, rarity, holoChance.value),
  })).filter((row) => row.cards > 0)
})

const size = computed(() => cardSet.value.packSlots.reduce((sum, slot) => sum + slot.count, 0))

function amount(value: number) {
  return Number.isInteger(value) ? `${value}` : value.toFixed(2).replace(/0+$/, '')
}
</script>

<template>
  <div class="odds">
    <h4>Slots ({{ size }} cards)</h4>
    <table>
      <thead>
        <tr>
          <th>Cards</th>
          <th>Each card is</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(slot, i) in slots" :key="i">
          <td>{{ slot.count }}</td>
          <td>
            <span v-for="[rarity, chance] in slot.chances" :key="rarity" class="chip">
              {{ RARITY_SYMBOLS[rarity] }} {{ RARITY_NAMES[rarity] }} <strong>{{ percent(chance) }}</strong>
            </span>
            <span v-if="slot.config" class="note">holo chance from config</span>
          </td>
        </tr>
      </tbody>
    </table>

    <label v-if="hasConfigHolo" class="slider">
      <span><code>packs.holoChance</code>: <strong>{{ percent(holoChance) }}</strong></span>
      <input v-model.number="holoChance" type="range" min="0" max="1" step="0.001" />
      <button v-if="holoChance !== DEFAULT_HOLO_CHANCE" type="button" @click="holoChance = DEFAULT_HOLO_CHANCE">Reset</button>
    </label>

    <h4>Per pack</h4>
    <table>
      <thead>
        <tr>
          <th>Rarity</th>
          <th>Cards in set</th>
          <th>Per pack</th>
          <th>A given card</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.rarity">
          <td>{{ RARITY_SYMBOLS[row.rarity] }} {{ RARITY_NAMES[row.rarity] }}</td>
          <td>{{ row.cards }}</td>
          <td>{{ amount(row.perPack) }}</td>
          <td>{{ percent(row.each) }} <span class="note">({{ oneIn(row.each) }})</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.odds h4 {
  margin: 20px 0 0;
}

.chip {
  display: inline-block;
  margin: 2px 8px 2px 0;
  white-space: nowrap;
}

.note {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.slider {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 14px;
  margin: 12px 0;
  padding: 10px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  font-size: 14px;
}

.slider input {
  flex: 1 1 160px;
  accent-color: var(--vp-c-brand-1);
}

.slider button {
  padding: 2px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  font-size: 13px;
}
</style>
