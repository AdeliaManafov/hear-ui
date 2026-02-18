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
          <h2>{{ $t('predictions_home.model_cards.title') }}</h2>
          <v-card
            class="mt-4"
            variant="outlined"
            elevation="2"
          >
            <v-card-text>
              <div class="markdown-content pa-4" v-html="modelCardHtml"></div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>


    </v-sheet>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import MarkdownIt from 'markdown-it'

// Reaktive Variable für gerendertes HTML
const modelCardHtml = ref('')

// MarkdownIt mit HTML-Rendering aktivieren
const md = new MarkdownIt({ html: true })

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/model-card/markdown')

    if (response.ok) {
      const data = await response.json()
      // Markdown in HTML rendern (inklusive <div> Blöcke)
      modelCardHtml.value = md.render(data.markdown)
    } else {
      modelCardHtml.value = '<p>Could not load model card.</p>'
    }

  } catch (error) {
    console.error('Error fetching model card:', error)
    modelCardHtml.value = '<p>Error loading model card.</p>'
  }
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

/* Metadata Styling */
.markdown-content :deep(.metadata) {
  background: rgba(var(--v-theme-surface-variant), 0.1);
  padding: 1em;
  border-radius: 8px;
  margin-bottom: 2em;
  font-family: monospace;
}

/* Überschriften */
.markdown-content :deep(h1) {
  color: rgb(var(--v-theme-primary));
  font-size: 2em;
  margin-bottom: 0.5em;
  padding-bottom: 0.3em;
  border-bottom: 2px solid rgb(var(--v-theme-primary));
}

.markdown-content :deep(h2) {
  color: rgb(var(--v-theme-secondary));
  font-size: 1.5em;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  padding: 0.5em;
  background: rgba(var(--v-theme-surface-variant), 0.1);
  border-radius: 4px;
}

.markdown-content :deep(h3) {
  color: rgb(var(--v-theme-primary));
  font-size: 1.2em;
  margin-top: 1.2em;
  margin-bottom: 0.5em;
  padding-bottom: 0.2em;
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.2);
}

/* Listen */
.markdown-content :deep(ul) {
  padding-left: 0;
  margin: 1em 0;
  list-style: none;
}

.markdown-content :deep(li) {
  margin: 0.5em 0;
  padding: 0.5em;
  background: rgba(var(--v-theme-surface-variant), 0.05);
  border-radius: 4px;
  transition: all 0.2s ease;
}

.markdown-content :deep(li:hover) {
  background: rgba(var(--v-theme-surface-variant), 0.1);
  transform: translateX(4px);
}

/* Feature Gruppen */
.markdown-content :deep(h3 + ul) {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 0.8em;
  padding: 1em;
  background: rgba(var(--v-theme-surface-variant), 0.05);
  border-radius: 8px;
  margin-bottom: 1.5em;
}

/* Trennlinien */
.markdown-content :deep(hr) {
  border: none;
  height: 1px;
  background: rgba(var(--v-theme-on-surface), 0.1);
  margin: 2em 0;
}

/* Listen-Items in Feature-Gruppen */
.markdown-content :deep(h3 + ul li) {
  background: white;
  padding: 0.8em;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 4px;
  font-size: 0.9em;
  line-height: 1.4;
  transition: all 0.2s ease;
}

.markdown-content :deep(h3 + ul li:hover) {
  border-color: rgb(var(--v-theme-primary));
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Entfernen der Timeline-Linie nach dem letzten Element */
.v-timeline-item:last-child .v-timeline-item__body::before {
  display: none !important;
}
</style>


