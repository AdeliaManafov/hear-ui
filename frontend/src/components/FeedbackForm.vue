<template>
  <form @submit.prevent="submitFeedback" class="feedback-form">
    <div class="feedback-question">
      <p class="question-text">
        Stimmen Sie der KI-Vorhersage zu?
      </p>
      <div class="feedback-buttons">
        <button
          type="button"
          class="feedback-btn agree"
          :class="{ active: formData.accepted === true }"
          @click="formData.accepted = true"
        >
          <span class="icon">👍</span>
          Stimme zu
        </button>
        <button
          type="button"
          class="feedback-btn disagree"
          :class="{ active: formData.accepted === false }"
          @click="formData.accepted = false"
        >
          <span class="icon">👎</span>
          Stimme nicht zu
        </button>
      </div>
    </div>

    <div class="form-group">
      <label for="comment">
        Kommentar (optional)
      </label>
      <textarea
        id="comment"
        v-model="formData.comment"
        rows="4"
        placeholder="Teilen Sie Ihre Gedanken oder zusätzliche Informationen..."
        :disabled="submitting"
      ></textarea>
      <small class="hint">
        Ihr Feedback hilft uns, das KI-Modell zu verbessern
      </small>
    </div>

    <div class="form-group">
      <label for="email">
        E-Mail (optional)
      </label>
      <input
        id="email"
        v-model="formData.user_email"
        type="email"
        placeholder="ihre.email@beispiel.de"
        :disabled="submitting"
      />
      <small class="hint">
        Für Rückfragen zu Ihrem Feedback
      </small>
    </div>

    <button
      type="submit"
      class="submit-btn"
      :disabled="formData.accepted === null || submitting"
    >
      <span v-if="!submitting">
        <span class="icon">📤</span>
        Feedback absenden
      </span>
      <span v-else class="loading-spinner">
        <span class="spinner"></span>
        Wird gesendet...
      </span>
    </button>

    <p v-if="error" class="error-message">
      {{ error }}
    </p>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface Props {
  predictionData: {
    prediction: number
    explanation: Record<string, number>
  }
  patientData: {
    age: number
    hearing_loss_duration: number
    implant_type: string
  }
}

const props = defineProps<Props>()
const emit = defineEmits<{
  feedbackSubmitted: []
}>()

const formData = reactive({
  accepted: null as boolean | null,
  comment: '',
  user_email: ''
})

const submitting = ref(false)
const error = ref('')

const submitFeedback = async () => {
  if (formData.accepted === null) {
    error.value = 'Bitte wählen Sie, ob Sie der Vorhersage zustimmen oder nicht.'
    return
  }

  submitting.value = true
  error.value = ''

  try {
    const feedbackPayload = {
      input_features: props.patientData,
      prediction: props.predictionData.prediction,
      explanation: props.predictionData.explanation,
      accepted: formData.accepted,
      comment: formData.comment || null,
      user_email: formData.user_email || null
    }

    const response = await fetch('http://localhost:8000/api/v1/feedback/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedbackPayload),
    })

    if (!response.ok) {
      throw new Error('Feedback submission failed')
    }

    // Reset form
    formData.accepted = null
    formData.comment = ''
    formData.user_email = ''

    emit('feedbackSubmitted')
  } catch (err) {
    console.error('Error submitting feedback:', err)
    error.value = 'Fehler beim Absenden des Feedbacks. Bitte versuchen Sie es erneut.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.feedback-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feedback-question {
  background: #f0f9ff;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.question-text {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e40af;
}

.feedback-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.feedback-btn {
  padding: 1rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.feedback-btn .icon {
  font-size: 1.5rem;
}

.feedback-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feedback-btn.agree.active {
  background: #d1fae5;
  border-color: #10b981;
  color: #065f46;
}

.feedback-btn.disagree.active {
  background: #fee2e2;
  border-color: #ef4444;
  color: #991b1b;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.form-group textarea,
.form-group input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: white;
}

.form-group textarea:focus,
.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea:disabled,
.form-group input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
  opacity: 0.6;
}

.hint {
  color: #6b7280;
  font-size: 0.875rem;
  font-style: italic;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn .icon {
  font-size: 1.2rem;
}

.loading-spinner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin: 0;
  border-left: 4px solid #ef4444;
}

@media (max-width: 768px) {
  .feedback-buttons {
    grid-template-columns: 1fr;
  }
  
  .submit-btn {
    font-size: 1rem;
    padding: 0.875rem 1.5rem;
  }
}
</style>
