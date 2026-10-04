<script setup lang="ts">
import { computed } from 'vue'
import { findSet } from '../tcg'
import BoosterPack from './BoosterPack.vue'

const props = withDefaults(defineProps<{ set: string; back?: boolean; width?: number }>(), { back: false, width: 140 })
const cardSet = computed(() => findSet(props.set)!)
</script>

<template>
  <div class="wrappers">
    <BoosterPack v-for="wrapper in cardSet.wrappers" :key="wrapper" :set="cardSet.id" :wrapper="wrapper" :width="width" caption />
    <BoosterPack v-if="back" :width="width" back caption />
  </div>
</template>

<style scoped>
.wrappers {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 16px 0;
}
</style>
