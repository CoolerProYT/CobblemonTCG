<script setup lang="ts">
import { withBase } from 'vitepress'
import { data, RARITIES, RARITY_NAMES } from '../tcg'
import BoosterPack from './BoosterPack.vue'

const sets = data.sets.map((set) => ({
  ...set,
  counts: RARITIES.map((rarity) => [rarity, set.cards.filter((card) => card.rarity === rarity).length] as const).filter(([, n]) => n > 0),
}))
</script>

<template>
  <div class="sets">
    <a v-for="set in sets" :key="set.id" class="set" :href="withBase(`/sets/${set.path}`)">
      <BoosterPack :set="set.id" :wrapper="set.wrappers[0]" :width="96" />
      <span class="info">
        <strong>{{ set.name }}</strong>
        <code>{{ set.id }}</code>
        <span>{{ set.cards.length }} cards</span>
        <span class="counts">
          <span v-for="[rarity, n] in set.counts" :key="rarity">{{ n }} {{ RARITY_NAMES[rarity].toLowerCase() }}</span>
        </span>
      </span>
    </a>
  </div>
</template>

<style scoped>
.sets {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin: 16px 0;
}

.set {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  color: inherit;
  text-decoration: none !important;
  transition: border-color 0.2s ease;
}

.set:hover {
  border-color: var(--vp-c-brand-1);
}

.info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

.info strong {
  font-size: 18px;
}

.counts {
  display: flex;
  flex-direction: column;
  color: var(--vp-c-text-2);
  font-size: 13px;
}
</style>
