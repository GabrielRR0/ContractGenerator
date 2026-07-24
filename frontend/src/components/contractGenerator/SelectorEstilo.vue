<script setup lang="ts">
import type { StyleInfo } from '../../services/contractGenerator/contract.service'

defineProps<{ styles: StyleInfo[]; modelValue: string | null }>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="selector-estilo">
    <button
      v-for="style in styles"
      :key="style.id"
      type="button"
      class="opcion-estilo"
      :class="{ activo: modelValue === style.id }"
      @click="$emit('update:modelValue', style.id)"
    >
      <strong>{{ style.nombre }}</strong>
      <span>{{ style.descripcion }}</span>
    </button>
  </div>
</template>

<style scoped>
.selector-estilo {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.opcion-estilo {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  cursor: pointer;
  text-align: left;
  font: inherit;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out),
    background-color var(--duration-base) var(--ease-out),
    color var(--duration-base) var(--ease-out);
}

.opcion-estilo strong {
  color: var(--text-h);
  font-weight: 600;
  transition: color var(--duration-base) var(--ease-out);
}

.opcion-estilo span {
  font-size: 0.8125rem;
  color: var(--text-muted);
  transition: color var(--duration-base) var(--ease-out);
}

.opcion-estilo:hover {
  transform: translateY(-1px);
}

.opcion-estilo.activo {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 18%, transparent);
}
</style>
