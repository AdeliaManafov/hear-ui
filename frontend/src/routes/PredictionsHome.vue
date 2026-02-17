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

      <!-- Model Cards Section -->
      <v-row>
        <v-col>
          <v-card 
            class="model-card-professional" 
            elevation="3"
          >
            <!-- Header -->
            <v-card-title class="model-card-header text-white pa-6">
              <div class="text-h4 font-weight-bold">{{ modelCardData.name || 'HEAR CI Prediction Model' }}</div>
            </v-card-title>

            <!-- Metadata Bar -->
            <div class="model-card-metadata pa-4 bg-grey-lighten-4">
              <v-row dense>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.version') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ modelCardData.version || 'v1.0' }}</div>
                </v-col>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.model_type') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ modelCardData.modelType || 'RandomForestClassifier' }}</div>
                </v-col>
                <v-col cols="12" md="4">
                  <div class="text-caption text-grey-darken-1">{{ $t('predictions_home.model_cards.header.last_updated') }}</div>
                  <div class="text-body-1 font-weight-medium">{{ modelCardData.lastUpdated || '2026-02-17' }}</div>
                </v-col>
              </v-row>
            </div>

            <v-card-text class="pa-6">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-12">
                <v-progress-circular 
                  indeterminate 
                  color="primary"
                  size="64"
                />
                <p class="mt-4 text-grey">{{ $t('predictions_home.model_cards.loading', {defaultValue: 'Loading model card...'}) }}</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="text-center py-12">
                <v-icon color="error" size="64">mdi-alert-circle-outline</v-icon>
                <p class="mt-4 text-error">{{ error }}</p>
                <v-btn 
                  @click="loadModelCard" 
                  variant="outlined" 
                  color="primary"
                  class="mt-4"
                >
                  {{ $t('predictions_home.model_cards.retry', {defaultValue: 'Retry'}) }}
                </v-btn>
              </div>

              <!-- Content Sections -->
              <div v-else class="model-card-sections">
                <!-- Model Description -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.model_description.title') }}</div>
                  <p class="mb-2"><strong>{{ $t('predictions_home.model_cards.model_description.description') }}</strong></p>
                  <ul class="section-list">
                    <li><strong>{{ $t('predictions_home.model_cards.model_description.training_data') }}:</strong> {{ $t('predictions_home.model_cards.model_description.training_data_value') }}</li>
                    <li><strong>{{ $t('predictions_home.model_cards.model_description.train_test_split') }}:</strong> 80/20</li>
                    <li><strong>{{ $t('predictions_home.model_cards.model_description.features') }}:</strong> {{ $t('predictions_home.model_cards.model_description.features_value') }}</li>
                  </ul>
                </div>

                <!-- Intended Use -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.intended_use.title') }}</div>
                  <p class="font-weight-bold mb-2">{{ $t('predictions_home.model_cards.intended_use.purpose') }}:</p>
                  <ul class="section-list">
                    <li>{{ $t('predictions_home.model_cards.intended_use.purpose_1') }}</li>
                    <li>{{ $t('predictions_home.model_cards.intended_use.purpose_2') }}</li>
                    <li>{{ $t('predictions_home.model_cards.intended_use.purpose_3') }}</li>
                  </ul>
                  <p class="font-weight-bold mb-2 mt-4">{{ $t('predictions_home.model_cards.intended_use.not_intended') }}:</p>
                  <ul class="section-list">
                    <li>{{ $t('predictions_home.model_cards.intended_use.not_intended_1') }}</li>
                    <li>{{ $t('predictions_home.model_cards.intended_use.not_intended_2') }}</li>
                    <li>{{ $t('predictions_home.model_cards.intended_use.not_intended_3') }}</li>
                    <li>{{ $t('predictions_home.model_cards.intended_use.not_intended_4') }}</li>
                  </ul>
                </div>

                <!-- Limitations -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.limitations.title') }}</div>
                  <ul class="section-list">
                    <li>{{ $t('predictions_home.model_cards.limitations.item_1') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_2') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_3') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_4') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_5') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_6') }}</li>
                    <li>{{ $t('predictions_home.model_cards.limitations.item_7') }}</li>
                  </ul>
                </div>

                <!-- Recommendations -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.recommendations.title') }}</div>
                  <ul class="section-list">
                    <li>{{ $t('predictions_home.model_cards.recommendations.item_1') }}</li>
                    <li>{{ $t('predictions_home.model_cards.recommendations.item_2') }}</li>
                    <li>{{ $t('predictions_home.model_cards.recommendations.item_3') }}</li>
                    <li>{{ $t('predictions_home.model_cards.recommendations.item_4') }}</li>
                    <li>{{ $t('predictions_home.model_cards.recommendations.item_5') }}</li>
                  </ul>
                </div>

                <!-- Model Metrics -->
                <div v-if="modelCardData.metrics" class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.performance.title') }}</div>
                  <p class="text-body-2 text-grey-darken-1 mb-3">{{ $t('predictions_home.model_cards.performance.dataset') }}</p>
                  <v-row dense class="mt-2">
                    <v-col v-if="modelCardData.metrics.accuracy" cols="6" md="3">
                      <div class="metric-item">
                        <div class="metric-label">{{ $t('predictions_home.model_cards.performance.accuracy') }}</div>
                        <div class="metric-value">{{ (modelCardData.metrics.accuracy * 100).toFixed(1) }}%</div>
                      </div>
                    </v-col>
                    <v-col v-if="modelCardData.metrics.f1_score" cols="6" md="3">
                      <div class="metric-item">
                        <div class="metric-label">{{ $t('predictions_home.model_cards.performance.f1_score') }}</div>
                        <div class="metric-value">{{ modelCardData.metrics.f1_score.toFixed(2) }}</div>
                      </div>
                    </v-col>
                    <v-col v-if="modelCardData.metrics.precision" cols="6" md="3">
                      <div class="metric-item">
                        <div class="metric-label">{{ $t('predictions_home.model_cards.performance.precision') }}</div>
                        <div class="metric-value">{{ (modelCardData.metrics.precision * 100).toFixed(1) }}%</div>
                      </div>
                    </v-col>
                    <v-col v-if="modelCardData.metrics.recall" cols="6" md="3">
                      <div class="metric-item">
                        <div class="metric-label">{{ $t('predictions_home.model_cards.performance.recall') }}</div>
                        <div class="metric-value">{{ (modelCardData.metrics.recall * 100).toFixed(1) }}%</div>
                      </div>
                    </v-col>
                    <v-col v-if="modelCardData.metrics.roc_auc" cols="6" md="3">
                      <div class="metric-item">
                        <div class="metric-label">{{ $t('predictions_home.model_cards.performance.roc_auc') }}</div>
                        <div class="metric-value">{{ modelCardData.metrics.roc_auc.toFixed(2) }}</div>
                      </div>
                    </v-col>
                  </v-row>
                  <p class="text-caption text-grey-darken-1 mt-3 font-italic">{{ $t('predictions_home.model_cards.performance.hint') }}</p>
                </div>

                <!-- Features with Expansion Panels -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.features.title') }}</div>
                  <p class="text-body-2 text-grey-darken-1 mb-3">{{ $t('predictions_home.model_cards.features.selected_note') }}</p>
                  
                  <div v-if="Object.keys(modelCardData.featureGroups).length === 0" class="text-grey">
                    Laden...
                  </div>
                  
                  <v-expansion-panels v-else class="mt-3" variant="accordion" multiple>
                    <v-expansion-panel
                      v-for="(group, groupName) in modelCardData.featureGroups"
                      :key="groupName"
                    >
                      <v-expansion-panel-title class="feature-group-title">
                        <strong>{{ groupName }}</strong>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <div class="feature-list">
                          <v-chip
                            v-for="(feature, idx) in group"
                            :key="idx"
                            class="ma-1"
                            size="small"
                            variant="outlined"
                            color="primary"
                          >
                            {{ feature }}
                          </v-chip>
                        </div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>

                <!-- XAI / Interpretability -->
                <div class="model-card-section">
                  <div class="section-title">{{ $t('predictions_home.model_cards.xai.title') }}</div>
                  <ul class="section-list">
                    <li>{{ $t('predictions_home.model_cards.xai.shap') }}</li>
                    <li>{{ $t('predictions_home.model_cards.xai.important_factors') }}</li>
                    <li>{{ $t('predictions_home.model_cards.xai.visualization') }}</li>
                  </ul>
                </div>

              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

    </v-sheet>
  </v-container>
