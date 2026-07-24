<script setup lang="ts">
import ContractGeneratorMain from './components/contractGenerator/ContractGeneratorMain.vue'
import AppFooter from './components/ui/AppFooter.vue'
import AppLogo from './components/ui/AppLogo.vue'
import LanguageToggle from './components/ui/LanguageToggle.vue'
import ThemeToggle from './components/ui/ThemeToggle.vue'
import { useLocale } from './i18n/useLocale'

const { t } = useLocale()
</script>

<template>
  <main>
    <div class="controles-flotantes">
      <LanguageToggle />
      <ThemeToggle />
    </div>
    <header class="page-header">
      <AppLogo class="logo" />
      <h1>{{ t.appTitle }}</h1>
      <p class="subtitle">{{ t.appSubtitle }}</p>
    </header>
    <ContractGeneratorMain />
    <AppFooter />
  </main>
</template>

<style scoped>
main {
  position: relative;
  min-height: 100vh;
  padding: 4rem 1.5rem 6rem;
}

.controles-flotantes {
  position: absolute;
  top: 2rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.page-header {
  max-width: 640px;
  margin: 0 auto 3rem;
  text-align: center;
  animation: fade-in-up var(--duration-base) var(--ease-out) both;
}

.logo {
  margin: 0 auto 1.25rem;
}

.page-header h1 {
  font-size: clamp(1.75rem, 6vw, 2.75rem);
}

.subtitle {
  margin-top: 0.75rem;
  color: var(--text-muted);
  font-size: 1.0625rem;
}

@media (max-width: 480px) {
  main {
    padding: 3.5rem 1rem 4rem;
  }

  .controles-flotantes {
    top: 1.25rem;
    right: 1rem;
  }

  .page-header {
    margin-bottom: 2rem;
  }

  .subtitle {
    font-size: 0.9375rem;
  }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
