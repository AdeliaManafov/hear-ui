<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="new-patient-card"
        rounded="lg"
    >

      <v-btn
          :to="backTarget"
          class="mb-4"
          color="primary"
          prepend-icon="mdi-arrow-left"
          size="small"
          variant="tonal"
      >
        {{ $t('form.back') }}
      </v-btn>
      <v-spacer/>
      <h1>{{ $t('form.title') }}</h1>
      <v-spacer/>
      <form v-if="definitionsReady" class="new-patient-form" @submit.prevent="submit">
        <!-- Required-fields info banner -->
        <v-alert
          v-if="!isEdit"
          type="info"
          variant="tonal"
          density="compact"
          class="mb-4"
          icon="mdi-information-outline"
        >
          <strong>{{ $t('form.minimum_fields_title', { defaultValue: 'Pflichtfelder für Vorhersage' }) }}:</strong>
          {{ $t('form.minimum_fields_hint', { defaultValue: 'Geschlecht, Alter und Hörminderung (operiertes Ohr) müssen ausgefüllt sein, damit eine Vorhersage berechnet werden kann. Weitere klinische Felder verbessern die Vorhersagequalität.' }) }}
        </v-alert>

        <template v-for="section in sectionedDefinitions" :key="section.name">
          <h3 class="section-title">{{ section.label }}</h3>
          <v-row dense>
            <template v-for="field in section.fields" :key="field.normalized">
              <v-col cols="12" md="6">
                <v-text-field
                  v-if="field.isDateMasked"
                  :model-value="formValues[field.normalized]"
                  @update:model-value="(val: any) => updateDateField(field.normalized, val)"
                  :label="field.label"
                  placeholder="TT.MM.JJJJ"
                  :error-messages="errorMessages(field.normalized)"
                  :error="!!requiredEmptyFields[field.normalized] || (submitAttempted && errorMessages(field.normalized).length > 0)"
                  color="primary"
                  hide-details="auto"
                  variant="outlined"
                  maxlength="10"
                />
                <component
                  v-else
                  :is="field.component"
                  :model-value="formValues[field.normalized]"
                  @update:model-value="(val: any) => updateField(field.normalized, val)"
                  :items="field.items"
                  item-title="title"
                  item-value="value"
                  :label="field.label"
                  :error-messages="errorMessages(field.normalized)"
                  :error="!!requiredEmptyFields[field.normalized] || (submitAttempted && errorMessages(field.normalized).length > 0)"
                  :type="field.inputType"
                  :multiple="field.multiple"
                  :chips="field.multiple"
                  :closable-chips="field.multiple"
                  :clearable="field.multiple"
                  :true-value="field.trueValue"
                  :false-value="field.falseValue"
                  color="primary"
                  hide-details="auto"
                  variant="outlined"
                />
              </v-col>
              <v-col
                v-if="field.otherField && isOtherSelected(field.normalized, formValues[field.normalized])"
                cols="12"
                md="6"
              >
                <v-text-field
                  :model-value="formValues[field.otherField]"
                  @update:model-value="(val: any) => updateField(field.otherField, val)"
                  :label="field.otherLabel"
                  :error-messages="errorMessages(field.otherField)"
                  :error="submitAttempted && errorMessages(field.otherField).length > 0"
                  color="primary"
                  hide-details="auto"
                  variant="outlined"
                />
              </v-col>
            </template>
          </v-row>
          <v-divider class="my-4"/>
        </template>

        <!-- Button row -->
        <div class="new-patient-actions">
          <v-btn
              class="me-4"
              color="primary"
              type="submit"
              variant="flat"
          >
            {{ $t('form.submit') }}
          </v-btn>
          <v-btn
              class="me-4"
              color="secondary"
              type="button"
              variant="tonal"
              @click="onReset"
          >
            {{ $t('form.reset') }}
          </v-btn>
        </div>
      </form>
      <div v-else class="new-patient-form">
        <p>{{ error ?? $t('form.error.submit_failed') }}</p>
      </div>
    </v-sheet>

    <v-snackbar
        v-model="updateSuccessOpen"
        color="success"
        location="top"
        timeout="2500"
    >
      {{ $t('patient_details.update_success') }}
    </v-snackbar>

    <v-snackbar
        v-model="submitErrorOpen"
        color="error"
        location="top"
        :timeout="6000"
        multi-line
    >
      {{ submitErrorMessage }}
      <template #actions>
        <v-btn variant="text" @click="submitErrorOpen = false">OK</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>


