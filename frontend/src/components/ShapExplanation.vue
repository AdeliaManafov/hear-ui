<template>
  <div class="shap-explanation">
    <p class="explanation-intro">
      Die folgenden Werte zeigen, wie stark jedes Merkmal die Vorhersage beeinflusst hat.
      Positive Werte erhöhen die Erfolgswahrscheinlichkeit, negative Werte verringern sie.
    </p>

    <div class="features-list">
      <div
        v-for="(value, feature) in sortedFeatures"
        :key="feature"
        class="feature-item"
      >
        <div class="feature-header">
          <span class="feature-name">{{ formatFeatureName(feature) }}</span>
          <span class="feature-value" :class="valueClass(value)">
            {{ value >= 0 ? '+' : '' }}{{ value.toFixed(3) }}
          </span>
        </div>
        <div class="feature-bar-container">
          <div class="feature-bar-center"></div>
          <div
            class="feature-bar"
            :class="valueClass(value)"
            :style="barStyle(value)"
          ></div>
        </div>
        <div class="feature-impact">
          {{ getImpactText(value) }}
        </div>
      </div>
    </div>

    <div class="chart-container">
      <h3>Visuelle Darstellung</h3>
      <div class="bar-chart">
        <div
          v-for="(value, feature) in sortedFeatures"
          :key="`chart-${feature}`"
          class="chart-bar-wrapper"
        >
          <div class="chart-label">{{ formatFeatureName(feature) }}</div>
          <div class="chart-bar-track">
            <div
              class="chart-bar"
              :class="valueClass(value)"
              :style="chartBarStyle(value)"
            >
              <span class="chart-value">{{ value.toFixed(3) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  explanation: Record<string, number>
}

const props = defineProps<Props>()

const sortedFeatures = computed(() => {
  const entries = Object.entries(props.explanation)
  entries.sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
  return Object.fromEntries(entries)
})

const maxAbsValue = computed(() => {
  const values = Object.values(props.explanation)
  return Math.max(...values.map(Math.abs), 0.01) // Avoid division by zero
})

const formatFeatureName = (feature: string): string => {
  const names: Record<string, string> = {
    age: 'Alter',
    hearing_loss_duration: 'Hörverlust-Dauer',
    implant_type: 'Implantat-Typ',
    other_feature: 'Weitere Faktoren'
  }
  return names[feature] || feature
}

const valueClass = (value: number): string => {
  if (value > 0.1) return 'positive'
  if (value < -0.1) return 'negative'
  return 'neutral'
}

const barStyle = (value: number) => {
  const absValue = Math.abs(value)
  const percentage = (absValue / maxAbsValue.value) * 50 // Max 50% to each side
  const direction = value >= 0 ? 'right' : 'left'
  
  return {
    width: `${percentage}%`,
    [direction]: '50%'
  }
}

const chartBarStyle = (value: number) => {
  const absValue = Math.abs(value)
  const percentage = (absValue / maxAbsValue.value) * 100
  
  return {
    width: `${percentage}%`
  }
}

const getImpactText = (value: number): string => {
  const absValue = Math.abs(value)
  if (absValue > 0.2) {
    return value > 0 ? 'Starker positiver Einfluss' : 'Starker negativer Einfluss'
  }
  if (absValue > 0.1) {
    return value > 0 ? 'Moderater positiver Einfluss' : 'Moderater negativer Einfluss'
  }
  return 'Geringer Einfluss'
}
</script>

<style scoped>
.shap-explanation {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.explanation-intro {
  background: #f0f9ff;
  border-left: 4px solid #3b82f6;
  padding: 1rem 1.5rem;
  margin: 0;
  border-radius: 4px;
  color: #1e40af;
  line-height: 1.6;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.feature-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.feature-value {
  font-weight: 700;
  font-size: 1.1rem;
  font-family: 'Courier New', monospace;
}

.feature-value.positive {
  color: #10b981;
}

.feature-value.negative {
  color: #ef4444;
}

.feature-value.neutral {
  color: #6b7280;
}

.feature-bar-container {
  position: relative;
  height: 24px;
  margin-bottom: 0.5rem;
}

.feature-bar-center {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #9ca3af;
  z-index: 1;
}

.feature-bar {
  position: absolute;
  top: 0;
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s ease-out;
  z-index: 2;
}

.feature-bar.positive {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.feature-bar.negative {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.feature-bar.neutral {
  background: linear-gradient(90deg, #9ca3af 0%, #6b7280 100%);
}

.feature-impact {
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
  text-align: center;
}

.chart-container {
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chart-bar-wrapper {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 1rem;
  align-items: center;
}

.chart-label {
  font-weight: 500;
  color: #4b5563;
  text-align: right;
  font-size: 0.9rem;
}

.chart-bar-track {
  background: #f3f4f6;
  border-radius: 4px;
  height: 32px;
  position: relative;
  overflow: hidden;
}

.chart-bar {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 0.5rem;
  transition: width 1s ease-out;
  border-radius: 4px;
}

.chart-value {
  color: white;
  font-weight: 600;
  font-size: 0.85rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .chart-bar-wrapper {
    grid-template-columns: 120px 1fr;
    gap: 0.5rem;
  }
  
  .chart-label {
    font-size: 0.8rem;
  }
  
  .chart-bar-track {
    height: 28px;
  }
}
</style>
