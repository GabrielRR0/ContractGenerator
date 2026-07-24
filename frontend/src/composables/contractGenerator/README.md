# composables/contractGenerator

Estado y logica reactiva del wizard de generacion (4 pasos: Tipo → Datos → Estilo → Descarga), separada de los componentes visuales para poder testearla sin montar Vue components.

## Archivos

- **`useContractWizard.ts`**: unico composable del dominio, orquesta todo el flujo:
  - `paso` (1-4), `pasos` (computed: nombres de paso ya traducidos via `useLocale`, para el `StepperNav`).
  - `templates` / `styles`: catalogos cargados de la API al montar (`cargarCatalogos`), pasando el `locale` activo (`useLocale().locale`). Un `watch(locale, cargarCatalogos)` los vuelve a pedir si el usuario cambia de idioma a mitad del formulario — los datos ya cargados (`data`) no se pierden, solo cambian las etiquetas.
  - `templateId` / `styleId`: seleccion del usuario en los pasos 1 y 3.
  - `data`: objeto reactivo generico (`Record<string, string>`) con los valores del formulario — su forma depende de `templateSeleccionado.campos`, no esta hardcodeado a un tipo de contrato.
  - `preview`: contenido (`titulo`/`parrafos`/`firmas`/`paginas`) que se re-pide a `POST /api/contracts/preview` cada vez que cambian `templateId`, `data`, `locale` o `styleId` (con un debounce de 400ms para no pegarle al backend en cada tecla — el preview tambien renderiza el PDF real para contar paginas, asi que hay que ser mas conservador que un simple GET).
  - `errores`: mensajes de validacion del paso actual, tambien traducidos (`t.value.errorChooseTemplate`, etc).
  - `siguiente()` / `anterior()`: `siguiente()` valida el paso actual (`validarPasoActual`) antes de avanzar; si falla, llena `errores` y no avanza.
  - `generar()`: llama a `POST /api/contracts/generate` (con el `locale` activo) y dispara la descarga del blob resultante.
  - **`useContractWizard.spec.ts`**: como el composable usa `onMounted` (para cargar templates/styles), el test lo monta dentro de un componente Vue minimo creado con `createApp` — llamarlo "pelado" fuera de un `setup()` hace que `onMounted` nunca se registre. Tambien cubre que cambiar `locale` (desde `useLocale`) dispara un nuevo `fetch` de templates/styles con el query param correcto.

## Por que la validacion vive en `utils/validators/` y no aca

La logica pura de validacion (`validateRequiredFields`, `validateFieldLengths`) esta en `utils/validators/validateContractFields.ts` para poder reutilizarla o testearla sin depender de la reactividad de Vue. Es generica: recibe los `campos` (`FieldSpec[]`) de la plantilla activa, no una lista de campos fija.