<script lang="ts" setup>
import {computed, onMounted, ref} from 'vue'
import {VCheckbox, VCombobox, VSelect, VTextField} from 'vuetify/components'
import {useForm} from 'vee-validate'
import i18next from 'i18next'
import {API_BASE} from '@/lib/api'
import {useRoute, useRouter} from 'vue-router'
import {useFeatureDefinitions} from '@/lib/featureDefinitions'
import {featureDefinitionsStore} from '@/lib/featureDefinitionsStore'

const language = ref(i18next.language)
i18next.on('languageChanged', (lng) => {
  language.value = lng
})

const route = useRoute()
const router = useRouter()
const rawId = route.params.id
const patientId = ref<string>(Array.isArray(rawId) ? rawId[0] : rawId ?? '')
const isEdit = computed(() => Boolean(patientId.value))
const backTarget = computed(() =>
  isEdit.value ? {name: 'PatientDetail', params: {id: patientId.value}} : {name: 'SearchPatients'}
)

const submitAttempted = ref(false)
const updateSuccessOpen = ref(false)
const submitErrorOpen = ref(false)
const submitErrorMessage = ref('')

const showError = (msg: string) => {
  submitErrorMessage.value = msg
  submitErrorOpen.value = true
}
const {definitions, definitionsByNormalized, labels, sections, error} = useFeatureDefinitions()
const definitionsReady = computed(() => (definitions.value ?? []).length > 0)

const featureDefinitions = computed(() => definitionsByNormalized.value)

const resolveOptionLabel = (option: any) => {
  const lang = language.value?.startsWith('de') ? 'de' : 'en'
  return option?.labels?.[lang] ?? option?.label ?? option?.value
}

const labelFor = (name: string, fallback?: string) => {
  return labels.value?.[name] ?? fallback ?? name
}

const sectionLabelFor = (name: string, fallback?: string) => {
  return sections.value?.[name] ?? fallback ?? name
}

const getOtherValues = (name: string) =>
  computed(() => {
    const options = featureDefinitions.value?.[name]?.options
    if (!Array.isArray(options)) return []
    return options.filter((opt: any) => opt?.is_other).map((opt: any) => opt.value)
  })

const isOtherSelected = (name: string, value: unknown) => {
  return getOtherValues(name).value.includes(String(value))
}

const getOptionValueByRole = (name: string, role: string, fallback: string) => {
  const options = featureDefinitions.value?.[name]?.options
  if (!Array.isArray(options)) return fallback
  const match = options.find((opt: any) => opt?.role === role)
  return match?.value ?? fallback
}

const errorMessages = (name: string) => {
  const msg = formErrors.value?.[name]
  return msg ? [msg] : []
}

const buildItems = (def: any) => {
  if (!Array.isArray(def?.options)) return undefined
  return def.options.map((opt: any) => ({
    title: resolveOptionLabel(opt),
    value: opt.value,
  }))
}

const isCheckboxField = (def: any) => {
  if (def?.type === 'boolean') return true
  if (!Array.isArray(def?.options) || def?.multiple) return false
  const roles = def.options.map((opt: any) => opt?.role).filter(Boolean)
  if (roles.includes('true') && roles.includes('false')) return true
  if (def.options.length === 2) {
    const values = def.options.map((opt: any) => String(opt?.value ?? '').toLowerCase())
    const hasPresent = values.includes('vorhanden')
    const hasNone = values.includes('kein') || values.includes('keine')
    return hasPresent && hasNone
  }
  return false
}

const getCheckboxValues = (def: any) => {
  if (!Array.isArray(def?.options)) {
    return {trueValue: 'Vorhanden', falseValue: 'Keine'}
  }
  const values = def.options.map((opt: any) => opt?.value)
  const trueValue =
    values.find((val: any) => String(val).toLowerCase() === 'vorhanden') ??
    values[0] ??
    'Vorhanden'
  const falseValue =
    values.find((val: any) => {
      const lower = String(val).toLowerCase()
      return lower === 'kein' || lower === 'keine'
    }) ??
    values[1] ??
    'Keine'
  return {trueValue, falseValue}
}

const getFieldComponent = (def: any) => {
  if (isCheckboxField(def)) return VCheckbox
  if (def?.multiple) return VCombobox
  if (Array.isArray(def?.options)) return VSelect
  return VTextField
}

