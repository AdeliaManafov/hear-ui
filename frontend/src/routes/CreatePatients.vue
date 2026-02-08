<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="new-patient-card"
        rounded="lg"
    >

      <v-btn
          :to="backTarget"
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
        <h3 class="section-title">{{ sectionLabelFor('Allgemein') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="first_name.value.value"
                :error-messages="first_name.errorMessage.value"
                :label="labelFor('first_name', $t('patient_details.fields.first_name'))"
                required
                color="primary"
                hide-details="auto"
                :hint="$t('form.hints.first_name')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="last_name.value.value"
                :error-messages="last_name.errorMessage.value"
                :label="labelFor('last_name', $t('patient_details.fields.last_name'))"
                required
                color="primary"
                hide-details="auto"
                :hint="$t('form.hints.last_name')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Demografie') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="age.value.value"
                :error-messages="age.errorMessage.value"
                :label="labelFor('age', $t('patient_details.fields.age'))"
                required
                color="primary"
                hide-details="auto"
                :hint="$t('form.hints.age')"
                persistent-hint
                type="number"
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="gender.value.value"
                :error-messages="gender.errorMessage.value"
                :items="genderOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('gender', $t('patient_details.fields.gender'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.gender')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="operated_side.value.value"
                :error-messages="operated_side.errorMessage.value"
                :items="operatedSideOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('operated_side', $t('patient_details.fields.operated_side'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.operated_side')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Sprache & Kommunikation') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="primary_language.value.value"
                :error-messages="primary_language.errorMessage.value"
                :label="labelFor('primary_language', $t('patient_details.fields.primary_language'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.primary_language')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="other_languages.value.value"
                :error-messages="other_languages.errorMessage.value"
                :label="labelFor('other_languages', $t('patient_details.fields.other_languages'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.other_languages')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-checkbox
                v-model="german_language_barrier.value.value"
                :error-messages="german_language_barrier.errorMessage.value"
                :label="labelFor('german_language_barrier', $t('patient_details.fields.german_language_barrier'))"
                color="primary"
                hide-details="auto"
                :true-value="true"
                :false-value="false"
                :hint="$t('form.hints.german_language_barrier')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-checkbox
                v-model="non_verbal.value.value"
                :error-messages="non_verbal.errorMessage.value"
                :label="labelFor('non_verbal', $t('patient_details.fields.non_verbal'))"
                color="primary"
                hide-details="auto"
                :true-value="true"
                :false-value="false"
                :hint="$t('form.hints.non_verbal')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Familienanamnese') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="parent_hearing_loss.value.value"
                :error-messages="parent_hearing_loss.errorMessage.value"
                :label="labelFor('parent_hearing_loss', $t('patient_details.fields.parent_hearing_loss'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.parent_hearing_loss')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="sibling_hearing_loss.value.value"
                :error-messages="sibling_hearing_loss.errorMessage.value"
                :label="labelFor('sibling_hearing_loss', $t('patient_details.fields.sibling_hearing_loss'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.sibling_hearing_loss')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Präoperative Symptome') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="tinnitus_preop.value.value"
                :error-messages="tinnitus_preop.errorMessage.value"
                :label="labelFor('tinnitus_preop', $t('patient_details.fields.tinnitus_preop'))"
                color="primary"
                hide-details="auto"
                :true-value="getOptionValueByRole('tinnitus_preop', 'true', 'Vorhanden')"
                :false-value="getOptionValueByRole('tinnitus_preop', 'false', 'Kein')"
                :hint="$t('form.hints.tinnitus_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="vertigo_preop.value.value"
                :error-messages="vertigo_preop.errorMessage.value"
                :label="labelFor('vertigo_preop', $t('patient_details.fields.vertigo_preop'))"
                color="primary"
                hide-details="auto"
                :true-value="getOptionValueByRole('vertigo_preop', 'true', 'Vorhanden')"
                :false-value="getOptionValueByRole('vertigo_preop', 'false', 'Kein')"
                :hint="$t('form.hints.vertigo_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="otorrhea_preop.value.value"
                :error-messages="otorrhea_preop.errorMessage.value"
                :label="labelFor('otorrhea_preop', $t('patient_details.fields.otorrhea_preop'))"
                color="primary"
                hide-details="auto"
                :true-value="getOptionValueByRole('otorrhea_preop', 'true', 'Vorhanden')"
                :false-value="getOptionValueByRole('otorrhea_preop', 'false', 'Keine')"
                :hint="$t('form.hints.otorrhea_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-checkbox
                v-model="headache_preop.value.value"
                :error-messages="headache_preop.errorMessage.value"
                :label="labelFor('headache_preop', $t('patient_details.fields.headache_preop'))"
                color="primary"
                hide-details="auto"
                :true-value="getOptionValueByRole('headache_preop', 'true', 'Vorhanden')"
                :false-value="getOptionValueByRole('headache_preop', 'false', 'Keine')"
                :hint="$t('form.hints.headache_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
                v-model="taste_preop.value.value"
                :error-messages="taste_preop.errorMessage.value"
                :items="tasteOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('taste_preop', $t('patient_details.fields.taste_preop'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.taste_preop')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Bildgebung') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-combobox
                :model-value="imagingTypeSelection"
                @update:model-value="onImagingTypeChange"
                :error-messages="imaging_type_preop.errorMessage.value"
                :items="imagingTypeOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('imaging_type_preop', $t('patient_details.fields.imaging_type_preop'))"
                color="primary"
                chips
                closable-chips
                multiple
                clearable
                :hint="$t('form.hints.imaging_type_preop')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="imaging_findings_preop.value.value"
                :error-messages="imaging_findings_preop.errorMessage.value"
                :label="labelFor('imaging_findings_preop', $t('patient_details.fields.imaging_findings_preop'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.imaging_findings_preop')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Objektive Messungen') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="oae_status.value.value"
                :error-messages="oae_status.errorMessage.value"
                :label="labelFor('oae_status', $t('patient_details.fields.objective_oae'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.objective_oae') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.objective_oae') }}</p>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="ll_status.value.value"
                :error-messages="ll_status.errorMessage.value"
                :label="labelFor('ll_status', $t('patient_details.fields.objective_ll'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.objective_ll') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.objective_ll') }}</p>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="hz4k_status.value.value"
                :error-messages="hz4k_status.errorMessage.value"
                :label="labelFor('hz4k_status', $t('patient_details.fields.objective_4k'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.objective_4k') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.objective_4k') }}</p>
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Hörstatus – Operiertes Ohr') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
                v-model="hl_operated_ear.value.value"
                :error-messages="hl_operated_ear.errorMessage.value"
                :items="hlOperatedOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('hl_operated_ear', $t('patient_details.fields.hl_operated_ear'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hl_operated_ear')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="isOtherSelected('hl_operated_ear', hl_operated_ear.value.value)"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="hl_operated_other.value.value"
                :error-messages="hl_operated_other.errorMessage.value"
                :label="labelFor('hl_operated_other', $t('patient_details.fields.hl_operated_other'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.hl_operated_other') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.hl_operated_other') }}</p>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="amplification_operated_ear.value.value"
                :error-messages="amplification_operated_ear.errorMessage.value"
                :items="amplificationOperatedOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('amplification_operated_ear', $t('patient_details.fields.amplification_operated_ear'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.amplification_operated_ear')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="isOtherSelected('amplification_operated_ear', amplification_operated_ear.value.value)"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="amplification_operated_other.value.value"
                :error-messages="amplification_operated_other.errorMessage.value"
                :label="labelFor('amplification_operated_other', $t('patient_details.fields.amplification_operated_other'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.amplification_operated_other') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.amplification_operated_other') }}</p>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="hearing_loss_onset.value.value"
                :error-messages="hearing_loss_onset.errorMessage.value"
                :items="hearingLossOnsetOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('hearing_loss_onset', $t('patient_details.fields.hearing_loss_onset'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hearing_loss_onset')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="acquisition_type.value.value"
                :error-messages="acquisition_type.errorMessage.value"
                :items="acquisitionTypeOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('acquisition_type', $t('patient_details.fields.acquisition_type'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.acquisition_type')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="hearing_loss_start.value.value"
                :error-messages="hearing_loss_start.errorMessage.value"
                :items="hearingLossStartOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('hearing_loss_start', $t('patient_details.fields.hearing_loss_start'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hearing_loss_start')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="duration_severe_hl.value.value"
                :error-messages="duration_severe_hl.errorMessage.value"
                :items="durationSevereOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('duration_severe_hl', $t('patient_details.fields.duration_severe_hl'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.duration_severe_hl')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="etiology.value.value"
                :error-messages="etiology.errorMessage.value"
                :label="labelFor('etiology', $t('patient_details.fields.etiology'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.etiology')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="hearing_disorder_type.value.value"
                :error-messages="hearing_disorder_type.errorMessage.value"
                :items="hearingDisorderTypeOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('hearing_disorder_type', $t('patient_details.fields.hearing_disorder_type'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hearing_disorder_type')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="isOtherSelected('hearing_disorder_type', hearing_disorder_type.value.value)"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="hearing_disorder_other.value.value"
                :error-messages="hearing_disorder_other.errorMessage.value"
                :label="labelFor('hearing_disorder_other', $t('patient_details.fields.hearing_disorder_other'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.hearing_disorder_other') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.hearing_disorder_other') }}</p>
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Hörstatus – Gegenohr') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
                v-model="hl_contra_ear.value.value"
                :error-messages="hl_contra_ear.errorMessage.value"
                :items="hlContraOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('hl_contra_ear', $t('patient_details.fields.hl_contra_ear'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hl_contra_ear')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
                v-model="amplification_contra_ear.value.value"
                :error-messages="amplification_contra_ear.errorMessage.value"
                :items="amplificationContraOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('amplification_contra_ear', $t('patient_details.fields.amplification_contra_ear'))"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.amplification_contra_ear')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ sectionLabelFor('Behandlung & Outcome') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
                v-model="ci_implant_type.value.value"
                :error-messages="ci_implant_type.errorMessage.value"
                :items="ciImplantTypeOptions"
                item-title="title"
                item-value="value"
                :label="labelFor('ci_implant_type', $t('patient_details.fields.ci_implant_type'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.ci_implant_type')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="isOtherSelected('ci_implant_type', ci_implant_type.value.value)"
              cols="12"
              md="6"
          >
            <v-text-field
                v-model="ci_implant_other.value.value"
                :error-messages="ci_implant_other.errorMessage.value"
                :label="labelFor('ci_implant_other', $t('patient_details.fields.ci_implant_other'))"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="submitAttempted ? $t('form.hints.ci_implant_other') : undefined"
                :persistent-hint="submitAttempted"
            />
            <p class="field-description">{{ $t('form.descriptions.ci_implant_other') }}</p>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="pre_measure.value.value"
                :error-messages="pre_measure.errorMessage.value"
                :label="labelFor('pre_measure', $t('patient_details.fields.pre_measure'))"
                color="primary"
                hide-details="auto"
                type="number"
                :hint="$t('form.hints.pre_measure')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="post12_measure.value.value"
                :error-messages="post12_measure.errorMessage.value"
                :label="labelFor('post12_measure', $t('patient_details.fields.post12_measure'))"
                color="primary"
                hide-details="auto"
                type="number"
                :hint="$t('form.hints.post12_measure')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="post24_measure.value.value"
                :error-messages="post24_measure.errorMessage.value"
                :label="labelFor('post24_measure', $t('patient_details.fields.post24_measure'))"
                color="primary"
                hide-details="auto"
                type="number"
                :hint="$t('form.hints.post24_measure')"
                persistent-hint
                variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="interval_days.value.value"
                :error-messages="interval_days.errorMessage.value"
                :label="labelFor('interval_days', $t('patient_details.fields.interval_days'))"
                color="primary"
                hide-details="auto"
                type="number"
                :hint="$t('form.hints.interval_days')"
                persistent-hint
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
        </div>
      </form>
    </v-sheet>

    <v-snackbar
        v-model="updateSuccessOpen"
        color="success"
        location="top"
        timeout="2500"
    >
      {{ $t('patient_details.update_success') }}
    </v-snackbar>
  </v-container>
</template>


<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue'
import {useField, useForm} from 'vee-validate'
import i18next from 'i18next'
import {API_BASE} from '@/lib/api'
import {useRoute, useRouter} from 'vue-router'
import {useFeatureDefinitions} from '@/lib/featureDefinitions'

const language = ref(i18next.language)
i18next.on('languageChanged', (lng) => {
  language.value = lng
})

const route = useRoute()
const router = useRouter()
const rawId = route.params.id
const patientId = ref<string>(Array.isArray(rawId) ? rawId[0] : rawId ?? '')
const isEdit = computed(() => Boolean(patientId.value))
const backTarget = computed(() =>
  isEdit.value ? {name: 'PatientDetail', params: {id: patientId.value}} : {name: 'SearchPatients'}
)

const submitAttempted = ref(false)
const updateSuccessOpen = ref(false)
const {definitionsByNormalized, labels, sections} = useFeatureDefinitions()

const featureDefinitions = computed(() => definitionsByNormalized.value)

const resolveOptionLabel = (option: any) => {
  const lang = language.value?.startsWith('de') ? 'de' : 'en'
  return option?.labels?.[lang] ?? option?.label ?? option?.value
}

const labelFor = (name: string, fallback?: string) => {
  return labels.value?.[name] ?? fallback ?? name
}

const sectionLabelFor = (name: string, fallback?: string) => {
  return sections.value?.[name] ?? fallback ?? name
}

const makeOptions = (name: string) =>
  computed(() => {
    const options = featureDefinitions.value?.[name]?.options ?? []
    return options.map((opt: any) => ({
      title: resolveOptionLabel(opt),
      value: opt.value,
    }))
  })

const getOtherValues = (name: string) =>
  computed(() => {
    const options = featureDefinitions.value?.[name]?.options
    if (!Array.isArray(options)) return []
    return options.filter((opt: any) => opt?.is_other).map((opt: any) => opt.value)
  })

const isOtherSelected = (name: string, value: unknown) => {
  return getOtherValues(name).value.includes(String(value))
}

const getOptionValuesByFlag = (name: string, flag: string) =>
  computed(() => {
    const options = featureDefinitions.value?.[name]?.options
    if (!Array.isArray(options)) return []
    return options.filter((opt: any) => opt?.[flag]).map((opt: any) => opt.value)
  })

const getOptionValueByRole = (name: string, role: string, fallback: string) => {
  const options = featureDefinitions.value?.[name]?.options
  if (!Array.isArray(options)) return fallback
  const match = options.find((opt: any) => opt?.role === role)
  return match?.value ?? fallback
}

const genderOptions = makeOptions('gender')
const operatedSideOptions = makeOptions('operated_side')
const imagingTypeOptions = makeOptions('imaging_type_preop')
const hlOperatedOptions = makeOptions('hl_operated_ear')
const amplificationOperatedOptions = makeOptions('amplification_operated_ear')
const hearingLossOnsetOptions = makeOptions('hearing_loss_onset')
const acquisitionTypeOptions = makeOptions('acquisition_type')
const hearingLossStartOptions = makeOptions('hearing_loss_start')
const durationSevereOptions = makeOptions('duration_severe_hl')
const hearingDisorderTypeOptions = makeOptions('hearing_disorder_type')
const hlContraOptions = makeOptions('hl_contra_ear')
const amplificationContraOptions = makeOptions('amplification_contra_ear')
const ciImplantTypeOptions = makeOptions('ci_implant_type')
const tasteOptions = makeOptions('taste_preop')

const amplificationOtherValues = getOtherValues('amplification_operated_ear')
const hearingDisorderOtherValues = getOtherValues('hearing_disorder_type')
const hlOperatedOtherValues = getOtherValues('hl_operated_ear')
const ciImplantOtherValues = getOtherValues('ci_implant_type')

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
      if (value) return true
      return i18next.t('form.error.gender')
    },
    operated_side(value: unknown) {
      if (value) return true
      return i18next.t('form.error.operated_side')
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
      if (Array.isArray(value) && value.length > 0) return true
      return requiredString(value as string, 'form.error.imaging_type_preop')
    },
    imaging_findings_preop(value: unknown) {
      return requiredString(value, 'form.error.imaging_findings_preop')
    },
    oae_status(value: unknown) {
      return requiredString(value, 'form.error.oae_status')
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
    hl_operated_other(value: unknown, ctx: any) {
      if (isOtherSelected('hl_operated_ear', ctx?.form?.hl_operated_ear)) {
        return requiredString(value, 'form.error.hl_operated_other')
      }
      return true
    },
    amplification_operated_ear(value: unknown) {
      return requiredString(value, 'form.error.amplification_operated_ear')
    },
    amplification_operated_other(value: unknown, ctx: any) {
      if (isOtherSelected('amplification_operated_ear', ctx?.form?.amplification_operated_ear)) {
        return requiredString(value, 'form.error.amplification_operated_other')
      }
      return true
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
      return requiredString(value as string, 'form.error.duration_severe_hl')
    },
    etiology(value: unknown) {
      return requiredString(value as string, 'form.error.etiology')
    },
    hearing_disorder_type(value: unknown) {
      return requiredString(value, 'form.error.hearing_disorder_type')
    },
    hearing_disorder_other(value: unknown, ctx: any) {
      if (isOtherSelected('hearing_disorder_type', ctx?.form?.hearing_disorder_type)) {
        return requiredString(value, 'form.error.hearing_disorder_other')
      }
      return true
    },
    hl_contra_ear(value: unknown) {
      return requiredString(value, 'form.error.hl_contra_ear')
    },
    amplification_contra_ear(value: unknown) {
      return requiredString(value, 'form.error.amplification_contra_ear')
    },
    ci_implant_type() {
      // Optional: do not block submission if treatment info is not available yet
      return true
    },
    ci_implant_other(value: unknown, ctx: any) {
      if (isOtherSelected('ci_implant_type', ctx?.form?.ci_implant_type)) {
        return requiredString(value, 'form.error.ci_implant_other')
      }
      return true
    },
    pre_measure() {
      return true;
    },
    post12_measure() {
      return true;
    },
    post24_measure() {
      return true;
    },
    interval_days() {
      return true;
    },
  }
})

