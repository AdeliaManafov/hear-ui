<template>
  <div id="app" class="app-container">
    <header class="app-header">
      <div class="header-content">
        <h1>
          <span class="icon">🦻</span>
          HEAR UI
        </h1>
        <p class="subtitle">Cochlea-Implantat Entscheidungsunterstützung</p>
      </div>
    </header>

    <main class="main-content">
      <div class="content-wrapper">
        <!-- Patient Input Form -->
        <section class="card">
          <h2>Patientendaten eingeben</h2>
          <PatientForm @predict="handlePredict" :loading="loading" />
        </section>

        <!-- Prediction Result -->
        <section v-if="predictionResult" class="card result-card">
          <h2>Vorhersage-Ergebnis</h2>
          <PredictionResult :result="predictionResult" />
        </section>

        <!-- SHAP Explanation -->
        <section v-if="predictionResult" class="card">
          <h2>KI-Erklärung (SHAP Feature Importance)</h2>
          <ShapExplanation :explanation="predictionResult.explanation" />
        </section>

        <!-- Feedback Form -->
        <section v-if="predictionResult" class="card">
          <h2>Feedback geben</h2>
          <FeedbackForm
            :prediction-data="predictionResult"
            :patient-data="currentPatientData"
            @feedback-submitted="handleFeedbackSubmitted"
          />
        </section>

        <!-- Success Message -->
        <div v-if="feedbackSuccess" class="success-message">
          <span class="icon">✓</span>
          Vielen Dank für Ihr Feedback! Es wurde erfolgreich gespeichert.
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <p>
        HEAR Projekt &copy; 2025 | 
        <a href="http://localhost:8000/docs" target="_blank">API Dokumentation</a>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PatientForm from './components/PatientForm.vue'
import PredictionResult from './components/PredictionResult.vue'
import ShapExplanation from './components/ShapExplanation.vue'
import FeedbackForm from './components/FeedbackForm.vue'

interface PatientData {
  age: number
  hearing_loss_duration: number
  implant_type: string
}

interface PredictionResponse {
  prediction: number
  explanation: Record<string, number>
}

const loading = ref(false)
const predictionResult = ref<PredictionResponse | null>(null)
const currentPatientData = ref<PatientData | null>(null)
const feedbackSuccess = ref(false)

const handlePredict = async (patientData: PatientData) => {
  loading.value = true
  feedbackSuccess.value = false
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/predict/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    })

    if (!response.ok) {
      throw new Error('Prediction request failed')
    }

    const data = await response.json()
    predictionResult.value = data
    currentPatientData.value = patientData
  } catch (error) {
    console.error('Error making prediction:', error)
    alert('Fehler bei der Vorhersage. Bitte versuchen Sie es erneut.')
  } finally {
    loading.value = false
  }
}

const handleFeedbackSubmitted = () => {
  feedbackSuccess.value = true
  setTimeout(() => {
    feedbackSuccess.value = false
  }, 5000)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem 1rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.app-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.app-header h1 .icon {
  font-size: 2.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0.5rem 0 0 0;
}

.main-content {
  flex: 1;
  padding: 2rem 1rem;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}

.card h2 {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  border-bottom: 3px solid #667eea;
  padding-bottom: 0.5rem;
}

.result-card {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border: 2px solid #667eea;
}

.success-message {
  background: #10b981;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-message .icon {
  font-size: 1.5rem;
  font-weight: bold;
}

.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1.5rem 1rem;
  text-align: center;
  color: #666;
  box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
}

.app-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.app-footer a:hover {
  color: #764ba2;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2rem;
  }
  
  .card {
    padding: 1.5rem;
  }
}
</style>