const sectionedDefinitions = computed(() => {
  const defs = definitions.value ?? []
  const otherFieldNames = new Set(
    defs.map((def: any) => def?.other_field).filter(Boolean)
  )
  const order: string[] = []
  const grouped: Record<string, any[]> = {}

  for (const def of defs) {
    if (!def?.normalized) continue
    if (otherFieldNames.has(def.normalized)) continue
    const section = def.section ?? 'Weitere'
    if (!order.includes(section)) order.push(section)
    grouped[section] = grouped[section] ?? []
    grouped[section].push(def)
  }

  const filtered = order.filter((section) => section !== 'Weitere')
  const visibleSections = filtered.length > 0 ? filtered : order

  return visibleSections.map((section) => ({
      name: section,
      label: sectionLabelFor(section),
      fields: (grouped[section] ?? []).map((def: any) => ({
        normalized: def.normalized,
        label: labelFor(def.normalized, def.description ?? def.raw),
        component: getFieldComponent(def),
        inputType: def.input_type === 'number' ? 'number' : undefined,
        isDateMasked: def.input_type === 'date',
        items: buildItems(def),
        multiple: Boolean(def.multiple),
        trueValue: isCheckboxField(def)
          ? getCheckboxValues(def).trueValue
          : getOptionValueByRole(def.normalized, 'true', 'Vorhanden'),
        falseValue: isCheckboxField(def)
          ? getCheckboxValues(def).falseValue
          : getOptionValueByRole(def.normalized, 'false', 'Keine'),
        otherField: def.other_field,
        otherLabel: def.other_field ? labelFor(def.other_field, def.other_field) : undefined,
      }))
    }))
})

const validationSchema = computed(() => {
  const _lang = language.value
  const defs = definitions.value ?? []
  const schema: Record<string, any> = {}

  const requiredMessage = () => i18next.t('form.error.name')

  const isEmptyValue = (value: unknown, def: any) => {
    if (def?.multiple) return !Array.isArray(value) || value.length === 0
    if (def?.input_type === 'number') {
      if (value === undefined || value === null || value === '') return true
      const numericValue = typeof value === 'number' ? value : Number(value)
      return !Number.isFinite(numericValue)
    }
    return value === undefined || value === null || value === ''
  }

  const getAllowedValues = (def: any) => {
    if (def?.validation?.type === 'enum_one_of') {
      return Array.isArray(def.validation.allowed) ? def.validation.allowed : []
    }
    if (Array.isArray(def?.options)) {
      return def.options.map((opt: any) => opt.value)
    }
    return []
  }

  for (const def of defs) {
    if (!def?.normalized) continue
    const allowed = getAllowedValues(def)

    schema[def.normalized] = (value: unknown, ctx: any) => {
      if (def.required && isEmptyValue(value, def)) return requiredMessage()
      if (!isEmptyValue(value, def) && allowed.length > 0) {
        if (def.multiple && Array.isArray(value)) {
          const normalized = normalizeImagingValue(value)
          const allAllowed = normalized.every((entry) => allowed.includes(entry))
          if (!allAllowed) return requiredMessage()
        } else if (!allowed.includes(value as any)) {
          return requiredMessage()
        }
      }
      return true
    }

    if (def.other_field) {
      schema[def.other_field] = (value: unknown, ctx: any) => {
        if (isOtherSelected(def.normalized, ctx?.form?.[def.normalized])) {
          if (value === undefined || value === null || value === '') return requiredMessage()
        }
        return true
      }
    }
  }

  return schema
})

const {handleSubmit, handleReset, setFieldTouched, setFieldValue, values, errors} = useForm({
  validationSchema,
})

const formValues = values
const formErrors = computed(() => errors.value ?? {})
const updateField = (name: string, value: any) => setFieldValue(name, value)

// Collect all normalized names of required fields for immediate red-border feedback
const requiredFieldNames = computed<Set<string>>(() => {
  return new Set(
    (definitions.value ?? [])
      .filter((def: any) => def?.required === true && def?.normalized)
      .map((def: any) => def.normalized as string)
  )
})

// Reactive map: fieldName → true when field is required, submit was attempted, and field is empty
const requiredEmptyFields = computed<Record<string, boolean>>(() => {
  const result: Record<string, boolean> = {}
  if (!submitAttempted.value) return result
  for (const name of requiredFieldNames.value) {
    const val = (formValues as Record<string, unknown>)[name]
    const isEmpty = Array.isArray(val)
      ? val.length === 0
      : val === undefined || val === null || val === ''
    if (isEmpty) result[name] = true
  }
  return result
})

const formatDateInput = (raw: string): string => {
  const digits = raw.replace(/\D/g, '').slice(0, 8)
  if (digits.length <= 2) return digits
  if (digits.length <= 4) return `${digits.slice(0, 2)}.${digits.slice(2)}`
  return `${digits.slice(0, 2)}.${digits.slice(2, 4)}.${digits.slice(4)}`
}

