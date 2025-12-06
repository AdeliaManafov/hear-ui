<template>
  <div class="prediction-result">
    <div class="prediction-score">
      <div class="score-label">Erfolgswahrscheinlichkeit</div>
      <div class="score-value" :class="scoreClass">
        {{ (result.prediction * 100).toFixed(1) }}%
      </div>
      <div class="score-bar">
        <div 
          class="score-fill" 
          :class="scoreClass"
          :style="{ width: `${result.prediction * 100}%` }"
        ></div>
      </div>
      <div class="score-interpretation">
        <span class="interpretation-text">{{ interpretationText }}</span>
      </div>
    </div>

    <div class="prediction-details">
      <h3>Interpretation</h3>
      <p v-if="result.prediction >= 0.7" class="detail-text success">
        <strong>Hohe Erfolgswahrscheinlichkeit:</strong> 
        Die KI-Analyse deutet auf eine hohe Wahrscheinlichkeit hin, dass der Patient 
        von einem Cochlea-Implantat profitieren würde. Eine weitere medizinische 
        Bewertung wird empfohlen.
      </p>
      <p v-else-if="result.prediction >= 0.4" class="detail-text warning">
        <strong>Moderate Erfolgswahrscheinlichkeit:</strong> 
        Die KI-Analyse zeigt gemischte Indikatoren. Eine detaillierte medizinische 
        Untersuchung und Beratung sind erforderlich, um eine fundierte Entscheidung 
        zu treffen.
      </p>
      <p v-else class="detail-text danger">
        <strong>Niedrige Erfolgswahrscheinlichkeit:</strong> 
        Die KI-Analyse deutet auf eine geringere Wahrscheinlichkeit eines erfolgreichen 
        Outcomes hin. Alternative Behandlungsoptionen sollten in Betracht gezogen werden.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  result: {
    prediction: number
    explanation: Record<string, number>
  }
}

const props = defineProps<Props>()

const scoreClass = computed(() => {
  if (props.result.prediction >= 0.7) return 'high'
  if (props.result.prediction >= 0.4) return 'medium'
  return 'low'
})

const interpretationText = computed(() => {
  if (props.result.prediction >= 0.7) return 'Hohe Erfolgsaussicht'
  if (props.result.prediction >= 0.4) return 'Moderate Erfolgsaussicht'
  return 'Niedrige Erfolgsaussicht'
})
</script>

<style scoped>
.prediction-result {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.prediction-score {
  text-align: center;
}

.score-label {
  font-size: 1.1rem;
  color: #6b7280;
  margin-bottom: 1rem;
  font-weight: 500;
}

.score-value {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  animation: countUp 0.8s ease-out;
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.score-value.high {
  color: #10b981;
}

.score-value.medium {
  color: #f59e0b;
}

.score-value.low {
  color: #ef4444;
}

.score-bar {
  width: 100%;
  height: 30px;
  background: #e5e7eb;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.score-fill {
  height: 100%;
  transition: width 1s ease-out;
  border-radius: 15px;
  position: relative;
  overflow: hidden;
}

.score-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.score-fill.high {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.score-fill.medium {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.score-fill.low {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.score-interpretation {
  margin-top: 0.5rem;
}

.interpretation-text {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1rem;
}

.score-value.high + .score-bar + .score-interpretation .interpretation-text {
  background: #d1fae5;
  color: #065f46;
}

.score-value.medium + .score-bar + .score-interpretation .interpretation-text {
  background: #fef3c7;
  color: #92400e;
}

.score-value.low + .score-bar + .score-interpretation .interpretation-text {
  background: #fee2e2;
  color: #991b1b;
}

.prediction-details {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.prediction-details h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.detail-text {
  margin: 0;
  line-height: 1.6;
  color: #4b5563;
}

.detail-text strong {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1.05rem;
}

.detail-text.success strong {
  color: #059669;
}

.detail-text.warning strong {
  color: #d97706;
}

.detail-text.danger strong {
  color: #dc2626;
}

@media (max-width: 768px) {
  .score-value {
    font-size: 3rem;
  }
  
  .prediction-details {
    padding: 1rem;
  }
}
</style>
