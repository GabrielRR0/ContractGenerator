# components/contractGenerator

Componentes Vue del dominio "generador de contratos". Implementan un wizard de 4 pasos: elegir tipo de contrato → completar datos → elegir estilo → confirmar y descargar.

## Archivos

- **`ContractGeneratorMain.vue`**: orquestador/padre del dominio. Usa `useContractWizard` para todo el estado y renderiza el paso activo (`paso` 1-4) dentro de una `<Transition>` (fade + slide horizontal entre pasos). El layout de los pasos 2-4 es de dos columnas (contenido del paso + `PreviewDocumento` al costado); el paso 1 (`TemplateSelector`) ocupa el ancho completo. Los botones "Atrás"/"Continuar" llaman a `anterior()`/`siguiente()` del composable.
- **`StepperNav.vue`**: indicador visual de progreso (1 Tipo — 2 Datos — 3 Estilo — 4 Descarga), con el paso activo resaltado y los pasos completados marcados con un check. Puramente presentacional (recibe `pasos` y `pasoActual` por props).
- **`TemplateSelector.vue`** (paso 1): grid de cards, una por tipo de contrato (`TemplateInfo` del backend: icono, nombre, descripcion). Selección unica via `v-model`.
- **`FormularioDatos.vue`** (paso 2): renderiza los inputs **dinamicamente** a partir de `campos: FieldSpec[]` (viene de la plantilla elegida) — no tiene ningun campo hardcodeado, por eso sirve igual para NDA, Contrato Laboral, etc. Es "tonto": recibe `data` y `errores` por props y muta `data` via `v-model` (el estado real vive en `useContractWizard`).
- **`SelectorEstilo.vue`** (paso 3): lista vertical de estilos disponibles como botones seleccionables (`v-model` sobre el `style_id` elegido).
- **`PreviewDocumento.vue`** (pasos 2-4): muestra el `content` (`titulo`/`parrafos`/`firmas`) que ya vino resuelto de `POST /api/contracts/preview` — este componente no arma texto, solo lo renderiza.

## Por que el preview le pega al backend (a diferencia de la primera version del proyecto)

Con una sola plantilla (NDA) el preview se resolvia con una maqueta hardcodeada en el frontend. Con 4 plantillas de contenido narrativo distinto, duplicar ese texto en dos lenguajes (Python y TypeScript) hubiera significado mantenerlo en dos lugares. `POST /api/contracts/preview` reutiliza `build_preview()` de la plantilla (la misma logica que arma el PDF real, solo que tolerante a campos incompletos) — con debounce de 200ms en `useContractWizard`, sigue siendo liviano.

## Por que el estado vive en un composable y no aca

`useContractWizard` (en `composables/contractGenerator/`) concentra el estado del wizard (paso actual, datos, seleccion) y su validacion. Esto permite testear la logica de navegacion entre pasos sin montar componentes, y mantiene estos componentes enfocados en la UI.