</template>

<script setup lang="ts">
import {onMounted, ref, watch} from 'vue'
import {API_BASE} from '@/lib/api'
import {useTranslation} from 'i18next-vue'

const {i18next} = useTranslation()

interface ModelMetrics {
  accuracy?: number
  precision?: number
  recall?: number
  f1_score?: number
  roc_auc?: number
}

interface ModelCardData {
  name: string
  version: string
  modelType: string
  lastUpdated: string
  intendedUse: string[]
  notIntendedFor: string[]
  limitations: string[]
  recommendations: string[]
  metrics?: ModelMetrics
  featureGroups: Record<string, string[]>
}

const loading = ref(true)
const error = ref('')
const modelCardData = ref<ModelCardData>({
  name: 'HEAR CI Prediction Model',
  version: 'v1.0',
  modelType: 'RandomForestClassifier',
  lastUpdated: '2026-02-17',
  intendedUse: [],
  notIntendedFor: [],
  limitations: [],
  recommendations: [],
  featureGroups: {}
})

function parseModelCardMarkdown(markdown: string): ModelCardData {
  const data: ModelCardData = {
    name: 'HEAR CI Prediction Model',
    version: 'v1.0',
    modelType: 'RandomForestClassifier',
    lastUpdated: '2026-02-17',
    intendedUse: [],
    notIntendedFor: [],
    limitations: [],
    recommendations: [],
    featureGroups: {}
  }

  console.log('Parsing model card markdown...')

  // Parse title
  const titleMatch = markdown.match(/^#\s+(.+)$/m)
  if (titleMatch) data.name = titleMatch[1]

  // Parse metadata
  const versionMatch = markdown.match(/\*\*Version:\*\*\s+(.+?)(?:\s|\n)/i)
  if (versionMatch) data.version = versionMatch[1]

  const typeMatch = markdown.match(/\*\*(?:Modelltyp|Model Type):\*\*\s+(.+?)(?:\s|\n)/i)
  if (typeMatch) data.modelType = typeMatch[1]

  const dateMatch = markdown.match(/\*\*(?:Letzte Aktualisierung|Last Updated):\*\*\s+(.+?)(?:\s|\n)/i)
  if (dateMatch) data.lastUpdated = dateMatch[1]

  // Parse metrics
  const metricsMatch = markdown.match(/\*\*Accuracy:\*\*\s+([\d.]+)%[\s\S]*?\*\*ROC-AUC:\*\*\s+([\d.]+)[\s\S]*?\*\*(?:Sensitivität|Sensitivity).*?:\*\*\s+([\d.]+)%[\s\S]*?\*\*(?:Spezifität|Specificity).*?:\*\*\s+([\d.]+)%[\s\S]*?\*\*F1-Score:\*\*\s+([\d.]+)/i)
  if (metricsMatch) {
    data.metrics = {
      accuracy: parseFloat(metricsMatch[1]) / 100,
      roc_auc: parseFloat(metricsMatch[2]),
      recall: parseFloat(metricsMatch[3]) / 100,
      precision: parseFloat(metricsMatch[4]) / 100,
      f1_score: parseFloat(metricsMatch[5])
    }
    console.log('Parsed metrics:', data.metrics)
  }

  // Parse feature groups - improved regex
  const featureSection = markdown.match(/## (?:📋\s*)?Features[\s\S]*?(?=\n---\n|$)/i)
  if (featureSection) {
    console.log('Found feature section')
    const sectionText = featureSection[0]
    
    // Match all ### headers and their content until next ### or ---
    const lines = sectionText.split('\n')
    let currentGroup = ''
    let currentFeatures: string[] = []
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      
      // Check for group header (### ...)
      if (line.startsWith('###')) {
        // Save previous group if exists
        if (currentGroup && currentFeatures.length > 0) {
          data.featureGroups[currentGroup] = [...currentFeatures]
          console.log(`Added group "${currentGroup}" with ${currentFeatures.length} features`)
        }
        // Start new group
        currentGroup = line.replace(/^###\s+/, '').trim()
        currentFeatures = []
      }
      // Check for numbered feature (1. ...)
      else if (/^\d+\.\s+/.test(line)) {
        const feature = line.replace(/^\d+\.\s+/, '').trim()
        if (feature && !feature.startsWith('...')) {
          currentFeatures.push(feature)
        }
      }
    }
    
    // Add last group
    if (currentGroup && currentFeatures.length > 0) {
      data.featureGroups[currentGroup] = [...currentFeatures]
      console.log(`Added final group "${currentGroup}" with ${currentFeatures.length} features`)
    }
    
    console.log('Total feature groups:', Object.keys(data.featureGroups).length)
  } else {
    console.log('No feature section found')
  }

  return data
}

async function loadModelCard() {
  loading.value = true
  error.value = ''
  
  try {
    const currentLang = i18next.language || 'de'
    const response = await fetch(`${API_BASE}/api/v1/model-card?lang=${currentLang}`)
    if (response.ok) {
      const markdownText = await response.text()
      modelCardData.value = parseModelCardMarkdown(markdownText)
    } else {
      error.value = `Failed to load model card (HTTP ${response.status})`
    }
  } catch (err) {
    console.error('Error fetching model card:', err)
    error.value = 'Error loading model card. Please check your connection.'
  } finally {
    loading.value = false
  }
}

// Watch for language changes and reload model card
watch(() => i18next.language, () => {
  loadModelCard()
})

onMounted(() => {
  loadModelCard()
})
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

/* Remove connector line after final step */
.v-timeline-item:last-child .v-timeline-item__body::before {
  display: none !important;
}

/* Professional Model Card Styles */
.model-card-professional {
  border-radius: 8px !important;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.model-card-header {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-primary-darken-1)) 100%);
  border-bottom: none !important;
}

