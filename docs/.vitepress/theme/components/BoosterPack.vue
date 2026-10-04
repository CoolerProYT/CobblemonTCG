<script setup lang="ts">
import { computed } from 'vue'
import { capitalize, findSet, tcgTexture } from '../tcg'

// A pack front is three layers, like the in-game model: foil, mascot (from y 96) and overlay.
// The mascot is the Cobblemon render of the wrapper's Pokémon exported from the game (docs/renders/).
const props = withDefaults(defineProps<{ set?: string | null; wrapper?: string | null; width?: number | string; back?: boolean; caption?: boolean }>(), {
  set: null,
  wrapper: null,
  width: 140,
  back: false,
  caption: false,
})

const cardSet = computed(() => (props.set ? findSet(props.set) : undefined))
const name = computed(() => (cardSet.value && props.wrapper ? `${cardSet.value.path}_${props.wrapper}` : 'default'))
const cssWidth = computed(() => (typeof props.width === 'number' ? `${props.width}px` : props.width))
const label = computed(() => (cardSet.value ? `${cardSet.value.name} booster pack${props.wrapper ? `, ${capitalize(props.wrapper)} wrapper` : ''}` : 'Booster pack'))
</script>

<template>
  <figure class="tcg-pack" :style="{ width: cssWidth }">
    <div class="inner" role="img" :aria-label="label">
      <img v-if="back" class="layer" :src="tcgTexture('pack/back.png')" alt="" loading="lazy" />
      <template v-else>
        <img class="layer" :src="tcgTexture(`pack/${name}.png`)" alt="" loading="lazy" />
        <img class="mascot" :src="tcgTexture(`pack/${name}_mascot.png`)" alt="" loading="lazy" />
        <img class="layer" :src="tcgTexture(`pack/${name}_overlay.png`)" alt="" loading="lazy" />
      </template>
    </div>
    <figcaption v-if="caption">{{ back ? 'Back' : wrapper ? capitalize(wrapper) : cardSet?.name }}</figcaption>
  </figure>
</template>

<style scoped>
.tcg-pack {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  max-width: 100%;
  margin: 0;
  vertical-align: top;
}

.inner {
  position: relative;
  width: 100%;
  aspect-ratio: 240 / 368;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.25));
  transition: transform 0.2s ease;
}

.inner:hover {
  transform: translateY(-4px) rotate(-1.5deg);
}

.inner img {
  position: absolute;
  display: block;
  user-select: none;
}

.layer {
  inset: 0;
  width: 100%;
  height: 100%;
}

.mascot {
  left: 0;
  top: 26.087%;
  width: 100%;
  height: 56.522%;
}

figcaption {
  font-size: 13px;
  color: var(--vp-c-text-2);
}
</style>
