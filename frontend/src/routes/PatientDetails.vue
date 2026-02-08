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
        <v-col
          v-for="section in detailSections"
          :key="section.title"
          cols="12"
          md="6"
          class="detail-col"
        >
          <v-card class="detail-card" rounded="lg" elevation="0" variant="outlined">
            <v-card-title class="detail-card__header">
              {{ section.title }}
            </v-card-title>
            <v-card-text class="detail-card__body">
              <div v-for="item in section.items" :key="item.label" class="detail-row">
                <span class="detail-label">{{ item.label }}</span>
                <span class="detail-value">{{ item.value }}</span>
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
              :to="{ name: 'UpdatePatient', params: { id: patient_id } }"
          >
            {{ $t('patient_details.change_patient') }}
          </v-btn>

          <!-- TODO: implement patient deletion if needed for MVP -->
          <v-btn
              class="me-4"
              color="error"
              variant="flat"
              :disabled="!patient_id"
              @click="openDeleteDialog"
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

      <v-snackbar
          v-model="updateSuccessOpen"
          color="success"
          location="top"
          timeout="2500"
      >
        {{ $t('patient_details.update_success') }}
      </v-snackbar>
      <v-snackbar
          v-model="createSuccessOpen"
          color="success"
          location="top"
          timeout="2500"
      >
        {{ $t('patient_details.create_success') }}
      </v-snackbar>

      <v-dialog
          v-model="deleteDialog"
          max-width="520"
      >
        <v-card rounded="lg">
          <v-card-title class="text-h6">
            {{ $t('patient_details.delete_confirm_title') }}
          </v-card-title>
          <v-card-text>
            <p class="mb-4">
              {{ $t('patient_details.delete_confirm_body', { name: displayName }) }}
            </p>
            <v-alert
                v-if="deleteError"
                type="error"
                variant="tonal"
            >
              {{ deleteError }}
            </v-alert>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
                variant="text"
                :disabled="deleteLoading"
                @click="closeDeleteDialog"
            >
              {{ $t('patient_details.delete_confirm_cancel') }}
            </v-btn>
            <v-btn
                color="error"
                variant="flat"
                :loading="deleteLoading"
                @click="confirmDelete"
            >
              {{ $t('patient_details.delete_confirm_confirm') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-sheet>
  </v-container>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {API_BASE} from "@/lib/api";
import {useFeatureDefinitions} from "@/lib/featureDefinitions";

const route = useRoute();
const router = useRouter();

const rawId = route.params.id;
const patient_id = ref<string>(Array.isArray(rawId) ? rawId[0] : rawId ?? "");
const patient = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const deleteDialog = ref(false);
const deleteLoading = ref(false);
const deleteError = ref<string | null>(null);
const updateSuccessOpen = ref(false);
const createSuccessOpen = ref(false);

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

const {definitions, labels, sections} = useFeatureDefinitions()

const sectionOrder = [
  "Allgemein",
  "Demografie",
  "Sprache & Kommunikation",
  "Familienanamnese",
  "Präoperative Symptome",
  "Bildgebung",
  "Objektive Messungen",
  "Hörstatus – Operiertes Ohr",
  "Hörstatus – Gegenohr",
  "Behandlung & Outcome"
]

const labelFor = (name: string, fallback?: string) => {
  return labels.value?.[name] ?? fallback ?? name
}

const sectionLabelFor = (name: string) => {
  return sections.value?.[name] ?? name
}

const parseDisplayName = (value: string) => {
  if (!value) return {first: "", last: ""}
  if (value.includes(",")) {
    const parts = value.split(",").map((p) => p.trim())
    return {last: parts[0] || "", first: parts.slice(1).join(", ").trim()}
  }
  if (value.includes(" ")) {
    const parts = value.split(" ").filter(Boolean)
    return {first: parts[0] || "", last: parts.slice(1).join(" ").trim()}
  }
  return {first: "", last: value}
}

const formatValue = (value: unknown) => {
  if (value === undefined || value === null || value === "") return "—"
  if (Array.isArray(value)) return value.filter(Boolean).join(", ") || "—"
  return String(value)
}

const detailSections = computed(() => {
  const defs = definitions.value ?? []
  const input = patient.value?.input_features ?? {}
  const nameParts = parseDisplayName(displayName.value)

  const itemsBySection: Record<string, Array<{label: string; value: string}>> = {}

  for (const def of defs) {
    if (def?.ui_only) continue
    const section = def.section ?? "Weitere"
    let value: unknown
    if (def.normalized === "first_name") {
      value = nameParts.first
    } else if (def.normalized === "last_name") {
      value = nameParts.last
    } else {
      value = input?.[def.raw]
    }
    const label = labelFor(def.normalized, def.description ?? def.raw)
    itemsBySection[section] = itemsBySection[section] ?? []
    itemsBySection[section].push({label, value: formatValue(value)})
  }

  const orderedSections = sectionOrder.map((title) => ({
    title: sectionLabelFor(title),
    items: itemsBySection[title] ?? []
  }))

  const otherSections = Object.keys(itemsBySection)
    .filter((title) => !sectionOrder.includes(title))
    .sort()
    .map((title) => ({title: sectionLabelFor(title), items: itemsBySection[title]}))

  return [...orderedSections, ...otherSections]
    .filter((section) => section.items.length > 0)
    .filter((section) => section.title !== "Weitere")
})

const openDeleteDialog = () => {
  deleteError.value = null;
  deleteDialog.value = true;
};

const closeDeleteDialog = () => {
  if (!deleteLoading.value) {
    deleteDialog.value = false;
  }
};

const confirmDelete = async () => {
  if (!patient_id.value) {
    deleteError.value = "Missing patient id.";
    return;
  }

  deleteLoading.value = true;
  deleteError.value = null;

  try {
    const response = await fetch(
        `${API_BASE}/api/v1/patients/${encodeURIComponent(patient_id.value)}`,
        {
          method: "DELETE",
          headers: {
            accept: "application/json",
          },
        }
    );

    if (!response.ok) {
      let message = "Failed to delete patient.";
      try {
        const text = await response.text();
        if (text) message = text;
      } catch {
        // ignore parsing error
      }
      throw new Error(message);
    }

    deleteDialog.value = false;
    await router.push({name: "SearchPatients"});
  } catch (err: any) {
    console.error(err);
    deleteError.value = err?.message ?? "Failed to delete patient.";
  } finally {
    deleteLoading.value = false;
  }
};


onMounted(async () => {
  if (route.query.updated === '1') {
    updateSuccessOpen.value = true;
    router.replace({query: {...route.query, updated: undefined}});
  }
  if (route.query.created === '1') {
    createSuccessOpen.value = true;
    router.replace({query: {...route.query, created: undefined}});
  }

  if (!patient_id.value) {
    await router.replace({name: "NotFound"});
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

    if (response.status === 404) {
      await router.replace({name: "NotFound"});
      return;
    }
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
