<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { itemIcon, itemName } from '../tcg'
import BoosterPack from './BoosterPack.vue'

const props = withDefaults(defineProps<{ id?: string | null; count?: number; label?: boolean }>(), {
  id: null,
  count: 1,
  label: false,
})

const name = computed(() => (props.id ? itemName(props.id) : ''))
const isPack = computed(() => props.id === 'cobblemontcg:booster_pack')
const src = computed(() => (props.id && !isPack.value ? itemIcon(props.id) : null))

// Falls back to initials when an item has no icon or the hosted icon fails to load.
const failed = ref(false)
watch(src, () => (failed.value = false))
const initials = computed(() =>
  name.value
    .split(' ')
    .filter((word) => /^[A-Z]/.test(word))
    .slice(0, 2)
    .map((word) => word[0])
    .join(''),
)
</script>

<template>
  <span class="tcg-item" :class="{ 'with-label': label }">
    <span class="tcg-slot" :title="name" :aria-label="name" role="img">
      <BoosterPack v-if="isPack" set="base1" wrapper="charizard" :width="21" />
      <img v-else-if="src && !failed" class="pixelated" :src="src" alt="" loading="lazy" @error="failed = true" />
      <span v-else-if="id" class="initials">{{ initials }}</span>
      <span v-if="count > 1" class="count">{{ count }}</span>
    </span>
    <span v-if="label && id" class="label">{{ name }}</span>
  </span>
</template>

<style scoped>
.tcg-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  vertical-align: middle;
}

.tcg-slot {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex: none;
  background: var(--tcg-slot-bg);
  border: 2px solid;
  border-color: var(--tcg-slot-dark) var(--tcg-slot-light) var(--tcg-slot-light) var(--tcg-slot-dark);
}

.tcg-slot img {
  width: 32px;
  height: 32px;
}

.tcg-slot :deep(.inner:hover) {
  transform: none;
}

.initials {
  font: 600 12px/1 var(--vp-font-family-mono);
  color: #fff;
  text-shadow: 1px 1px 0 #3f3f3f;
}

.count {
  position: absolute;
  right: 1px;
  bottom: -1px;
  font: 700 12px/1 var(--vp-font-family-mono);
  color: #fff;
  text-shadow: 1px 1px 0 #3f3f3f;
}

.label {
  font-weight: 500;
}
</style>
