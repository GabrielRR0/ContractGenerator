<script setup lang="ts">
import type { TemplateInfo } from '../../services/contractGenerator/contract.service'

defineProps<{ templates: TemplateInfo[]; modelValue: string | null }>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="template-selector">
    <button
      v-for="template in templates"
      :key="template.id"
      type="button"
      class="opcion-template"
      :class="{ activo: modelValue === template.id }"
      @click="$emit('update:modelValue', template.id)"
    >
      <span class="icono">{{ template.icono }}</span>
      <strong>{{ template.nombre }}</strong>
      <span class="descripcion">{{ template.descripcion }}</span>
    </button>
  </div>
</template>

<style scoped>
.template-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.opcion-template {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.625rem;
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  background: var(--bg-surface);
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

.opcion-template:hover {
  transform: translateY(-2px);
}

.opcion-template.activo {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 18%, transparent);
}

.icono {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--accent-contrast);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  transition: background-color var(--duration-base) var(--ease-out);
}

.opcion-template strong {
  color: var(--text-h);
  font-size: 1rem;
  transition: color var(--duration-base) var(--ease-out);
}

.descripcion {
  font-size: 0.8125rem;
  color: var(--text-muted);
  line-height: 1.5;
  transition: color var(--duration-base) var(--ease-out);
}
</style>
