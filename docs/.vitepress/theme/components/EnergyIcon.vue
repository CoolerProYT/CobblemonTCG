<script setup lang="ts">
import { computed } from 'vue'
import { capitalize, TYPE_COLORS } from '../tcg'

const props = defineProps<{ type: string }>()
const color = computed(() => TYPE_COLORS[props.type] ?? TYPE_COLORS.colorless)
// Fire and Fighting share a first letter.
const letter = computed(() => (props.type === 'fighting' ? 'Fg' : props.type.charAt(0).toUpperCase()))
</script>

<template>
  <span class="energy" :style="{ background: color }" :title="capitalize(type)" :aria-label="`${capitalize(type)} Energy`" role="img">
    {{ letter }}
  </span>
</template>

<style scoped>
.energy {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  margin-right: 2px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.35);
  font: 700 9px/1 var(--vp-font-family-base);
  color: #fff;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.6);
  vertical-align: middle;
}
</style>
