<script setup lang="ts">
import { computed, ref } from 'vue'
import { findSet, frameTexture, tcgTexture } from '../tcg'

// Stacks the card's layers like the in-game model: frame, holo foil, illustration, card text and
// evolution portrait. In game the illustration and portrait show Cobblemon's own models instead.
const props = withDefaults(
  defineProps<{ set: string; number?: number; holo?: boolean | null; width?: number | string; back?: boolean; tilt?: boolean }>(),
  { number: 0, holo: null, width: 180, back: false, tilt: true },
)

const cardSet = computed(() => findSet(props.set))
const card = computed(() => cardSet.value?.cards.find((c) => c.number === props.number))
const isHolo = computed(() => (props.holo === null ? card.value?.rarity === 'rare_holo' : props.holo))
const cssWidth = computed(() => (typeof props.width === 'number' ? `${props.width}px` : props.width))
const label = computed(() => (card.value ? `${card.value.name} (${card.value.number}/${cardSet.value?.total})${isHolo.value ? ', holo' : ''}` : 'Card back'))

// A gentle tilt and glare under the pointer, like holding the card up to the light.
const el = ref<HTMLElement | null>(null)
const rx = ref(0)
const ry = ref(0)
const gx = ref(50)
const gy = ref(50)
const active = ref(false)

function move(event: PointerEvent) {
  if (!props.tilt || !el.value || event.pointerType === 'touch') return
  const rect = el.value.getBoundingClientRect()
  const x = (event.clientX - rect.left) / rect.width
  const y = (event.clientY - rect.top) / rect.height
  ry.value = (x - 0.5) * 18
  rx.value = (0.5 - y) * 18
  gx.value = x * 100
  gy.value = y * 100
  active.value = true
}

function leave() {
  rx.value = 0
  ry.value = 0
  active.value = false
}
</script>

<template>
  <div
    ref="el"
    class="tcg-card"
    :class="{ holo: isHolo, active }"
    :style="{ width: cssWidth, '--rx': `${rx}deg`, '--ry': `${ry}deg`, '--gx': `${gx}%`, '--gy': `${gy}%` }"
    role="img"
    :aria-label="label"
    @pointermove="move"
    @pointerleave="leave"
  >
    <div class="inner">
      <img v-if="back || !card" class="layer" :src="tcgTexture('card_back.png')" alt="" loading="lazy" />
      <template v-else>
        <img class="layer" :src="frameTexture(card)" alt="" loading="lazy" />
        <span v-if="isHolo" class="foil" :style="{ backgroundImage: `url(${tcgTexture('holo_overlay.png')})` }" />
        <img v-if="card.illustration" class="art" :src="tcgTexture(`${cardSet!.path}/illustration/${card.number}.png`)" alt="" loading="lazy" />
        <img class="layer" :src="tcgTexture(`${cardSet!.path}/${card.number}.png`)" alt="" loading="lazy" />
        <img v-if="card.evolution" class="portrait" :src="tcgTexture(`${cardSet!.path}/evolution/${card.number}.png`)" alt="" loading="lazy" />
      </template>
      <span class="glare" />
    </div>
  </div>
</template>

<style scoped>
.tcg-card {
  display: inline-block;
  max-width: 100%;
  perspective: 800px;
  vertical-align: top;
}

.inner {
  position: relative;
  aspect-ratio: 256 / 352;
  border-radius: 5% / 3.6%;
  overflow: hidden;
  transform: rotateX(var(--rx)) rotateY(var(--ry));
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.active .inner {
  transition: transform 0.05s linear;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
}

.inner img,
.inner span {
  position: absolute;
  display: block;
  user-select: none;
  -webkit-user-drag: none;
}

.layer {
  inset: 0;
  width: 100%;
  height: 100%;
}

/* Art window: x 24 to 231, y 40 to 183 of 256x352. */
.art,
.foil {
  left: 9.375%;
  top: 11.364%;
  width: 81.25%;
  height: 40.909%;
}

/* The holo foil is an 8-frame strip of 208x144, cycled like the in-game animation. */
.foil {
  background-size: 100% 800%;
  animation: foil 1.2s steps(8) infinite;
}

@keyframes foil {
  from {
    background-position: 0 0;
  }
  to {
    background-position: 0 114.2857%;
  }
}

/* Previous stage portrait: x 14, y 13, 32x32 texture with the picture in its top 32x24. */
.portrait {
  left: 5.469%;
  top: 3.693%;
  width: 12.5%;
  height: 9.091%;
}

.glare {
  inset: 0;
  opacity: 0;
  transition: opacity 0.25s ease;
  background: radial-gradient(circle at var(--gx) var(--gy), rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0) 55%);
  pointer-events: none;
}

.active .glare {
  opacity: 1;
}

.holo.active .glare {
  background:
    radial-gradient(circle at var(--gx) var(--gy), rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0) 50%),
    linear-gradient(115deg, rgba(255, 0, 128, 0.12), rgba(0, 255, 200, 0.12) 50%, rgba(120, 80, 255, 0.12));
  mix-blend-mode: screen;
}

@media (prefers-reduced-motion: reduce) {
  .foil {
    animation: none;
  }
  .inner {
    transform: none !important;
  }
}
</style>
