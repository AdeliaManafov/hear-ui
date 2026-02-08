import {ref, computed, readonly, type Ref} from 'vue'
import i18next from 'i18next'
import {API_BASE} from '@/lib/api'

export type FeatureOption = {
  value: string
  labels?: Record<string, string>
  role?: string
  is_other?: boolean
}

export type FeatureDefinition = {
  raw: string
  normalized: string
  description?: string
  section?: string
  options?: FeatureOption[]
  input_type?: string
  multiple?: boolean
  other_field?: string
  ui_only?: boolean
}

type FeatureDefinitionsState = {
  definitions: Ref<FeatureDefinition[]>
  definitionsByNormalized: Ref<Record<string, FeatureDefinition>>
  labels: Ref<Record<string, string>>
  sections: Ref<Record<string, string>>
  loading: Ref<boolean>
  loadDefinitions: () => Promise<void>
  loadLabels: (locale?: string) => Promise<void>
}

const definitions = ref<FeatureDefinition[]>([])
const labels = ref<Record<string, string>>({})
const sections = ref<Record<string, string>>({})
const loading = ref(false)

const definitionsByNormalized = computed(() => {
  return Object.fromEntries(
    definitions.value
      .filter((entry) => entry?.normalized)
      .map((entry) => [entry.normalized, entry])
  )
})

const loadDefinitions = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/api/v1/features/definitions`, {
      method: 'GET',
      headers: {accept: 'application/json'},
    })
    if (!response.ok) throw new Error('Failed to load feature definitions')
    const data = await response.json()
    definitions.value = Array.isArray(data?.features) ? data.features : []
  } catch (err) {
    console.error(err)
    definitions.value = []
  } finally {
    loading.value = false
  }
}

const loadLabels = async (locale?: string) => {
  const lang = locale ?? i18next.language
  try {
    const response = await fetch(`${API_BASE}/api/v1/features/locales/${encodeURIComponent(lang)}`, {
      method: 'GET',
      headers: {accept: 'application/json'},
    })
    if (!response.ok) throw new Error('Failed to load feature locales')
    const data = await response.json()
    labels.value = data?.labels ?? {}
    sections.value = data?.sections ?? {}
  } catch (err) {
    console.error(err)
    labels.value = {}
    sections.value = {}
  }
}

export const featureDefinitionsStore: FeatureDefinitionsState = {
  definitions,
  definitionsByNormalized: computed(() => definitionsByNormalized.value) as Ref<Record<string, FeatureDefinition>>,
  labels,
  sections,
  loading,
  loadDefinitions,
  loadLabels,
}

export const useFeatureDefinitionsStore = () => readonly(featureDefinitionsStore)
