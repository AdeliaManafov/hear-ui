<template>
  <form @submit.prevent="submitForm" class="patient-form">
    <div class="form-group">
      <label for="age">
        Alter (Jahre)
        <span class="required">*</span>
      </label>
      <input
        id="age"
        v-model.number="formData.age"
        type="number"
        min="0"
        max="120"
        required
        :disabled="loading"
        placeholder="z.B. 65"
      />
      <small class="hint">Alter des Patienten in Jahren</small>
    </div>

    <div class="form-group">
      <label for="duration">
        Hörverlust-Dauer (Jahre)
        <span class="required">*</span>
      </label>
      <input
        id="duration"
        v-model.number="formData.hearing_loss_duration"
        type="number"
        min="0"
        step="0.1"
        required
        :disabled="loading"
        placeholder="z.B. 5.5"
      />
      <small class="hint">Dauer des Hörverlusts in Jahren</small>
    </div>

    <div class="form-group">
      <label for="implant-type">
        Implantat-Typ
        <span class="required">*</span>
      </label>
      <select
        id="implant-type"
        v-model="formData.implant_type"
        required
        :disabled="loading"
      >
        <option value="" disabled>Bitte wählen...</option>
        <option value="type_a">Typ A - Standard</option>
        <option value="type_b">Typ B - Advanced</option>
        <option value="type_c">Typ C - Premium</option>
      </select>
      <small class="hint">Art des geplanten Cochlea-Implantats</small>
    </div>

    <button type="submit" class="submit-btn" :disabled="loading">
      <span v-if="!loading">
        <span class="icon">🔍</span>
        Vorhersage berechnen
      </span>
      <span v-else class="loading-spinner">
        <span class="spinner"></span>
        Wird berechnet...
      </span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface PatientFormData {
  age: number | null
  hearing_loss_duration: number | null
  implant_type: string
}

interface Props {
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  predict: [data: { age: number; hearing_loss_duration: number; implant_type: string }]
}>()

const formData = ref<PatientFormData>({
  age: null,
  hearing_loss_duration: null,
  implant_type: ''
})

const submitForm = () => {
  if (formData.value.age !== null && 
      formData.value.hearing_loss_duration !== null && 
      formData.value.implant_type) {
    emit('predict', {
      age: formData.value.age,
      hearing_loss_duration: formData.value.hearing_loss_duration,
      implant_type: formData.value.implant_type
    })
  }
}
</script>

<style scoped>
.patient-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.required {
  color: #ef4444;
  margin-left: 0.25rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled,
.form-group select:disabled {
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
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
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

@media (max-width: 768px) {
  .submit-btn {
    font-size: 1rem;
    padding: 0.875rem 1.5rem;
  }
}
</style>
