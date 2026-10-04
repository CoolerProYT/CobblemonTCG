<script setup lang="ts">
import { computed } from 'vue'
import { data, percent, setName } from '../tcg'

// The reward rules the mod ships, in plain words.
const props = defineProps<{ file: string }>()
const rules = computed(() => data.rewards.find((r) => r.file === props.file || r.file === `${props.file}.json`)?.rules ?? [])

function species(list: unknown): string {
  const names = (list as string[]).map((s) => s.charAt(0).toUpperCase() + s.slice(1))
  return names.length > 6 ? `${names.slice(0, 6).join(', ')} and ${names.length - 6} more` : names.join(', ')
}

function when(conditions: Record<string, unknown>): string[] {
  const parts: string[] = []
  if (conditions.first_catch_of_species) parts.push('First catch of a species')
  if (conditions.shiny) parts.push('Shiny')
  if (conditions.min_level !== undefined) parts.push(`Level ${conditions.min_level}+`)
  if (conditions.level !== undefined) parts.push(`A Pokémon reaches level ${conditions.level}`)
  if (conditions.dex_every !== undefined) parts.push(`Every ${conditions.dex_every} species owned`)
  if (conditions.dex_percent !== undefined) parts.push(`${conditions.dex_percent}% of the Pokédex owned`)
  if (conditions.species) parts.push(`Only ${species(conditions.species)}`)
  if (conditions.exclude_species) parts.push(`Not ${species(conditions.exclude_species)}`)
  return parts
}
</script>

<template>
  <table>
    <thead>
      <tr>
        <th>When</th>
        <th>Chance</th>
        <th>Reward</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(rule, i) in rules" :key="i">
        <td>
          <template v-for="(part, j) in when(rule.conditions)" :key="j">
            <span :class="{ 'tcg-muted': part.startsWith('Only') || part.startsWith('Not') }">{{ part }}</span><br />
          </template>
        </td>
        <td>{{ rule.chance >= 1 ? 'Always' : percent(rule.chance) }}</td>
        <td>{{ rule.amount }} {{ setName(rule.set) }} pack{{ rule.amount === 1 ? '' : 's' }}</td>
      </tr>
    </tbody>
  </table>
</template>
