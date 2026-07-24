<script setup lang="ts">
import { useContractWizard } from '../../composables/contractGenerator/useContractWizard'
import { useLocale } from '../../i18n/useLocale'
import BaseAlert from '../ui/BaseAlert.vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseCard from '../ui/BaseCard.vue'
import FormularioDatos from './FormularioDatos.vue'
import PreviewDocumento from './PreviewDocumento.vue'
import SelectorEstilo from './SelectorEstilo.vue'
import StepperNav from './StepperNav.vue'
import TemplateSelector from './TemplateSelector.vue'

const { t } = useLocale()

const {
  pasos,
  paso,
  templates,
  styles,
  templateId,
  styleId,
  data,
  errores,
  preview,
  generando,
  errorGeneracion,
  templateSeleccionado,
  siguiente,
  anterior,
  generar,
} = useContractWizard()
</script>

<template>
  <div class="contract-generator-main">
    <StepperNav :pasos="pasos" :paso-actual="paso" />

    <Transition name="paso-transicion" mode="out-in">
      <div :key="paso">
        <template v-if="paso === 1">
          <h2>{{ t.step1Heading }}</h2>
          <TemplateSelector :templates="templates" v-model="templateId" />
        </template>

        <div v-else class="dos-columnas">
          <BaseCard>
            <template v-if="paso === 2 && templateSeleccionado">
              <h2>{{ t.step2Heading }}</h2>
              <p class="etiqueta-plantilla">{{ templateSeleccionado.nombre.toUpperCase() }}</p>
              <FormularioDatos :campos="templateSeleccionado.campos" :data="data" :errores="errores" />
            </template>

            <template v-else-if="paso === 3">
              <h2>{{ t.step3Heading }}</h2>
              <SelectorEstilo :styles="styles" v-model="styleId" />
            </template>

            <template v-else-if="paso === 4">
              <h2>{{ t.step4Heading }}</h2>
              <PreviewDocumento :content="preview" :style-id="styleId" />
            </template>
          </BaseCard>

          <BaseCard v-if="paso !== 4">
            <h2>{{ t.previewHeading }}</h2>
            <PreviewDocumento :content="preview" :style-id="styleId" />
          </BaseCard>

          <BaseCard v-else class="resumen">
            <div class="dato-resumen">
              <span class="etiqueta">{{ t.summaryTemplateLabel }}</span>
              <strong>{{ templateSeleccionado?.nombre }}</strong>
            </div>
            <div class="dato-resumen">
              <span class="etiqueta">{{ t.summaryStyleLabel }}</span>
              <strong>{{ styles.find((s) => s.id === styleId)?.nombre }}</strong>
            </div>
            <BaseButton :disabled="generando" @click="generar">
              {{ generando ? t.generatingButton : t.generateButton }}
            </BaseButton>
            <BaseAlert :mensajes="errorGeneracion ? [errorGeneracion] : []" />
          </BaseCard>
        </div>
      </div>
    </Transition>

    <!-- Los errores del paso 2 ya se muestran dentro de FormularioDatos, junto
         a cada campo; aca solo se repiten para los pasos 1 y 3, que no tienen
         un formulario con alert propio. -->
    <BaseAlert v-if="paso !== 2" class="errores-paso" :mensajes="errores" />

    <div class="navegacion">
      <BaseButton v-if="paso > 1" variant="secondary" @click="anterior">{{ t.backButton }}</BaseButton>
      <span v-else />
      <BaseButton v-if="paso < 4" @click="siguiente">{{ t.continueButton }}</BaseButton>
    </div>
  </div>
</template>

<style scoped>
.contract-generator-main {
  max-width: 900px;
  margin: 0 auto;
}

.contract-generator-main h2 {
  font-size: 1.125rem;
  margin-bottom: 1.25rem;
}

.etiqueta-plantilla {
  margin: -0.75rem 0 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.dos-columnas {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 720px) {
  .dos-columnas {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .dos-columnas {
    gap: 1rem;
  }

  .navegacion {
    margin-top: 1.5rem;
  }

  .navegacion > * {
    flex: 1;
  }
}

.resumen {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
}

.dato-resumen {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.dato-resumen .etiqueta {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.errores-paso {
  margin-top: 1rem;
}

.navegacion {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.paso-transicion-enter-active,
.paso-transicion-leave-active {
  transition:
    opacity var(--duration-base) var(--ease-out),
    transform var(--duration-base) var(--ease-out);
}

.paso-transicion-enter-from {
  opacity: 0;
  transform: translateX(12px);
}

.paso-transicion-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--duration-fast) var(--ease-out);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