const {handleSubmit, handleReset, setFieldTouched, setFieldValue, values} = useForm({
  validationSchema,
})

const last_name = useField("last_name")
const first_name = useField("first_name")

// Demographics
const age = useField("age")
const gender = useField("gender")
const operated_side = useField("operated_side")

// Language / Communication
const primary_language = useField("primary_language")
const other_languages = useField("other_languages")

const german_language_barrier = useField("german_language_barrier")
const non_verbal = useField("non_verbal")

// Family history
const parent_hearing_loss = useField("parent_hearing_loss")
const sibling_hearing_loss = useField("sibling_hearing_loss")

// Pre-operative symptoms
const taste_preop = useField("taste_preop")
const tinnitus_preop = useField("tinnitus_preop")
const vertigo_preop = useField("vertigo_preop")
const otorrhea_preop = useField("otorrhea_preop")
const headache_preop = useField("headache_preop")

// Imaging
const imaging_type_preop = useField("imaging_type_preop", undefined, {initialValue: [] as string[]})
const imaging_findings_preop = useField("imaging_findings_preop")

const imagingTypeSelection = ref<string[]>([])

const normalizeImagingValue = (val: unknown): string[] => {
  if (Array.isArray(val)) {
    return val
      .map((entry: any) => (entry && typeof entry === 'object' ? entry.value : entry))
      .filter((entry) => entry !== undefined && entry !== null && entry !== '')
      .map((entry) => String(entry))
  }
  if (val === undefined || val === null || val === '') return []
  if (typeof val === 'object') {
    const value = (val as any)?.value
    return value === undefined || value === null || value === '' ? [] : [String(value)]
  }
  return [String(val)]
}

