# utils/validators

Funciones puras de validacion, sin estado ni dependencia de Vue. Reciben datos y devuelven una lista de errores (nunca lanzan excepciones ni tocan el DOM).

## Archivos

- **`validateContractFields.ts`**: `validateRequiredFields(data, campos)` revisa, de forma generica, que cada `campo` de la plantilla activa (`FieldSpec[]`, viene del backend) tenga un valor no vacio en `data` (usa `.trim()` para rechazar strings de solo espacios). No sabe de NDA ni de ningun tipo de contrato en particular — sirve igual para las 4 plantillas porque recibe la lista de campos requeridos como parametro.

## Por que son funciones puras separadas de `useContractWizard.ts`

Al no depender de `ref`/`reactive` de Vue, se pueden testear con datos planos (`{ parte_reveladora: '' }`) sin montar ningun composable ni componente, y reutilizar si en el futuro se valida el mismo formulario fuera de un componente Vue (ej. en un test de integracion del backend-para-frontend).