const updateDateField = (name: string, val: any) => {
  const str = typeof val === 'string' ? val : ''
  setFieldValue(name, formatDateInput(str))
}

const normalizeImagingValue = (val: unknown): string[] => {
  if (Array.isArray(val)) {
    return val
      .map((entry: any) => (entry && typeof entry === 'object' ? entry.value : entry))
      .filter((entry) => entry !== undefined && entry !== null && entry !== '')
      .map((entry) => String(entry))
  }
  if (val === undefined || val === null || val === '') return []
  if (typeof val === 'object') {
    const value = (val as any)?.value
    return value === undefined || value === null || value === '' ? [] : [String(value)]
  }
  return [String(val)]
}

const formFieldNames = computed(() => Object.keys(definitionsByNormalized.value ?? {}))


const resolveOther = (value: unknown, other: unknown, triggers: string[]) => {
  if (typeof value === 'string' && triggers.includes(value)) return other
  return value
}

const withDefault = (value: any, fallback = 'Keine') => {
  if (Array.isArray(value)) return value.length ? value : fallback
  if (value === undefined || value === null || value === '') return fallback
  return value
}


const normalizeErrors = (errors: Record<string, unknown>) => {
  const toMessage = (err: unknown): string | undefined => {
    if (!err) return undefined
    if (typeof err === 'string') return err
    if (err instanceof Error) return err.message
    if (Array.isArray(err)) {
      const nested = err.map(toMessage).filter(Boolean) as string[]
      return nested.length ? nested.join('\n') : undefined
    }
    if (typeof err === 'object') {
      try {
        const serialized = JSON.stringify(err)
        return serialized === '{}' ? undefined : serialized
      } catch (e) {
        return String(err)
      }
    }
    return String(err)
  }

  const messages: string[] = []
  Object.values(errors || {}).forEach(err => {
    const msg = toMessage(err)
    if (msg) messages.push(msg)
  })
  return messages
}