watch(
  () => imaging_type_preop.value.value,
  (val) => {
    imagingTypeSelection.value = normalizeImagingValue(val)
  },
  {immediate: true}
)

const onImagingTypeChange = (val: unknown) => {
  const normalized = normalizeImagingValue(val)
  imagingTypeSelection.value = normalized
  setFieldValue('imaging_type_preop', normalized)
}

// Objective measurements
const oae_status = useField("oae_status")
const ll_status = useField("ll_status")
const hz4k_status = useField("hz4k_status")

// Hearing loss – operated ear
const hl_operated_ear = useField("hl_operated_ear")
const hl_operated_other = useField("hl_operated_other")
const amplification_operated_ear = useField("amplification_operated_ear")
const amplification_operated_other = useField("amplification_operated_other")
const hearing_loss_onset = useField("hearing_loss_onset")
const acquisition_type = useField("acquisition_type")
const hearing_loss_start = useField("hearing_loss_start")
const duration_severe_hl = useField("duration_severe_hl")
const etiology = useField("etiology")
const hearing_disorder_type = useField("hearing_disorder_type")
const hearing_disorder_other = useField("hearing_disorder_other")

// Hearing loss – contralateral ear
const hl_contra_ear = useField("hl_contra_ear")
const amplification_contra_ear = useField("amplification_contra_ear")

