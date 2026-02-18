<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="predictions-home-sheet"
        rounded="lg"
    >
      <!-- Title -->
      <v-row justify="start" no-gutters>
        <h1>{{ $t('predictions_home.title') }}</h1>
      </v-row>

      <v-divider class="my-6"/>

      <!-- About Section -->
      <v-row>
        <v-col>
          <h2>{{ $t('predictions_home.about.title') }}</h2>
          <p class="text-medium-emphasis mt-2">
            {{ $t('predictions_home.about.description') }}
          </p>
        </v-col>
      </v-row>

      <!-- How to get a prediction -->
      <v-row>
        <div>
          <v-col>
            <h2>{{ $t('predictions_home.process.title') }}</h2>
            <v-timeline align="start" class="mt-4" density="compact" side="end">
              <v-timeline-item
                  dot-color="primary"
                  fill-dot
                  icon="mdi-magnify"
                  size="small"
              >
                <div class="d-flex">
                  <strong class="me-4">{{ $t('predictions_home.process.step1.title') }}</strong>
                  <div>{{ $t('predictions_home.process.step1.description') }}</div>
                </div>
              </v-timeline-item>
              <v-timeline-item
                  dot-color="primary"
                  fill-dot
                  icon="mdi-account-plus"
                  size="small"
              >
                <div class="d-flex">
                  <strong class="me-4">{{ $t('predictions_home.process.step2.title') }}</strong>
                  <div>{{ $t('predictions_home.process.step2.description') }}</div>
                </div>
              </v-timeline-item>
              <v-timeline-item
                  dot-color="primary"
                  fill-dot
                  icon="mdi-account-details"
                  size="small"
              >
                <div class="d-flex">
                  <strong class="me-4">{{ $t('predictions_home.process.step3.title') }}</strong>
                  <div>{{ $t('predictions_home.process.step3.description') }}</div>
                </div>
              </v-timeline-item>
              <v-timeline-item
                  dot-color="primary"
                  fill-dot
                  icon="mdi-creation"
                  size="small"
              >
                <div class="d-flex">
                  <strong class="me-4">{{ $t('predictions_home.process.step4.title') }}</strong>
                  <div>{{ $t('predictions_home.process.step4.description') }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-col>
        </div>
      </v-row>
      <v-spacer class="my-6 mb-8"></v-spacer>

      <v-divider class="my-6 mb-8"/>

      <!-- Action Buttons -->
      <div class="d-flex justify-center ga-4 mt-8">
        <v-btn
            :to="{ name: 'SearchPatients' }"
            color="primary"
            prepend-icon="mdi-magnify"
            size="large"
            flat
        >
          {{ $t('predictions_home.action_cards.search_patients.title') }}
        </v-btn>
        <v-btn
            :to="{ name: 'CreatePatient' }"
            color="primary"
            prepend-icon="mdi-account-plus"
            size="large"
            flat
        >
          {{ $t('predictions_home.action_cards.create_patient.title') }}
        </v-btn>
      </div>

      <v-divider class="my-6 mb-8"/>

      <!-- Model Card Section -->
      <v-row>
        <v-col>
          <v-card class="model-card-professional" elevation="3">

            <!-- Header -->
            <v-card-title class="model-card-header text-white pa-6">
              <div class="text-h4 font-weight-bold">{{ meta.name }}</div>
            </v-card-title>

            <!-- Metadata Bar -->
            <div class="model-card-metadata pa-4 bg-grey-lighten-4">
              <v-row dense>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.version') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ meta.version }}</div>
                </v-col>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.model_type') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ meta.modelType }}</div>
                </v-col>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.last_updated') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ meta.lastUpdated }}</div>
                </v-col>
              </v-row>
            </div>

            <v-card-text class="pa-6">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-12">
                <v-progress-circular indeterminate color="primary" size="64"/>
                <p class="mt-4 text-grey">{{ $t('predictions_home.model_cards.loading', { defaultValue: 'Lädt...' }) }}</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="text-center py-12">
                <v-icon color="error" size="64">mdi-alert-circle-outline</v-icon>
                <p class="mt-4 text-error">{{ error }}</p>
                <v-btn @click="loadModelCard" variant="outlined" color="primary" class="mt-4">
                  {{ $t('predictions_home.model_cards.retry', { defaultValue: 'Erneut versuchen' }) }}
                </v-btn>
              </div>

              <!-- Rendered Markdown -->
              <div
                v-else
                class="model-card-markdown"
                v-html="renderedHtml"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

    </v-sheet>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { API_BASE } from '@/lib/api'
import { useTranslation } from 'i18next-vue'

const { i18next } = useTranslation()

const loading = ref(true)
const error = ref('')
const rawMarkdown = ref('')

interface Meta { name: string; version: string; modelType: string; lastUpdated: string }

const meta = ref<Meta>({
  name: 'HEAR CI Prediction Model',
  version: 'v3.0',
  modelType: 'RandomForestClassifier',
  lastUpdated: new Date().toISOString().slice(0, 10),
})

// Configure marked: GitHub-flavoured Markdown with line breaks
marked.setOptions({ gfm: true, breaks: true } as Parameters<typeof marked.setOptions>[0])

const renderedHtml = computed(() => {
  if (!rawMarkdown.value) return ''
  const html = marked.parse(rawMarkdown.value) as string
  return DOMPurify.sanitize(html)
})

/** Extract the handful of metadata values we show in the header bar. */
function extractMeta(md: string): Meta {
  const title = md.match(/^#\s+(.+)$/m)?.[1] ?? meta.value.name
  const version = md.match(/\*\*Version:\*\*\s*([^\s\n]+)/i)?.[1] ?? meta.value.version
  const modelType = md.match(/\*\*(?:Modelltyp|Model Type):\*\*\s*(.+?)(?:\s{2,}|\n)/i)?.[1]?.trim() ?? meta.value.modelType
  const lastUpdated = md.match(/\*\*(?:Letzte Aktualisierung|Last Updated):\*\*\s*(.+?)(?:\s{2,}|\n)/i)?.[1]?.trim() ?? meta.value.lastUpdated
  return { name: title, version, modelType, lastUpdated }
}

async function loadModelCard() {
  loading.value = true
  error.value = ''
  try {
    const lang = i18next.language?.startsWith('en') ? 'en' : 'de'
    const res = await fetch(`${API_BASE}/api/v1/model-card?lang=${lang}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const text = await res.text()
    rawMarkdown.value = text
    meta.value = extractMeta(text)
  } catch (err) {
    error.value = String(err)
  } finally {
    loading.value = false
  }
}

watch(() => i18next.language, () => loadModelCard())
onMounted(() => loadModelCard())
</script>

<style scoped>
.predictions-home-sheet {
  padding: 32px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}

/* Professional Model Card Styles */
.model-card-professional {
  border-radius: 8px !important;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.model-card-header {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-primary-darken-1)) 100%);
}

.model-card-metadata {
  border-bottom: 1px solid #e0e0e0;
}

/* ── Rendered Markdown Styles ─────────────────────────────────── */
.model-card-markdown {
  line-height: 1.75;
  color: rgba(0, 0, 0, 0.82);
  font-size: 0.96rem;
}

/* H1 (model name) – hidden, already in header bar */
.model-card-markdown :deep(h1) { display: none; }

/* Section headings */
.model-card-markdown :deep(h2) {
  font-size: 1.15rem;
  font-weight: 700;
  color: rgb(var(--v-theme-primary));
  margin: 2rem 0 0.6rem;
  padding-bottom: 0.35rem;
  border-bottom: 2px solid rgb(var(--v-theme-primary));
}

.model-card-markdown :deep(h3) {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.78);
  margin: 1.2rem 0 0.4rem;
  padding-left: 0.5rem;
  border-left: 3px solid rgb(var(--v-theme-primary));
}

/* Paragraphs & Metadata line (Version / Modelltyp / ...) */
.model-card-markdown :deep(p) {
  margin: 0.4rem 0;
}

/* Metadata block right after the title – hide (shown in header bar) */
.model-card-markdown :deep(p:first-of-type) { display: none; }

/* Unordered + ordered lists */
.model-card-markdown :deep(ul),
.model-card-markdown :deep(ol) {
  padding-left: 1.6rem;
  margin: 0.5rem 0 1rem;
}

.model-card-markdown :deep(li) {
  margin-bottom: 0.3rem;
  line-height: 1.65;
}

/* Bold labels inside lists */
.model-card-markdown :deep(li strong),
.model-card-markdown :deep(p strong) {
  color: rgba(0, 0, 0, 0.87);
}

/* Italic descriptions under group headings */
.model-card-markdown :deep(em) {
  color: rgba(0, 0, 0, 0.55);
  font-size: 0.9rem;
}

/* Horizontal rule */
.model-card-markdown :deep(hr) {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 1.5rem 0;
}

/* Blockquote (hints / notes) */
.model-card-markdown :deep(blockquote) {
  border-left: 4px solid rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.06);
  margin: 1rem 0;
  padding: 0.6rem 1rem;
  border-radius: 0 6px 6px 0;
  color: rgba(0, 0, 0, 0.7);
  font-style: italic;
}

/* Code inline */
.model-card-markdown :deep(code) {
  background: #f4f4f4;
  border-radius: 4px;
  padding: 0.1em 0.35em;
  font-size: 0.88em;
  color: #c62828;
}

/* Numbered feature list → display as chips grid */
.model-card-markdown :deep(ol) {
  list-style: none;
  padding-left: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0.5rem 0 1rem;
}

.model-card-markdown :deep(ol li) {
  background: rgba(var(--v-theme-primary), 0.08);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  border-radius: 16px;
  padding: 0.2rem 0.75rem;
  font-size: 0.82rem;
  color: rgb(var(--v-theme-primary));
  margin-bottom: 0;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .model-card-markdown { font-size: 0.92rem; }
  .model-card-markdown :deep(h2) { font-size: 1.05rem; }
  .model-card-markdown :deep(ol li) { white-space: normal; }
}
</style>