const stableStringify = (value: any): string => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`
  const keys = Object.keys(value).sort()
  const entries = keys.map(k => `${JSON.stringify(k)}:${stableStringify(value[k])}`)
  return `{${entries.join(',')}}`
}

const buildSnapshot = (formValues: Record<string, any>) => {
  const displayName = [formValues.last_name, formValues.first_name].filter(Boolean).join(", ")
  return {
    display_name: displayName || null,
    input_features: buildInputFeatures(formValues),
  }
}

const splitImagingTypes = (value: unknown): string[] => {
  if (Array.isArray(value)) return value.map(v => String(v).trim()).filter(Boolean)
  if (typeof value !== 'string') return []
  return value
    .split(',')
    .map(v => v.trim())
    .filter(Boolean)
    .map(v => {
      const lower = v.toLowerCase()
      if (lower === 'ct') return 'CT'
      if (lower === 'mrt') return 'MRT'
      if (lower === 'konventionell') return 'Konventionell'
      return v
    })
}

const buildInputFeatures = (values: Record<string, any>) => {
  const input_features: Record<string, any> = {}
  const defs = Object.values(definitionsByNormalized.value ?? {})

  for (const def of defs) {
    if (!def?.raw || def.ui_only) continue
    let value = values[def.normalized]

    if (def.other_field && isOtherSelected(def.normalized, value)) {
      value = values[def.other_field]
    }

    if (def.multiple) {
      const normalized = normalizeImagingValue(value)
      value = withDefault(normalized.join(', '))
    } else if (def.input_type === 'number') {
      value = Number(value)
    } else if (typeof value === 'boolean') {
      value = getOptionValueByRole(def.normalized, value ? 'true' : 'false', value ? 'Vorhanden' : 'Keine')
    } else {
      const fallback = getOptionValueByRole(def.normalized, 'false', 'Keine')
      value = withDefault(value, fallback)
    }

    input_features[def.raw] = value
  }

  return input_features
}

const initialSnapshot = ref<string | null>(null)

const populateFormForEdit = (patient: any) => {
  const input = patient?.input_features || {}
  const displayName = String(patient?.display_name || '')
  let first = ''
  let last = ''
  if (displayName.includes(',')) {
    const parts = displayName.split(',').map(p => p.trim())
    last = parts[0] || ''
    first = parts.slice(1).join(', ').trim()
  } else if (displayName.includes(' ')) {
    const parts = displayName.split(' ').filter(Boolean)
    first = parts[0] || ''
    last = parts.slice(1).join(' ').trim()
  } else {
    last = displayName
  }

  setFieldValue('first_name', first)
  setFieldValue('last_name', last)

  const defs = definitions.value ?? []
  for (const def of defs) {
    if (!def?.normalized || def.ui_only) continue
    if (def.normalized === 'first_name' || def.normalized === 'last_name') continue
    const rawValue = input?.[def.raw]

    if (def.multiple) {
      setFieldValue(def.normalized, splitImagingTypes(rawValue))
      continue
    }

    if (Array.isArray(def.options)) {
      const optionValues = def.options.map((opt: any) => opt.value)
      if (optionValues.includes(rawValue)) {
        setFieldValue(def.normalized, rawValue)
      } else if (def.other_field && rawValue !== undefined && rawValue !== null && rawValue !== '') {
        const otherOptions = getOtherValues(def.normalized).value
        if (otherOptions.length) {
          setFieldValue(def.normalized, otherOptions[0])
          setFieldValue(def.other_field, rawValue)
        } else {
          setFieldValue(def.normalized, rawValue)
        }
      } else {
        setFieldValue(def.normalized, rawValue ?? '')
      }
      continue
    }

    setFieldValue(def.normalized, rawValue ?? '')
  }

  initialSnapshot.value = stableStringify(buildSnapshot(values as Record<string, any>))
}

const onSubmit = handleSubmit(
  async values => {
    try {
      const payload = buildSnapshot(values)
      if (isEdit.value && initialSnapshot.value === stableStringify(payload)) {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: patientId.value}})
        return
      }

      const method = isEdit.value ? 'PUT' : 'POST'
      const url = isEdit.value
        ? `${API_BASE}/api/v1/patients/${encodeURIComponent(patientId.value)}`
        : `${API_BASE}/api/v1/patients/`

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
        body: JSON.stringify({
          input_features: payload.input_features,
          display_name: payload.display_name || undefined,
        }),
      })

      if (!response.ok) {
        const contentType = response.headers.get('content-type') || ''
        let errorMessage = 'Failed to create patient'
        try {
          if (contentType.includes('application/json')) {
            const data = await response.json()
            const rawDetail = (data?.detail as string) ?? JSON.stringify(data)
            // Translate minimum-fields backend error to current UI language
            if (rawDetail && rawDetail.includes('Mindestfelder')) {
              errorMessage = i18next.t('form.minimum_fields_error')
            } else if (rawDetail && rawDetail.includes('Pflichtfelder')) {
              errorMessage = i18next.t('form.required_fields_error')
            } else {
              errorMessage = rawDetail
            }
          } else {
            const text = await response.text()
            errorMessage = text || errorMessage
          }
        } catch (e) {
          // fall back to default message
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      if (isEdit.value) {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: patientId.value}, query: {updated: '1'}})
      } else {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: data.id}, query: {created: '1'}})
      }
    } catch (err: any) {
      showError(err?.message ?? i18next.t('form.error.submit_failed'))
    }
  },
  (errors) => {
    formFieldNames.value.forEach(name => setFieldTouched(name, true, true))
    const messages = normalizeErrors(errors)
    showError(messages.length ? messages.join('\n') : i18next.t('form.error.fix_fields'))
  }
)

const submit = async () => {
  submitAttempted.value = true
  await onSubmit()
}

const onReset = () => {
  submitAttempted.value = false
  handleReset()
}

onMounted(async () => {
  if (!definitionsReady.value) {
    await featureDefinitionsStore.loadDefinitions()
    await featureDefinitionsStore.loadLabels(language.value)
  }
  if (!isEdit.value) return
  try {
    const response = await fetch(
      `${API_BASE}/api/v1/patients/${encodeURIComponent(patientId.value)}`,
      {
        method: 'GET',
        headers: {accept: 'application/json'},
      }
    )
    if (!response.ok) throw new Error('Failed to load patient')
    const data = await response.json()
    populateFormForEdit(data)
  } catch (err) {
    console.error(err)
    showError(err instanceof Error ? err.message : 'Failed to load patient')
  }
})
</script>


<style scoped>
.new-patient-card {
  padding: 32px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}

/* space between title and first row */
.new-patient-card h1 {
  margin: 8px 0 24px 0;
}

.section-title {
  margin: 12px 0 8px;
  font-weight: 600;
}

.field-description {
  margin: 4px 0 6px;
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-size: 0.92rem;
}

/* form layout */
.new-patient-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* buttons aligned like in the mockup */
.new-patient-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}
</style>
