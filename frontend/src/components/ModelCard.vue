
<template>
  <v-card>
    <v-card-title>Model Card: {{ modelCard.name }}</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item>
          <v-list-item-title>Version</v-list-item-title>
          <v-list-item-subtitle>{{ modelCard.version }}</v-list-item-subtitle>
        </v-list-item>
        <!-- Weitere Modellinformationen -->
      </v-list>

      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-title>Metriken</v-expansion-panel-title>
          <v-expansion-panel-text>
            <metrics-display :metrics="modelCard.metrics" />
          </v-expansion-panel-text>
        </v-expansion-panel>
        <!-- Weitere Panels für andere Kategorien -->
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { API_BASE } from '@/lib/api'

export default defineComponent({
  name: 'ModelCard',
  data() {
    return {
      modelCard: null
    }
  },
  async created() {
    // Lade Model Card Daten vom Backend
    const response = await fetch(`${API_BASE}/api/v1/model-card`)
    this.modelCard = await response.json()
  }
})
</script>
