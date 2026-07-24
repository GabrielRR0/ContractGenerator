<script setup lang="ts">
import { useLocale } from '../../i18n/useLocale'
import type { PreviewContent } from '../../services/contractGenerator/contract.service'

defineProps<{ content: PreviewContent | null; styleId?: string | null }>()

const { t } = useLocale()
</script>

<template>
  <div class="preview-documento-contenedor">
    <p v-if="content?.paginas" class="contador-paginas">
      {{ content.paginas }} {{ content.paginas === 1 ? t.pageCountSingular : t.pageCountPlural }}
    </p>
    <Transition name="preview-fade" mode="out-in">
      <!-- La key es solo el estilo (no el contenido): asi el texto se actualiza
           en el lugar mientras el usuario escribe (sin parpadeo), y solo se
           dispara la transicion cuando cambia el estilo elegido (paso 3). -->
      <div v-if="content" :key="styleId ?? 'sin-estilo'" class="preview-documento" :class="`estilo-${styleId}`">
        <h3>{{ content.titulo }}</h3>
        <p v-for="(parrafo, index) in content.parrafos" :key="index">{{ parrafo }}</p>
      </div>
      <p v-else class="preview-vacio">{{ t.previewEmpty }}</p>
    </Transition>
  </div>
</template>

<style scoped>
.contador-paginas {
  margin: 0 0 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.preview-documento {
  padding: 2rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-family: var(--sans);
  /* El contenido puede ser largo (clausulas reales, no solo el resumen
     minimo) — scrollea adentro de la card en vez de estirar la pagina. */
  max-height: min(32rem, 65vh);
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}

.preview-documento::-webkit-scrollbar {
  width: 6px;
}

.preview-documento::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 999px;
}

.preview-documento h3 {
  font-size: 1.125rem;
  letter-spacing: -0.01em;
  transition: color var(--duration-base) var(--ease-out);
}

.preview-documento p {
  color: var(--text);
  font-size: 0.9375rem;
  line-height: 1.7;
  margin: 0;
  /* Respeta los saltos de linea que el usuario escribio en un textarea (ej.
     la clausula de confidencialidad) — por defecto el navegador los colapsa. */
  white-space: pre-line;
}

.preview-vacio {
  color: var(--text-muted);
  font-size: 0.9375rem;
  padding: 2rem;
}

/* Aproximacion visual de cada estilo del PDF real (ver backend
   pdf/styles/*.py) para que elegir un estilo se sienta con efecto inmediato. */
.preview-documento.estilo-classic {
  font-family: Georgia, 'Times New Roman', Times, serif;
  text-align: center;
}
.preview-documento.estilo-classic h3 {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.75rem;
}
.preview-documento.estilo-classic p {
  text-align: left;
  text-indent: 1.5rem;
}

.preview-documento.estilo-corporate {
  padding: 0;
  overflow-x: hidden;
}
.preview-documento.estilo-corporate h3 {
  margin: 0;
  padding: 1.25rem 2rem;
  background: #1f2937;
  color: #ffffff;
  letter-spacing: 0;
}
.preview-documento.estilo-corporate p {
  padding: 0 2rem;
}
.preview-documento.estilo-corporate p:last-child {
  padding-bottom: 2rem;
}
.preview-documento.estilo-corporate p:first-of-type {
  margin-top: 1.25rem;
}

.preview-documento.estilo-modern h3 {
  color: var(--accent);
  font-size: 1.25rem;
  position: relative;
  padding-bottom: 0.75rem;
}
.preview-documento.estilo-modern h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 2.5rem;
  height: 3px;
  background: var(--accent);
  border-radius: 2px;
}

.preview-fade-enter-active,
.preview-fade-leave-active {
  transition:
    opacity var(--duration-base) var(--ease-out),
    transform var(--duration-base) var(--ease-out);
}

.preview-fade-enter-from {
  opacity: 0;
  transform: translateY(6px) scale(0.99);
}

.preview-fade-leave-to {
  opacity: 0;
}
</style>
