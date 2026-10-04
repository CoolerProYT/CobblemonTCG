<script setup lang="ts">
import TcgCard from './TcgCard.vue'

// A fanned hand of holo rares for the home page.
const hand = [
  { set: 'base1', number: 2 },
  { set: 'base2', number: 10 },
  { set: 'base1', number: 4 },
  { set: 'base2', number: 11 },
  { set: 'base1', number: 15 },
]
</script>

<template>
  <div class="hand" aria-label="A hand of holo cards" role="img">
    <div v-for="(card, i) in hand" :key="i" class="slot" :style="{ '--i': i - (hand.length - 1) / 2 }">
      <TcgCard :set="card.set" :number="card.number" width="100%" />
    </div>
  </div>
</template>

<style scoped>
.hand {
  position: relative;
  width: 320px;
  height: 320px;
}

.slot {
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 150px;
  margin-left: -75px;
  transform-origin: 50% 140%;
  transform: rotate(calc(var(--i) * 13deg));
  transition: transform 0.25s ease;
  z-index: calc(10 - var(--i) * var(--i));
}

.slot:hover {
  transform: rotate(calc(var(--i) * 13deg)) translateY(-18px);
  z-index: 20;
}

@media (max-width: 640px) {
  .hand {
    width: 260px;
    height: 250px;
  }

  .slot {
    width: 116px;
    margin-left: -58px;
  }
}
</style>
