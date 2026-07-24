<script setup lang="ts">
import type { ContractData, FieldSpec } from '../../services/contractGenerator/contract.service'
import BaseAlert from '../ui/BaseAlert.vue'

defineProps<{ campos: FieldSpec[]; data: ContractData; errores: string[] }>()
</script>

<template>
  <div class="formulario-datos">
    <label v-for="campo in campos" :key="campo.name">
      <span>{{ campo.label }}</span>
      <textarea
        v-if="campo.type === 'textarea'"
        v-model="data[campo.name]"
        :placeholder="campo.placeholder"
        rows="3"
      />
      <input v-else v-model="data[campo.name]" :type="campo.type" :placeholder="campo.placeholder" />
    </label>

    <BaseAlert :mensajes="errores" />
  </div>
</template>

<style scoped>
.formulario-datos {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}

input,
textarea {
  padding: 0.75rem 0.875rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text-h);
  font: inherit;
  font-size: 0.95rem;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-base) var(--ease-out),
    color var(--duration-base) var(--ease-out);
}

input:focus,
textarea:focus {
  outline: none;
  border-color: var(--accent);
}

textarea {
  resize: vertical;
  font-family: var(--sans);
}
</style>
