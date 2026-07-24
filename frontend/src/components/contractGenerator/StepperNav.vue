<script setup lang="ts">
defineProps<{ pasos: readonly string[]; pasoActual: number }>()
</script>

<template>
  <ol class="stepper-nav">
    <li v-for="(nombre, index) in pasos" :key="nombre" class="paso" :class="{ activo: pasoActual === index + 1, completo: pasoActual > index + 1 }">
      <span class="circulo">
        <span v-if="pasoActual > index + 1">✓</span>
        <span v-else>{{ index + 1 }}</span>
      </span>
      <span class="nombre">{{ nombre }}</span>
      <span v-if="index < pasos.length - 1" class="linea" :class="{ completa: pasoActual > index + 1 }" />
    </li>
  </ol>
</template>

<style scoped>
.stepper-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  list-style: none;
  margin: 0 0 2.5rem;
  padding: 0;
}

.paso {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  color: var(--text-muted);
  min-width: 0;
}

.circulo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  min-width: 1.75rem;
  border-radius: 50%;
  border: 1px solid var(--border);
  font-size: 0.8125rem;
  font-weight: 600;
  transition:
    background var(--duration-base) var(--ease-out),
    border-color var(--duration-base) var(--ease-out),
    color var(--duration-base) var(--ease-out),
    transform var(--duration-base) var(--ease-out);
}

.paso.activo .circulo,
.paso.completo .circulo {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--accent-contrast);
}

.paso.activo .circulo {
  transform: scale(1.1);
}

.paso.activo .nombre {
  color: var(--text-h);
  font-weight: 600;
}

.nombre {
  font-size: 0.875rem;
  white-space: nowrap;
}

.linea {
  width: clamp(1.5rem, 6vw, 4rem);
  height: 1px;
  background: var(--border);
  transition: background var(--duration-base) var(--ease-out);
}

.linea.completa {
  background: var(--accent);
}

/* En mobile no entran los 4 nombres + circulos + lineas en una sola fila
   (el nombre "Descarga" del ultimo paso quedaba directamente cortado fuera
   de la pantalla). Se muestra el nombre solo del paso activo, y el resto
   queda como circulo numerado — sigue siendo claro en que paso estas. */
@media (max-width: 480px) {
  .paso:not(.activo) .nombre {
    display: none;
  }

  .linea {
    width: clamp(0.75rem, 4vw, 2rem);
  }
}
</style>