.model-card-metadata {
  border-bottom: 1px solid #e0e0e0;
}

.model-card-sections {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.model-card-section {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.87);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgb(var(--v-theme-primary));
  display: inline-block;
}

.section-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.section-list li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.7);
}

.section-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: rgb(var(--v-theme-primary));
  font-weight: bold;
  font-size: 1.2rem;
}

/* Metrics Grid */
.metric-item {
  background-color: white;
  border-radius: 6px;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  text-align: center;
}

.metric-label {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgb(var(--v-theme-primary));
}

/* Feature Groups */
.feature-group-title {
  font-weight: 500 !important;
  color: rgba(0, 0, 0, 0.87) !important;
}

.feature-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem 0;
}

/* Expansion Panels Custom Styling */
:deep(.v-expansion-panel) {
  background-color: white !important;
  border: 1px solid #e0e0e0 !important;
  margin-bottom: 0.5rem !important;
  border-radius: 6px !important;
}

:deep(.v-expansion-panel-title) {
  padding: 1rem !important;
  font-weight: 500;
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 1rem !important;
}

/* Chips */
:deep(.v-chip) {
  border-color: rgb(var(--v-theme-primary)) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .model-card-section {
    padding: 1rem;
  }
  
  .metric-item {
    margin-bottom: 0.5rem;
  }
  
  .section-title {
    font-size: 1rem;
  }
}
</style>