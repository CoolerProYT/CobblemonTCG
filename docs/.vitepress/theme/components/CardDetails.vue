<script setup lang="ts">
import { computed } from 'vue'
import { capitalize, type Card, type CardSet, RARITY_NAMES, RARITY_SYMBOLS, SUPERTYPE_NAMES } from '../tcg'
import EnergyIcon from './EnergyIcon.vue'

const props = defineProps<{ set: CardSet; card: Card }>()

const stage = computed(() => props.card.subtypes.join(' · '))
const command = computed(() => `/tcg give card ${props.set.path} ${props.card.number}`)
</script>

<template>
  <div class="details">
    <p class="meta">
      <span>{{ card.number }}/{{ set.total }}</span>
      <span>{{ RARITY_SYMBOLS[card.rarity] }} {{ RARITY_NAMES[card.rarity] }}</span>
      <span>{{ SUPERTYPE_NAMES[card.supertype] }}<template v-if="stage"> · {{ stage }}</template></span>
    </p>

    <dl class="stats">
      <template v-if="card.type">
        <dt>Type</dt>
        <dd><EnergyIcon :type="card.type" /> {{ capitalize(card.type) }}</dd>
      </template>
      <template v-if="card.hp">
        <dt>HP</dt>
        <dd>{{ card.hp }}</dd>
      </template>
      <template v-if="card.evolvesFrom">
        <dt>Evolves from</dt>
        <dd>{{ card.evolvesFrom }}</dd>
      </template>
      <template v-if="card.level">
        <dt>Level</dt>
        <dd>{{ card.level }}</dd>
      </template>
      <template v-if="card.pokedex">
        <dt>Pokédex</dt>
        <dd>#{{ card.pokedex }}</dd>
      </template>
    </dl>

    <div v-for="power in card.powers" :key="power.name" class="move">
      <p class="move-head"><span class="power">Pokémon Power</span> <strong>{{ power.name }}</strong></p>
      <p class="move-text">{{ power.text }}</p>
    </div>

    <div v-for="attack in card.attacks" :key="attack.name" class="move">
      <p class="move-head">
        <span class="cost">
          <EnergyIcon v-for="(type, i) in attack.cost" :key="i" :type="type" />
          <span v-if="attack.cost.length === 0" class="free">—</span>
        </span>
        <strong>{{ attack.name }}</strong>
        <span v-if="attack.damage" class="damage">{{ attack.damage }}</span>
      </p>
      <p v-if="attack.text" class="move-text">{{ attack.text }}</p>
    </div>

    <p v-for="(rule, i) in card.rules" :key="i" class="move-text rule">{{ rule }}</p>

    <dl v-if="card.supertype === 'pokemon'" class="wrr">
      <dt>Weakness</dt>
      <dd>
        <template v-for="w in card.weakness" :key="w.type"><EnergyIcon :type="w.type" /> {{ w.value }} </template>
        <template v-if="!card.weakness.length">—</template>
      </dd>
      <dt>Resistance</dt>
      <dd>
        <template v-for="r in card.resistance" :key="r.type"><EnergyIcon :type="r.type" /> {{ r.value }} </template>
        <template v-if="!card.resistance.length">—</template>
      </dd>
      <dt>Retreat</dt>
      <dd>
        <EnergyIcon v-for="i in card.retreat ?? 0" :key="i" type="colorless" />
        <template v-if="!card.retreat">—</template>
      </dd>
    </dl>

    <p class="give">
      <code>{{ command }}</code>
      <span class="hint">add <code>true</code> for the holo print</span>
    </p>
  </div>
</template>

<style scoped>
.details p {
  margin: 0;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 14px;
  font-size: 13px;
  color: var(--vp-c-text-2);
}

dl {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 4px 14px;
  margin: 12px 0;
  font-size: 14px;
}

dt {
  color: var(--vp-c-text-2);
}

dd {
  margin: 0;
}

.move {
  padding: 8px 0;
  border-top: 1px solid var(--vp-c-divider);
}

.move-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.damage {
  margin-left: auto;
  font-weight: 700;
  font-size: 16px;
}

.power {
  padding: 1px 6px;
  border-radius: 4px;
  background: #c0392b;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.free {
  color: var(--vp-c-text-3);
}

.move-text {
  margin-top: 4px !important;
  font-size: 13.5px;
  line-height: 1.5;
  color: var(--vp-c-text-2);
}

.rule {
  padding: 8px 0;
  border-top: 1px solid var(--vp-c-divider);
}

.wrr {
  padding-top: 10px;
  border-top: 1px solid var(--vp-c-divider);
}

.give {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 10px;
  margin-top: 12px !important;
}

.hint {
  font-size: 12px;
  color: var(--vp-c-text-3);
}
</style>
