<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="new-patient-card"
        rounded="lg"
    >

      <v-btn
          :to="{ name: 'SearchPatients' }"
          class="mb-4"
          color="primary"
          prepend-icon="mdi-arrow-left"
          size="small"
          variant="tonal"
      >
        {{ $t('form.back') }}
      </v-btn>
      <v-spacer/>
      <h1>{{ $t('form.title') }}</h1>
      <v-spacer/>
      <form class="new-patient-form" @submit.prevent="submit">
        <h3 class="section-title">Allgemein</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="first_name.value.value"
                :error-messages="first_name.errorMessage.value"
                label="Vorname"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="last_name.value.value"
                :error-messages="last_name.errorMessage.value"
                label="Nachname"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.demographics') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="age.value.value"
                :error-messages="age.errorMessage.value"
                :label="$t('patient_details.fields.age')"
                color="primary"
                hide-details="auto"
                type="number"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="gender.value.value"
                :error-messages="gender.errorMessage.value"
                :label="$t('patient_details.fields.gender')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="operated_side.value.value"
                :error-messages="operated_side.errorMessage.value"
                :label="$t('patient_details.fields.operated_side')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.language') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="primary_language.value.value"
                :error-messages="primary_language.errorMessage.value"
                :label="$t('patient_details.fields.primary_language')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="other_languages.value.value"
                :error-messages="other_languages.errorMessage.value"
                :label="$t('patient_details.fields.other_languages')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="german_language_barrier.value.value"
                :error-messages="german_language_barrier.errorMessage.value"
                :label="$t('patient_details.fields.german_language_barrier')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="non_verbal.value.value"
                :error-messages="non_verbal.errorMessage.value"
                :label="$t('patient_details.fields.non_verbal')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.family_history') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="parent_hearing_loss.value.value"
                :error-messages="parent_hearing_loss.errorMessage.value"
                :label="$t('patient_details.fields.parent_hearing_loss')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="sibling_hearing_loss.value.value"
                :error-messages="sibling_hearing_loss.errorMessage.value"
                :label="$t('patient_details.fields.sibling_hearing_loss')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.preop_symptoms') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="tinnitus_preop.value.value"
                :error-messages="tinnitus_preop.errorMessage.value"
                :label="$t('patient_details.fields.tinnitus_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="vertigo_preop.value.value"
                :error-messages="vertigo_preop.errorMessage.value"
                :label="$t('patient_details.fields.vertigo_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="otorrhea_preop.value.value"
                :error-messages="otorrhea_preop.errorMessage.value"
                :label="$t('patient_details.fields.otorrhea_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="headache_preop.value.value"
                :error-messages="headache_preop.errorMessage.value"
                :label="$t('patient_details.fields.headache_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="taste_preop.value.value"
                :error-messages="taste_preop.errorMessage.value"
                :label="$t('patient_details.fields.taste_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">Imaging</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="imaging_type_preop.value.value"
                :error-messages="imaging_type_preop.errorMessage.value"
                label="Imaging type (pre-op)"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="imaging_findings_preop.value.value"
                :error-messages="imaging_findings_preop.errorMessage.value"
                label="Imaging findings (pre-op)"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">Objective measurements</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="oae_status.value.value"
                :error-messages="oae_status.errorMessage.value"
                label="OAE status"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="ll_status.value.value"
                :error-messages="ll_status.errorMessage.value"
                label="LL status"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hz4k_status.value.value"
                :error-messages="hz4k_status.errorMessage.value"
                label="4 kHz status"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.hearing_status') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hl_operated_ear.value.value"
                :error-messages="hl_operated_ear.errorMessage.value"
                :label="$t('patient_details.fields.hl_operated_ear')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="amplification_operated_ear.value.value"
                :error-messages="amplification_operated_ear.errorMessage.value"
                label="Amplification operated ear"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hearing_loss_onset.value.value"
                :error-messages="hearing_loss_onset.errorMessage.value"
                :label="$t('patient_details.fields.hearing_loss_onset')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="acquisition_type.value.value"
                :error-messages="acquisition_type.errorMessage.value"
                label="Acquisition type"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hearing_loss_start.value.value"
                :error-messages="hearing_loss_start.errorMessage.value"
                :label="$t('patient_details.fields.hearing_loss_start')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="duration_severe_hl.value.value"
                :error-messages="duration_severe_hl.errorMessage.value"
                :label="$t('patient_details.fields.duration_severe_hl')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="etiology.value.value"
                :error-messages="etiology.errorMessage.value"
                :label="$t('patient_details.fields.etiology')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hearing_disorder_type.value.value"
                :error-messages="hearing_disorder_type.errorMessage.value"
                label="Hearing disorder type"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.hearing_status') }} – {{ $t('patient_details.fields.hl_contra_ear') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="hl_contra_ear.value.value"
                :error-messages="hl_contra_ear.errorMessage.value"
                :label="$t('patient_details.fields.hl_contra_ear')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="amplification_contra_ear.value.value"
                :error-messages="amplification_contra_ear.errorMessage.value"
                label="Amplification contralateral ear"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.treatment_outcome') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="ci_implant_type.value.value"
                :error-messages="ci_implant_type.errorMessage.value"
                :label="$t('patient_details.fields.ci_implant_type')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="pre_measure.value.value"
                :error-messages="pre_measure.errorMessage.value"
                :label="$t('patient_details.fields.pre_measure')"
                color="primary"
                hide-details="auto"
                type="number"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="post12_measure.value.value"
                :error-messages="post12_measure.errorMessage.value"
                :label="$t('patient_details.fields.post12_measure')"
                color="primary"
                hide-details="auto"
                type="number"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="post24_measure.value.value"
                :error-messages="post24_measure.errorMessage.value"
                :label="$t('patient_details.fields.post24_measure')"
                color="primary"
                hide-details="auto"
                type="number"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="interval_days.value.value"
                :error-messages="interval_days.errorMessage.value"
                :label="$t('patient_details.fields.interval_days')"
                color="primary"
                hide-details="auto"
                type="number"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <!-- Button row (unchanged buttons, just wrapped) -->
        <div class="new-patient-actions">
          <v-btn
              class="me-4"
              color="primary"
              type="submit"
              variant="flat"
          >
            {{ $t('form.submit') }}
          </v-btn>

          <v-btn
              color="primary"
              variant="outlined"
              @click="handleReset"
          >
            {{ $t('form.reset') }}
          </v-btn>
        </div>
      </form>
    </v-sheet>
  </v-container>
