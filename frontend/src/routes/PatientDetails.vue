<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="patient-sheet"
        rounded="lg"
    >
      <!-- Title -->
      <v-row justify="start" no-gutters>
        <h1>
          {{$t('patient_details.title')}}
          <span class="text-primary">{{ patient.name }}</span>
        </h1>

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
        <v-btn
            :to="{ name: 'SearchPatients' }"
            color="primary"
            prepend-icon="mdi-arrow-left"
            variant="tonal"
        >
          {{ $t('patient_details.back') }}
        </v-btn>

        <v-btn
            class="me-4"
            color="primary"
            variant="flat"
            :to="{ name: 'Prediction', params: { patient_id: patient_id, patient_name: patient.name }}"
        >
          generate prediction
        </v-btn>
      </div>
    </v-sheet>
  </v-container>
</template>

<script lang="ts" setup>
import {useRoute} from 'vue-router'

const route = useRoute()

// Get the id from the URL
const patient_id = route.params.id

// TODO: implement an API call for that
const patient = {
  name: 'John Doe',
}
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