// Treatment
const ci_implant_type = useField("ci_implant_type")
const ci_implant_other = useField("ci_implant_other")

// Outcome
const pre_measure = useField("pre_measure")
const post12_measure = useField("post12_measure")
const post24_measure = useField("post24_measure")
const interval_days = useField("interval_days")

const allFieldNames = [
  "first_name",
  "last_name",
  "age",
  "gender",
  "operated_side",
  "primary_language",
  "other_languages",
  "german_language_barrier",
  "non_verbal",
  "parent_hearing_loss",
  "sibling_hearing_loss",
  "taste_preop",
  "tinnitus_preop",
  "vertigo_preop",
  "otorrhea_preop",
  "headache_preop",
  "imaging_type_preop",
  "imaging_findings_preop",
  "oae_status",
  "ll_status",
  "hz4k_status",
  "hl_operated_ear",
  "hl_operated_other",
  "amplification_operated_ear",
  "amplification_operated_other",
  "hearing_loss_onset",
  "acquisition_type",
  "hearing_loss_start",
  "duration_severe_hl",
  "etiology",
  "hearing_disorder_type",
  "hearing_disorder_other",
  "hl_contra_ear",
  "amplification_contra_ear",
  "ci_implant_type",
  "ci_implant_other",
  "pre_measure",
  "post12_measure",
  "post24_measure",
  "interval_days",
]


