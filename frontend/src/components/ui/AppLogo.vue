<template>
  <div class="app-logo" aria-hidden="true">
    <svg viewBox="0 0 24 24" fill="none">
      <path
        d="M7 3.5h6.5L18 8v11.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1Z"
        fill="currentColor"
        fill-opacity="0.18"
      />
      <path d="M13.5 3.5V8H18" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" />
      <path d="M9 12.5h6M9 15.2h6M9 9.8h2.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
    </svg>
  </div>
</template>

<style scoped>
.app-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--accent-contrast);
  transition: background-color var(--duration-base) var(--ease-out);
}

.app-logo svg {
  width: 1.375rem;
  height: 1.375rem;
}
</style>
