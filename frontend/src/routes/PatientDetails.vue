<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="patient-sheet"
        rounded="lg"
    >
      <v-row justify="start" no-gutters>
        <v-btn
            :to="{ name: 'SearchPatients' }"
            color="primary"
            prepend-icon="mdi-arrow-left"
            variant="tonal"
        >
          {{ $t('patient_details.back') }}
        </v-btn>
      </v-row>
      <v-divider
          class="my-6"
      />

      <!-- Title -->
      <v-row justify="start" no-gutters>
        <h1>
          {{ $t('patient_details.title') }}
          <span class="text-primary">{{ displayName }}</span>
        </h1>

      </v-row>
      <v-row v-if="loading" class="my-2" no-gutters>
        <span>{{ $t('common.loading') || 'Loading...' }}</span>
      </v-row>
      <v-row v-else-if="error" class="my-2 text-error" no-gutters>
        <span>{{ error }}</span>
      </v-row>
      <v-divider
          class="my-6"
      />

      <!-- TODO: upload the form -->

      <!-- TODO: add action for change and delete -->

      <v-divider
          class="my-6"
      />

      <!-- Actions -->
      <div class="d-flex justify-space-between align-center mb-4">
        <v-row>


          <v-btn
              class="me-4"
              color="success"
              variant="flat"
              :to="{ name: 'Prediction', params: { patient_id: patient_id, patient_name: displayName }}"
          >
            {{ $t('patient_details.generate_prediction') }}
          </v-btn>

          <v-btn
              class="me-4"
              color="warning"
              variant="flat"
          >
            {{ $t('patient_details.change_patient') }}
          </v-btn>
        </v-row>
        <!-- TODO: implement patient deletion if needed for MVP -->
        <v-btn
            class="me-4"
            color="error"
            variant="flat"
        >
          {{ $t('patient_details.delete_patient') }}
        </v-btn>

      </div>
    </v-sheet>
  </v-container>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const route = useRoute();

const rawId = route.params.id;
const patient_id = ref<string>(Array.isArray(rawId) ? rawId[0] : rawId ?? "");
const patient = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const displayName = computed(() => patient.value?.name ?? patient.value?.display_name ?? "Patient");

onMounted(async () => {
  if (!patient_id.value) {
    error.value = "No patient id provided in route params";
    loading.value = false;
    return;
  }

  try {
    const response = await fetch(
        `${API_BASE}/api/v1/patients/${encodeURIComponent(patient_id.value)}`,
        {
          method: "GET",
          headers: {
            accept: "application/json",
          },
        }
    );

    if (!response.ok) throw new Error("Network error");

    patient.value = await response.json();
  } catch (err: any) {
    console.error(err);
    error.value = err?.message ?? "Failed to load patient";
  } finally {
    loading.value = false;
  }
});

</script>

<style scoped>
.patient-sheet {
  padding: 32px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}
</style>
