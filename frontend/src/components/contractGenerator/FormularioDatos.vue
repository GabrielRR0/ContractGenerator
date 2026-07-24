<script setup lang="ts">
import { useLocale } from '../../i18n/useLocale'
import type { ContractData, FieldSpec } from '../../services/contractGenerator/contract.service'
import BaseAlert from '../ui/BaseAlert.vue'

defineProps<{ campos: FieldSpec[]; data: ContractData; errores: string[] }>()

const { t } = useLocale()
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
      <!-- Contador solo en textareas: son los campos donde el limite (miles
           de caracteres) es realista de alcanzar; en un campo corto (200
           caracteres, ej. un nombre) nunca se acerca y solo ensuciaria el form. -->
      <span
        v-if="campo.type === 'textarea' && campo.max_length"
        class="contador-caracteres"
        :class="{ 'sobre-limite': (data[campo.name]?.length ?? 0) > campo.max_length }"
      >
        {{ (data[campo.name]?.length ?? 0).toLocaleString() }} / {{ campo.max_length.toLocaleString() }}
        {{ t.characterCountSuffix }}
      </span>
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

.contador-caracteres {
  align-self: flex-end;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.contador-caracteres.sobre-limite {
  color: var(--alert-text);
  font-weight: 600;
}

textarea {
  resize: vertical;
  font-family: var(--sans);
}
</style>
