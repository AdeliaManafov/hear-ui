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
          <v-card class="mt-4" variant="outlined">
            <div class="markdown-content pa-4" v-html="modelCardHtml"></div>
          </v-card>
        </v-col>
      </v-row>

    </v-sheet>
  </v-container>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import MarkdownIt from 'markdown-it'

const modelCardHtml = ref('')
const md = new MarkdownIt()

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/model-card')
    if (response.ok) {
      const markdownText = await response.text()
      modelCardHtml.value = md.render(markdownText)
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

/* Remove connector line after final step */
.v-timeline-item:last-child .v-timeline-item__body::before {
  display: none !important;
}


.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.markdown-content :deep(ul) {
  padding-left: 2em;
}

.markdown-content :deep(code) {
  background-color: rgba(var(--v-theme-on-surface), 0.1);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}
</style>