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
            size="small"
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

      <v-divider
          class="my-6"
      />

      <!-- Patient details cards -->
      <v-row class="details-grid" dense>
        <!-- Demographics -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.demographics') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.name') }}</span>
                <span class="detail-value">{{ displayName }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.age') }}</span>
                <span class="detail-value">{{ age || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.gender') }}</span>
                <span class="detail-value">{{ gender || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.operated_side') }}</span>
                <span class="detail-value">{{ operated_side || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Language & Communication -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.language') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.primary_language') }}</span>
                <span class="detail-value">{{ primary_language || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.other_languages') }}</span>
                <span class="detail-value">{{ other_languages || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.german_language_barrier') }}</span>
                <span class="detail-value">{{ german_language_barrier || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.non_verbal') }}</span>
                <span class="detail-value">{{ non_verbal || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Family history -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.family_history') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.parent_hearing_loss') }}</span>
                <span class="detail-value">{{ parent_hearing_loss || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.sibling_hearing_loss') }}</span>
                <span class="detail-value">{{ sibling_hearing_loss || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Pre-operative symptoms -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.preop_symptoms') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.tinnitus_preop') }}</span>
                <span class="detail-value">{{ tinnitus_preop || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.vertigo_preop') }}</span>
                <span class="detail-value">{{ vertigo_preop || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.otorrhea_preop') }}</span>
                <span class="detail-value">{{ otorrhea_preop || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.headache_preop') }}</span>
                <span class="detail-value">{{ headache_preop || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.taste_preop') }}</span>
                <span class="detail-value">{{ taste_preop || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Hearing status -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.hearing_status') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.hl_operated_ear') }}</span>
                <span class="detail-value">{{ hl_operated_ear || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.hl_contra_ear') }}</span>
                <span class="detail-value">{{ hl_contra_ear || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.hearing_loss_onset') }}</span>
                <span class="detail-value">{{ hearing_loss_onset || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.hearing_loss_start') }}</span>
                <span class="detail-value">{{ hearing_loss_start || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.duration_severe_hl') }}</span>
                <span class="detail-value">{{ duration_severe_hl || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.etiology') }}</span>
                <span class="detail-value">{{ etiology || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Treatment & Outcome -->
        <v-col cols="12" md="6" lg="4" class="detail-col">
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ $t('patient_details.sections.treatment_outcome') }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.ci_implant_type') }}</span>
                <span class="detail-value">{{ ci_implant_type || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.pre_measure') }}</span>
                <span class="detail-value">{{ pre_measure || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.post12_measure') }}</span>
                <span class="detail-value">{{ post12_measure || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.post24_measure') }}</span>
                <span class="detail-value">{{ post24_measure || "—" }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">{{ $t('patient_details.fields.interval_days') }}</span>
                <span class="detail-value">{{ interval_days || "—" }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>



      <v-divider
          class="my-6"
      />

      <!-- Actions -->
      <div class="d-flex justify-space-between align-center mb-4">
        <v-row class="ms-4">

          <!-- TODO: redirect to create patient form but with the values filled out -->
          <v-btn
              class="me-4"
              color="warning"
              variant="flat"
          >
            {{ $t('patient_details.change_patient') }}
          </v-btn>

          <!-- TODO: implement patient deletion if needed for MVP -->
          <v-btn
              class="me-4"
              color="error"
              variant="flat"
          >
            {{ $t('patient_details.delete_patient') }}
          </v-btn>
        </v-row>
        <v-btn
            class="me-4"
            color="success"
            variant="flat"
            :to="{ name: 'Prediction', params: {patient_id: patient_id}}"
        >
          {{ $t('patient_details.generate_prediction') }}
        </v-btn>

      </div>
    </v-sheet>
  </v-container>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {API_BASE} from "@/lib/api";

const route = useRoute();

const rawId = route.params.id;
const patient_id = ref<string>(Array.isArray(rawId) ? rawId[0] : rawId ?? "");
const patient = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const displayName = computed(() => patient.value?.name ?? patient.value?.display_name ?? "Patient");

// Demographics
const age = ref("");
const gender = ref("");
const operated_side = ref("");

// Language / Communication
const primary_language = ref("");
const other_languages = ref("");
const german_language_barrier = ref("");
const non_verbal = ref("");

// Family history
const parent_hearing_loss = ref("");
const sibling_hearing_loss = ref("");

// Pre-operative symptoms
const taste_preop = ref("");
const tinnitus_preop = ref("");
const vertigo_preop = ref("");
const otorrhea_preop = ref("");
const headache_preop = ref("");

// Imaging
const imaging_type_preop = ref("");
const imaging_findings_preop = ref("");

// Objective measurements
const oae_status = ref("");
const ll_status = ref("");
const hz4k_status = ref("");

// Hearing loss – operated ear
const hl_operated_ear = ref("");
const amplification_operated_ear = ref("");
const hearing_loss_onset = ref("");
const acquisition_type = ref("");
const hearing_loss_start = ref("");
const duration_severe_hl = ref("");
const etiology = ref("");
const hearing_disorder_type = ref("");

// Hearing loss – contralateral ear
const hl_contra_ear = ref("");
const amplification_contra_ear = ref("");

// Treatment
const ci_implant_type = ref("");

// Outcome
const pre_measure = ref("");
const post12_measure = ref("");
const post24_measure = ref("");
const interval_days = ref("");


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

    // assign values

    // Demographics
    age.value = patient.value.input_features["Alter [J]"];
    gender.value = patient.value.input_features["Geschlecht"];
    operated_side.value = patient.value.input_features["Seiten"];

    // Language / communication
    primary_language.value = patient.value.input_features["Primäre Sprache"];
    other_languages.value = patient.value.input_features["Weitere Sprachen"];
    german_language_barrier.value = patient.value.input_features["Deutsch Sprachbarriere"];
    non_verbal.value = patient.value.input_features["non-verbal"];

    // Family history
    parent_hearing_loss.value = patient.value.input_features["Eltern m. Schwerhörigkeit"];
    sibling_hearing_loss.value = patient.value.input_features["Geschwister m. SH"];

    // Pre-operative symptoms
    taste_preop.value = patient.value.input_features["Symptome präoperativ.Geschmack..."];
    tinnitus_preop.value = patient.value.input_features["Symptome präoperativ.Tinnitus..."];
    vertigo_preop.value = patient.value.input_features["Symptome präoperativ.Schwindel..."];
    otorrhea_preop.value = patient.value.input_features["Symptome präoperativ.Otorrhoe..."];
    headache_preop.value = patient.value.input_features["Symptome präoperativ.Kopfschmerzen..."];

    // Imaging
    imaging_type_preop.value = patient.value.input_features["Bildgebung, präoperativ.Typ..."];
    imaging_findings_preop.value = patient.value.input_features["Bildgebung, präoperativ.Befunde..."];

    // Objective measurements
    oae_status.value = patient.value.input_features["Objektive Messungen.OAE (TEOAE/DPOAE)..."];
    ll_status.value = patient.value.input_features["Objektive Messungen.LL..."];
    hz4k_status.value = patient.value.input_features["Objektive Messungen.4000 Hz..."];

    // Hearing loss – operated ear
    hl_operated_ear.value = patient.value.input_features["Diagnose.Höranamnese.Hörminderung operiertes Ohr..."];
    amplification_operated_ear.value = patient.value.input_features["Diagnose.Höranamnese.Versorgung operiertes Ohr..."];
    hearing_loss_onset.value = patient.value.input_features["Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)..."];
    acquisition_type.value = patient.value.input_features["Diagnose.Höranamnese.Erwerbsart..."];
    hearing_loss_start.value = patient.value.input_features["Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..."];
    duration_severe_hl.value = patient.value.input_features["Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)..."];
    etiology.value = patient.value.input_features["Diagnose.Höranamnese.Ursache....Ursache..."];
    hearing_disorder_type.value = patient.value.input_features["Diagnose.Höranamnese.Art der Hörstörung..."];

    // Contralateral ear
    hl_contra_ear.value = patient.value.input_features["Diagnose.Höranamnese.Hörminderung Gegenohr..."];
    amplification_contra_ear.value = patient.value.input_features["Diagnose.Höranamnese.Versorgung Gegenohr..."];

    // Treatment
    ci_implant_type.value = patient.value.input_features["Behandlung/OP.CI Implantation"];

    // Outcome
    pre_measure.value = patient.value.input_features["outcome_measurments.pre.measure."];
    post12_measure.value = patient.value.input_features["outcome_measurments.post12.measure."];
    post24_measure.value = patient.value.input_features["outcome_measurments.post24.measure."];
    interval_days.value = patient.value.input_features["abstand"];


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

/* stack cards vertically and center them a bit */
.details-grid {
  margin-top: 8px;
  row-gap: 12px;
}

.detail-col {
  margin-bottom: 12px;
}

@media (min-width: 1280px) {
  .details-grid {
    row-gap: 8px;
  }

  .detail-col {
    margin-bottom: 6px;
  }
}

/* one “Personal details” style card */
.detail-card {
  height: 100%;
  border-radius: 16px;
  padding: 12px 16px 16px;
  box-shadow: none;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background-color: rgb(var(--v-theme-surface));
}

/* header text */
.detail-card__header {
  font-weight: 600;
  font-size: 1rem;
  padding: 4px 0 8px;
}

/* body */
.detail-card__body {
  margin-top: 4px;
  padding: 0;
}

/* rows inside the card */
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-top: 1px dashed rgba(148, 163, 184, 0.6);
  column-gap: 16px;
}

.detail-label {
  font-size: 0.88rem;
  color: #6b7280;
}

.detail-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #111827;
  text-align: right;
  max-width: 55%;
  word-break: break-word;
}

@media (max-width: 600px) {
  .detail-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-value {
    text-align: left;
    max-width: 100%;
  }
}
</style>
