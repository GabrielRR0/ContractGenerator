import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useLocale } from '../../i18n/useLocale'
import {
  fetchPreview,
  fetchStyles,
  fetchTemplates,
  generateContract,
  type ContractData,
  type PreviewContent,
  type StyleInfo,
  type TemplateInfo,
} from '../../services/contractGenerator/contract.service'
import { validateRequiredFields } from '../../utils/validators/validateContractFields'

export function useContractWizard() {
  const { locale, t } = useLocale()

  const paso = ref(1)
  const templates = ref<TemplateInfo[]>([])
  const styles = ref<StyleInfo[]>([])

  const templateId = ref<string | null>(null)
  const styleId = ref<string | null>(null)
  const data = reactive<ContractData>({})

  const errores = ref<string[]>([])
  const preview = ref<PreviewContent | null>(null)
  const generando = ref(false)
  const errorGeneracion = ref('')

  const pasos = computed(() => [t.value.stepTipo, t.value.stepDatos, t.value.stepEstilo, t.value.stepDescarga])
  const templateSeleccionado = computed(() => templates.value.find((tpl) => tpl.id === templateId.value) ?? null)

  async function cargarCatalogos() {
    ;[templates.value, styles.value] = await Promise.all([fetchTemplates(locale.value), fetchStyles(locale.value)])
    // Preseleccionar el primer estilo: es solo un refinamiento visual (a
    // diferencia del tipo de contrato, que si es una decision del usuario),
    // asi el preview del paso 3 ya muestra algo antes de tocar nada.
    styleId.value ??= styles.value[0]?.id ?? null
  }

  onMounted(cargarCatalogos)

  // Al cambiar de idioma, los nombres/etiquetas que vienen del backend
  // (templates, styles) hay que volver a pedirlos traducidos — los datos ya
  // cargados por el usuario (`data`) no se tocan, solo cambian las etiquetas.
  watch(locale, cargarCatalogos)

  // Debounce chico: evita pegarle al backend en cada tecla mientras el
  // usuario todavia esta escribiendo.
  let previewTimeout: ReturnType<typeof setTimeout> | undefined
  async function actualizarPreview() {
    if (!templateId.value) return
    clearTimeout(previewTimeout)
    previewTimeout = setTimeout(async () => {
      preview.value = await fetchPreview(templateId.value!, { ...data }, locale.value, styleId.value)
    }, 200)
  }

  // styleId entra al watch: antes el estilo no afectaba el preview de texto
  // (el estilo visual del preview es puro CSS), pero ahora tambien determina
  // la cantidad de paginas, asi que cambiar de estilo debe refrescarla.
  watch([templateId, data, locale, styleId], actualizarPreview, { deep: true })

  function validarPasoActual(): boolean {
    errores.value = []
    if (paso.value === 1 && !templateId.value) {
      errores.value = [t.value.errorChooseTemplate]
    } else if (paso.value === 2 && templateSeleccionado.value) {
      errores.value = validateRequiredFields(data, templateSeleccionado.value.campos, t.value.fieldRequiredSuffix)
    } else if (paso.value === 3 && !styleId.value) {
      errores.value = [t.value.errorChooseStyle]
    }
    return errores.value.length === 0
  }

  function siguiente() {
    if (!validarPasoActual()) return
    if (paso.value < pasos.value.length) paso.value += 1
  }

  function anterior() {
    errores.value = []
    if (paso.value > 1) paso.value -= 1
  }

  async function generar() {
    errorGeneracion.value = ''
    if (!templateId.value || !styleId.value) return

    generando.value = true
    try {
      // El backend devuelve el PDF binario directo (no JSON/base64), asi que
      // se recibe como Blob y se dispara la descarga simulando un click en un
      // <a download> temporal, sin navegar fuera de la SPA.
      const blob = await generateContract(templateId.value, styleId.value, { ...data }, locale.value)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'contrato.pdf'
      link.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      errorGeneracion.value = error instanceof Error ? error.message : 'Error'
    } finally {
      generando.value = false
    }
  }

  return {
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
  }
}