const resolveOther = (value: unknown, other: unknown, triggers: string[]) => {
  if (typeof value === 'string' && triggers.includes(value)) return other
  return value
}

const withDefault = (value: any, fallback = 'Keine') => {
  if (Array.isArray(value)) return value.length ? value : fallback
  if (value === undefined || value === null || value === '') return fallback
  return value
}

const checkboxToString = (value: any) => value ? 'Vorhanden' : 'Keine'

const normalizeErrors = (errors: Record<string, unknown>) => {
  const toMessage = (err: unknown): string | undefined => {
    if (!err) return undefined
    if (typeof err === 'string') return err
    if (err instanceof Error) return err.message
    if (Array.isArray(err)) {
      const nested = err.map(toMessage).filter(Boolean) as string[]
      return nested.length ? nested.join('\n') : undefined
    }
    if (typeof err === 'object') {
      try {
        const serialized = JSON.stringify(err)
        return serialized === '{}' ? undefined : serialized
      } catch (e) {
        return String(err)
      }
    }
    return String(err)
  }

  const messages: string[] = []
  Object.values(errors || {}).forEach(err => {
    const msg = toMessage(err)
    if (msg) messages.push(msg)
  })
  return messages
}

const stableStringify = (value: any): string => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`
  const keys = Object.keys(value).sort()
  const entries = keys.map(k => `${JSON.stringify(k)}:${stableStringify(value[k])}`)
  return `{${entries.join(',')}}`
}

const buildSnapshot = (formValues: Record<string, any>) => {
  const displayName = [formValues.last_name, formValues.first_name].filter(Boolean).join(", ")
  return {
    display_name: displayName || null,
    input_features: buildInputFeatures(formValues),
  }
}

const toBool = (value: unknown) => {
  if (value === true) return true
  if (value === false) return false
  if (typeof value === 'string') {
    const normalized = value.trim().toLowerCase()
    return normalized === 'vorhanden' || normalized === 'ja' || normalized === 'true' || normalized === 'yes'
  }
  return false
}

const toCheckboxValue = (value: unknown, falseValue = 'Keine') => {
  if (typeof value === 'string' && value.trim()) return value
  if (value === true) return 'Vorhanden'
  if (value === false) return falseValue
  return ''
}

const splitImagingTypes = (value: unknown): string[] => {
  if (Array.isArray(value)) return value.map(v => String(v).trim()).filter(Boolean)
  if (typeof value !== 'string') return []
  return value
    .split(',')
    .map(v => v.trim())
    .filter(Boolean)
    .map(v => {
      const lower = v.toLowerCase()
      if (lower === 'ct') return 'CT'
      if (lower === 'mrt') return 'MRT'
      if (lower === 'konventionell') return 'Konventionell'
      return v
    })
}

const buildInputFeatures = (values: Record<string, any>) => {
  const imagingTypes = normalizeImagingValue(values.imaging_type_preop)
  const input_features: Record<string, any> = {
    "Alter [J]": Number(values.age),
    "Geschlecht": withDefault(values.gender),
    "Seiten": withDefault(values.operated_side),
    "Primäre Sprache": withDefault(values.primary_language),
    "Weitere Sprachen": withDefault(values.other_languages),
    "Deutsch Sprachbarriere": checkboxToString(values.german_language_barrier),
    "non-verbal": checkboxToString(values.non_verbal),
    "Eltern m. Schwerhörigkeit": withDefault(values.parent_hearing_loss),
    "Geschwister m. SH": withDefault(values.sibling_hearing_loss),
    "Symptome präoperativ.Geschmack...": withDefault(values.taste_preop),
    "Symptome präoperativ.Tinnitus...": withDefault(values.tinnitus_preop),
    "Symptome präoperativ.Schwindel...": withDefault(values.vertigo_preop),
    "Symptome präoperativ.Otorrhoe...": withDefault(values.otorrhea_preop),
    "Symptome präoperativ.Kopfschmerzen...": withDefault(values.headache_preop),
    "Bildgebung, präoperativ.Typ...": withDefault(imagingTypes.join(', ')),
    "Bildgebung, präoperativ.Befunde...": withDefault(values.imaging_findings_preop),
    "Objektive Messungen.OAE (TEOAE/DPOAE)...": withDefault(values.oae_status),
    "Objektive Messungen.LL...": withDefault(values.ll_status),
    "Objektive Messungen.4000 Hz...": withDefault(values.hz4k_status),
    "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": withDefault(resolveOther(values.hl_operated_ear, values.hl_operated_other, hlOperatedOtherValues.value ?? [])),
    "Diagnose.Höranamnese.Versorgung operiertes Ohr...": withDefault(resolveOther(values.amplification_operated_ear, values.amplification_operated_other, amplificationOtherValues.value ?? [])),
    "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...": withDefault(values.hearing_loss_onset),
    "Diagnose.Höranamnese.Erwerbsart...": withDefault(values.acquisition_type),
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": withDefault(values.hearing_loss_start),
    "Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...": withDefault(values.duration_severe_hl),
    "Diagnose.Höranamnese.Ursache....Ursache...": withDefault(values.etiology),
    "Diagnose.Höranamnese.Art der Hörstörung...": withDefault(resolveOther(values.hearing_disorder_type, values.hearing_disorder_other, hearingDisorderOtherValues.value ?? [])),
    "Diagnose.Höranamnese.Hörminderung Gegenohr...": withDefault(values.hl_contra_ear),
    "Diagnose.Höranamnese.Versorgung Gegenohr...": withDefault(values.amplification_contra_ear),
    "Behandlung/OP.CI Implantation": withDefault(resolveOther(values.ci_implant_type, values.ci_implant_other, ciImplantOtherValues.value ?? [])),
    "outcome_measurments.pre.measure.": Number(values.pre_measure),
    "outcome_measurments.post12.measure.": Number(values.post12_measure),
    "outcome_measurments.post24.measure.": Number(values.post24_measure),
    "abstand": Number(values.interval_days),
  }
  return input_features
}

const initialSnapshot = ref<string | null>(null)

const populateFormForEdit = (patient: any) => {
  const input = patient?.input_features || {}
  const displayName = String(patient?.display_name || '')
  let first = ''
  let last = ''
  if (displayName.includes(',')) {
    const parts = displayName.split(',').map(p => p.trim())
    last = parts[0] || ''
    first = parts.slice(1).join(', ').trim()
  } else if (displayName.includes(' ')) {
    const parts = displayName.split(' ').filter(Boolean)
    first = parts[0] || ''
    last = parts.slice(1).join(' ').trim()
  } else {
    last = displayName
  }

  setFieldValue('first_name', first)
  setFieldValue('last_name', last)
  setFieldValue('age', input["Alter [J]"] ?? '')
  setFieldValue('gender', input["Geschlecht"] ?? '')
  setFieldValue('operated_side', input["Seiten"] ?? '')
  setFieldValue('primary_language', input["Primäre Sprache"] ?? '')
  setFieldValue('other_languages', input["Weitere Sprachen"] ?? '')
  setFieldValue('german_language_barrier', toBool(input["Deutsch Sprachbarriere"]))
  setFieldValue('non_verbal', toBool(input["non-verbal"]))
  setFieldValue('parent_hearing_loss', input["Eltern m. Schwerhörigkeit"] ?? '')
  setFieldValue('sibling_hearing_loss', input["Geschwister m. SH"] ?? '')
  setFieldValue('taste_preop', input["Symptome präoperativ.Geschmack..."] ?? '')
  setFieldValue('tinnitus_preop', toCheckboxValue(input["Symptome präoperativ.Tinnitus..."], 'Kein'))
  setFieldValue('vertigo_preop', toCheckboxValue(input["Symptome präoperativ.Schwindel..."], 'Kein'))
  setFieldValue('otorrhea_preop', toCheckboxValue(input["Symptome präoperativ.Otorrhoe..."], 'Keine'))
  setFieldValue('headache_preop', toCheckboxValue(input["Symptome präoperativ.Kopfschmerzen..."], 'Keine'))
  setFieldValue('imaging_type_preop', splitImagingTypes(input["Bildgebung, präoperativ.Typ..."]))
  setFieldValue('imaging_findings_preop', input["Bildgebung, präoperativ.Befunde..."] ?? '')
  setFieldValue('oae_status', input["Objektive Messungen.OAE (TEOAE/DPOAE)..."] ?? '')
  setFieldValue('ll_status', input["Objektive Messungen.LL..."] ?? '')
  setFieldValue('hz4k_status', input["Objektive Messungen.4000 Hz..."] ?? '')
  setFieldValue('hl_operated_ear', input["Diagnose.Höranamnese.Hörminderung operiertes Ohr..."] ?? '')
  setFieldValue('amplification_operated_ear', input["Diagnose.Höranamnese.Versorgung operiertes Ohr..."] ?? '')
  setFieldValue('hearing_loss_onset', input["Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)..."] ?? '')
  setFieldValue('acquisition_type', input["Diagnose.Höranamnese.Erwerbsart..."] ?? '')
  setFieldValue('hearing_loss_start', input["Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)..."] ?? '')
  setFieldValue('duration_severe_hl', input["Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)..."] ?? '')
  setFieldValue('etiology', input["Diagnose.Höranamnese.Ursache....Ursache..."] ?? '')
  setFieldValue('hearing_disorder_type', input["Diagnose.Höranamnese.Art der Hörstörung..."] ?? '')
  setFieldValue('hl_contra_ear', input["Diagnose.Höranamnese.Hörminderung Gegenohr..."] ?? '')
  setFieldValue('amplification_contra_ear', input["Diagnose.Höranamnese.Versorgung Gegenohr..."] ?? '')
  setFieldValue('ci_implant_type', input["Behandlung/OP.CI Implantation"] ?? '')
  setFieldValue('pre_measure', input["outcome_measurments.pre.measure."] ?? '')
  setFieldValue('post12_measure', input["outcome_measurments.post12.measure."] ?? '')
  setFieldValue('post24_measure', input["outcome_measurments.post24.measure."] ?? '')
  setFieldValue('interval_days', input["abstand"] ?? '')

  initialSnapshot.value = stableStringify(buildSnapshot(values as Record<string, any>))
}

const onSubmit = handleSubmit(
  async values => {
    try {
      const payload = buildSnapshot(values)
      if (isEdit.value && initialSnapshot.value === stableStringify(payload)) {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: patientId.value}})
        return
      }

      const method = isEdit.value ? 'PUT' : 'POST'
      const url = isEdit.value
        ? `${API_BASE}/api/v1/patients/${encodeURIComponent(patientId.value)}`
        : `${API_BASE}/api/v1/patients/`

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
        body: JSON.stringify({
          input_features: payload.input_features,
          display_name: payload.display_name || undefined,
        }),
      })

      if (!response.ok) {
        const contentType = response.headers.get('content-type') || ''
        let errorMessage = 'Failed to create patient'
        try {
          if (contentType.includes('application/json')) {
            const data = await response.json()
            errorMessage = (data?.detail as string) ?? JSON.stringify(data)
          } else {
            const text = await response.text()
            errorMessage = text || errorMessage
          }
        } catch (e) {
          // fall back to default message
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      if (isEdit.value) {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: patientId.value}, query: {updated: '1'}})
      } else {
        submitAttempted.value = false
        await router.push({name: 'PatientDetail', params: {id: data.id}, query: {created: '1'}})
      }
    } catch (err: any) {
      alert(err?.message ?? i18next.t('form.error.submit_failed'))
    }
  },
  (errors) => {
    allFieldNames.forEach(name => setFieldTouched(name, true, true))
    const messages = normalizeErrors(errors)
    alert(messages.length ? messages.join('\n') : i18next.t('form.error.fix_fields'))
  }
)

const submit = async () => {
  submitAttempted.value = true
  await onSubmit()
}

const onReset = () => {
  submitAttempted.value = false
  handleReset()
}

onMounted(async () => {
  if (!isEdit.value) return
  try {
    const response = await fetch(
      `${API_BASE}/api/v1/patients/${encodeURIComponent(patientId.value)}`,
      {
        method: 'GET',
        headers: {accept: 'application/json'},
      }
    )
    if (!response.ok) throw new Error('Failed to load patient')
    const data = await response.json()
    populateFormForEdit(data)
  } catch (err) {
    console.error(err)
    alert(err instanceof Error ? err.message : 'Failed to load patient')
  }
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

.field-description {
  margin: 4px 0 6px;
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-size: 0.92rem;
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