</template>


<script lang="ts" setup>
import {computed, ref} from 'vue'
import {useField, useForm} from 'vee-validate'
import i18next from 'i18next'

const language = ref(i18next.language)
i18next.on('languageChanged', (lng) => {
  language.value = lng
})

const validationSchema = computed(() => {
  // we need lang here, so that the error messages are reactive and
  // i18next is updated
  // console.log(lang); is added so that the IDE is not telling us
  // the lang variable is never used
  const lang = language.value
  console.log(lang);

  const translateError = (key: string, fallbackKey = 'form.error.name') =>
    i18next.t(key, {defaultValue: i18next.t(fallbackKey)})

  const requiredString = (value: unknown, key: string, fallbackKey = 'form.error.name') => {
    if (typeof value === 'string' && value.trim().length > 0) return true
    return translateError(key, fallbackKey)
  }

  const requiredNumber = (value: unknown, key: string, options?: { min?: number, max?: number }) => {
    if (value === undefined || value === null || value === '') return translateError(key)
    const numericValue = typeof value === 'number' ? value : Number(value)
    if (!Number.isFinite(numericValue)) return translateError(key)
    if (options?.min !== undefined && numericValue < options.min) return translateError(key)
    if (options?.max !== undefined && numericValue > options.max) return translateError(key)
    return true
  }

  return {
    last_name(value: string) {
      if (value?.trim().length >= 2) return true
      return i18next.t('form.error.name')
    },
    first_name(value: string) {
      if (value?.trim().length >= 2) return true
      return i18next.t('form.error.name')
    },
    age(value: unknown) {
      return requiredNumber(value, 'form.error.age', {min: 0, max: 130})
    },
    gender(value: unknown) {
      // TODO: Should be a select
      return !!(value);
    },
    operated_side(value: unknown) {
      // TODO: Should be a select
      return !!(value);
    },
    primary_language(value: unknown) {
      return requiredString(value, 'form.error.primary_language')
    },
    other_languages() {
      return true;
    },
    german_language_barrier() {
      return true;
    },
    non_verbal() {
      return true;
    },
    parent_hearing_loss() {
      return true;
    },
    sibling_hearing_loss() {
      return true;
    },
    taste_preop() {
      return true;
    },
    tinnitus_preop() {
      return true;
    },
    vertigo_preop() {
      return true;
    },
    otorrhea_preop() {
      return true;
    },
    headache_preop() {
      return true;
    },
    imaging_type_preop(value: unknown) {
      return requiredString(value, 'form.error.imaging_type_preop')
    },
    imaging_findings_preop(value: unknown) {
      return requiredString(value, 'form.error.imaging_findings_preop')
    },
    oae_status() {
      return true;
    },
    ll_status(value: unknown) {
      return requiredString(value, 'form.error.ll_status')
    },
    hz4k_status(value: unknown) {
      return requiredString(value, 'form.error.hz4k_status')
    },
    hl_operated_ear(value: unknown) {
      return requiredString(value, 'form.error.hl_operated_ear')
    },
    amplification_operated_ear(value: unknown) {
      return requiredString(value, 'form.error.amplification_operated_ear')
    },
    hearing_loss_onset(value: unknown) {
      return requiredString(value, 'form.error.hearing_loss_onset')
    },
    acquisition_type(value: unknown) {
      return requiredString(value, 'form.error.acquisition_type')
    },
    hearing_loss_start(value: unknown) {
      return requiredString(value, 'form.error.hearing_loss_start')
    },
    duration_severe_hl(value: unknown) {
      // TODO: Should be a select
      return !!(value);
    },
    etiology(value: unknown) {
      // TODO: Should be a select
      return !!(value);
    },
    hearing_disorder_type(value: unknown) {
      return requiredString(value, 'form.error.hearing_disorder_type')
    },
    hl_contra_ear(value: unknown) {
      return requiredString(value, 'form.error.hl_contra_ear')
    },
    amplification_contra_ear(value: unknown) {
      return requiredString(value, 'form.error.amplification_contra_ear')
    },
    ci_implant_type(value: unknown) {
      return requiredString(value, 'form.error.ci_implant_type')
    },
    pre_measure(value: unknown) {
      return requiredNumber(value, 'form.error.pre_measure', {min: 0})
    },
    post12_measure(value: unknown) {
      return requiredNumber(value, 'form.error.post12_measure', {min: 0})
    },
    post24_measure(value: unknown) {
      return requiredNumber(value, 'form.error.post24_measure', {min: 0})
    },
    interval_days(value: unknown) {
      return requiredNumber(value, 'form.error.interval_days', {min: 0})
    },
  }
})

const {handleSubmit, handleReset} = useForm({
  validationSchema,
})

const last_name = useField("last_name")
const first_name = useField("first_name")

// Demographics
const age = useField("age")
// TODO: Should be a select
const gender = useField("gender")
// TODO: Should be a select
const operated_side = useField("operated_side")

// Language / Communication
const primary_language = useField("primary_language")
const other_languages = useField("other_languages")

// TODO: Should be a checkbox.
const german_language_barrier = useField("german_language_barrier")
// TODO: Should be a checkbox.
const non_verbal = useField("non_verbal")

// Family history
const parent_hearing_loss = useField("parent_hearing_loss")
const sibling_hearing_loss = useField("sibling_hearing_loss")

// Pre-operative symptoms
// TODO: Should be a checkbox
const taste_preop = useField("taste_preop")
// TODO: Should be a checkbox
const tinnitus_preop = useField("tinnitus_preop")
// TODO: Should be a checkbox
const vertigo_preop = useField("vertigo_preop")
// TODO: Should be a checkbox
const otorrhea_preop = useField("otorrhea_preop")
// TODO: Should be a checkbox
const headache_preop = useField("headache_preop")

// Imaging
const imaging_type_preop = useField("imaging_type_preop")
const imaging_findings_preop = useField("imaging_findings_preop")

// Objective measurements
// TODO: Should be a checkbox
const oae_status = useField("oae_status")
const ll_status = useField("ll_status")
const hz4k_status = useField("hz4k_status")

// Hearing loss – operated ear
const hl_operated_ear = useField("hl_operated_ear")
const amplification_operated_ear = useField("amplification_operated_ear")
const hearing_loss_onset = useField("hearing_loss_onset")
const acquisition_type = useField("acquisition_type")
// TODO: Should be a select
const hearing_loss_start = useField("hearing_loss_start")
// TODO: Should be a select
const duration_severe_hl = useField("duration_severe_hl")
// TODO: Should be a select
const etiology = useField("etiology")
const hearing_disorder_type = useField("hearing_disorder_type")

// Hearing loss – contralateral ear
const hl_contra_ear = useField("hl_contra_ear")
const amplification_contra_ear = useField("amplification_contra_ear")

// Treatment
const ci_implant_type = useField("ci_implant_type")

// Outcome
const pre_measure = useField("pre_measure")
const post12_measure = useField("post12_measure")
const post24_measure = useField("post24_measure")
const interval_days = useField("interval_days")


const submit = handleSubmit(values => {
  alert(JSON.stringify(values, null, 2))
})
</script>


<style scoped>
.new-patient-card {
  padding: 32px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}

/* space between title and first row */
.new-patient-card h1 {
  margin: 8px 0 24px 0;
}

.section-title {
  margin: 12px 0 8px;
  font-weight: 600;
}

/* form layout */
.new-patient-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* buttons aligned like in the mockup */
.new-patient-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}
</style>
