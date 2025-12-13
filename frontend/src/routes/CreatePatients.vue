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
        <h3 class="section-title">{{ $t('form.sections.general') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="first_name.value.value"
                :error-messages="first_name.errorMessage.value"
                :label="$t('patient_details.fields.first_name')"
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
                :label="$t('patient_details.fields.last_name')"
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
        <h3 class="section-title">{{ $t('form.sections.demographics') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="age.value.value"
                :error-messages="age.errorMessage.value"
                :label="$t('patient_details.fields.age')"
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
                :label="$t('patient_details.fields.gender')"
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
                :label="$t('patient_details.fields.operated_side')"
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
        <h3 class="section-title">{{ $t('form.sections.language') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="primary_language.value.value"
                :error-messages="primary_language.errorMessage.value"
                :label="$t('patient_details.fields.primary_language')"
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
                :label="$t('patient_details.fields.other_languages')"
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
                :label="$t('patient_details.fields.german_language_barrier')"
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
                :label="$t('patient_details.fields.non_verbal')"
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
        <h3 class="section-title">{{ $t('form.sections.family_history') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="parent_hearing_loss.value.value"
                :error-messages="parent_hearing_loss.errorMessage.value"
                :label="$t('patient_details.fields.parent_hearing_loss')"
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
                :label="$t('patient_details.fields.sibling_hearing_loss')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.sibling_hearing_loss')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('form.sections.preop_symptoms') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="tinnitus_preop.value.value"
                :error-messages="tinnitus_preop.errorMessage.value"
                :label="$t('patient_details.fields.tinnitus_preop')"
                color="primary"
                hide-details="auto"
                :true-value="'Vorhanden'"
                :false-value="'Kein'"
                :hint="$t('form.hints.tinnitus_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="vertigo_preop.value.value"
                :error-messages="vertigo_preop.errorMessage.value"
                :label="$t('patient_details.fields.vertigo_preop')"
                color="primary"
                hide-details="auto"
                :true-value="'Vorhanden'"
                :false-value="'Kein'"
                :hint="$t('form.hints.vertigo_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
                v-model="otorrhea_preop.value.value"
                :error-messages="otorrhea_preop.errorMessage.value"
                :label="$t('patient_details.fields.otorrhea_preop')"
                color="primary"
                hide-details="auto"
                :true-value="'Vorhanden'"
                :false-value="'Keine'"
                :hint="$t('form.hints.otorrhea_preop')"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-checkbox
                v-model="headache_preop.value.value"
                :error-messages="headache_preop.errorMessage.value"
                :label="$t('patient_details.fields.headache_preop')"
                color="primary"
                hide-details="auto"
                :true-value="'Vorhanden'"
                :false-value="'Keine'"
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
                :label="$t('patient_details.fields.taste_preop')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.taste_preop')"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('form.sections.imaging') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-checkbox-group
                v-model="imaging_type_preop.value.value"
                :error-messages="imaging_type_preop.errorMessage.value"
                :label="$t('patient_details.fields.imaging_type_preop')"
                color="primary"
                :hint="$t('form.hints.imaging_type_preop')"
                mandatory
                persistent-hint
            >
              <v-row dense>
                <v-col
                    v-for="option in imagingTypeOptions"
                    :key="option.value"
                    cols="12"
                >
                  <v-checkbox
                      :label="option.title"
                      :value="option.value"
                      color="primary"
                      hide-details
                  />
                </v-col>
              </v-row>
            </v-checkbox-group>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="imaging_findings_preop.value.value"
                :error-messages="imaging_findings_preop.errorMessage.value"
                :label="$t('patient_details.fields.imaging_findings_preop')"
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
        <h3 class="section-title">{{ $t('form.sections.objective_measurements') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
                v-model="oae_status.value.value"
                :error-messages="oae_status.errorMessage.value"
                :label="$t('patient_details.fields.objective_oae')"
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
                :label="$t('patient_details.fields.objective_ll')"
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
                :label="$t('patient_details.fields.objective_4k')"
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
        <h3 class="section-title">{{ $t('form.sections.hearing_status') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
                v-model="hl_operated_ear.value.value"
                :error-messages="hl_operated_ear.errorMessage.value"
                :items="hlOperatedOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.hl_operated_ear')"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hl_operated_ear')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="hl_operated_ear.value.value === 'Other'"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="hl_operated_other.value.value"
                :error-messages="hl_operated_other.errorMessage.value"
                :label="$t('patient_details.fields.hl_operated_other')"
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
                :label="$t('patient_details.fields.amplification_operated_ear')"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.amplification_operated_ear')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="amplificationOtherValues.includes(amplification_operated_ear.value.value as string)"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="amplification_operated_other.value.value"
                :error-messages="amplification_operated_other.errorMessage.value"
                :label="$t('patient_details.fields.amplification_operated_other')"
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
                :label="$t('patient_details.fields.hearing_loss_onset')"
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
                :label="$t('patient_details.fields.acquisition_type')"
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
                :label="$t('patient_details.fields.hearing_loss_start')"
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
                :label="$t('patient_details.fields.duration_severe_hl')"
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
                :label="$t('patient_details.fields.etiology')"
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
                :label="$t('patient_details.fields.hearing_disorder_type')"
                required
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.hearing_disorder_type')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="hearingDisorderOtherValues.includes(hearing_disorder_type.value.value as string)"
              cols="12"
              md="4"
          >
            <v-text-field
                v-model="hearing_disorder_other.value.value"
                :error-messages="hearing_disorder_other.errorMessage.value"
                :label="$t('patient_details.fields.hearing_disorder_other')"
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
        <h3 class="section-title">{{ $t('form.sections.hearing_status') }} – {{ $t('patient_details.fields.hl_contra_ear') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
                v-model="hl_contra_ear.value.value"
                :error-messages="hl_contra_ear.errorMessage.value"
                :items="hlContraOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.hl_contra_ear')"
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
                :label="$t('patient_details.fields.amplification_contra_ear')"
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
        <h3 class="section-title">{{ $t('form.sections.treatment_outcome') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
                v-model="ci_implant_type.value.value"
                :error-messages="ci_implant_type.errorMessage.value"
                :items="ciImplantTypeOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.ci_implant_type')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                :hint="$t('form.hints.ci_implant_type')"
                persistent-hint
            />
          </v-col>
          <v-col
              v-if="ci_implant_type.value.value === 'Other'"
              cols="12"
              md="6"
          >
            <v-text-field
                v-model="ci_implant_other.value.value"
                :error-messages="ci_implant_other.errorMessage.value"
                :label="$t('patient_details.fields.ci_implant_other')"
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
                :label="$t('patient_details.fields.pre_measure')"
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
                :label="$t('patient_details.fields.post12_measure')"
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
                :label="$t('patient_details.fields.post24_measure')"
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
                :label="$t('patient_details.fields.interval_days')"
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

          <v-btn
              color="primary"
              variant="outlined"
              @click="onReset"
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
import {API_BASE} from '@/lib/api'

const language = ref(i18next.language)
i18next.on('languageChanged', (lng) => {
  language.value = lng
})

const submitAttempted = ref(false)

const makeLocalizedOptions = (base: Array<{ titleDe: string, titleEn?: string, value: string }>) =>
  computed(() => base.map(o => ({
    title: language.value?.startsWith('de') ? o.titleDe : (o.titleEn ?? o.titleDe),
    value: o.value
  })))

const genderOptions = makeLocalizedOptions([
  {titleDe: 'w – weiblich', titleEn: 'f – female', value: 'w'},
  {titleDe: 'm – männlich', titleEn: 'm – male', value: 'm'},
])

const operatedSideOptions = makeLocalizedOptions([
  {titleDe: 'R – rechtes Ohr', titleEn: 'R – right ear', value: 'R'},
  {titleDe: 'L – linkes Ohr', titleEn: 'L – left ear', value: 'L'},
])

const imagingTypeOptions = makeLocalizedOptions([
  {titleDe: 'CT', titleEn: 'CT', value: 'CT'},
  {titleDe: 'Konventionell', titleEn: 'Conventional', value: 'Konventionell'},
  {titleDe: 'MRT', titleEn: 'MRI', value: 'MRT'},
])

const hlOperatedOptions = makeLocalizedOptions([
  {titleDe: 'Hochgradiger HV', titleEn: 'Severe HL', value: 'Hochgradiger HV'},
  {titleDe: 'Taubheit (Profound HL)', titleEn: 'Profound HL', value: 'Taubheit (Profound HL)'},
  {titleDe: 'Sonstige', titleEn: 'Other', value: 'Other'},
])

const amplificationOperatedOptions = makeLocalizedOptions([
  {titleDe: 'Hörgerät', titleEn: 'Hearing aid', value: 'Hörgerät'},
  {titleDe: 'Keine Versorgung', titleEn: 'No care', value: 'Keine Versorgung'},
  {titleDe: 'Sonstige', titleEn: 'Other', value: 'Sonstige'},
  {titleDe: 'Nicht erhoben', titleEn: 'Not taken', value: 'Nicht erhoben'},
])

const hearingLossOnsetOptions = makeLocalizedOptions([
  {titleDe: 'Congenital', titleEn: 'Congenital', value: 'Congenital'},
  {titleDe: 'Erworben – prälingual', titleEn: 'Acquired – prelingual', value: 'Erworben – prälingual'},
  {titleDe: 'Erworben - perilingual', titleEn: 'Acquired – perilingual', value: 'Erworben - perilingual'},
  {titleDe: 'Erworben - postlingual', titleEn: 'Acquired – postlingual', value: 'Erworben - postlingual'},
  {titleDe: 'Nicht erhoben', titleEn: 'Not taken', value: 'Nicht erhoben'},
  {titleDe: 'Unbekannt', titleEn: 'Unknown', value: 'Unbekannt'},
])

const acquisitionTypeOptions = makeLocalizedOptions([
  {titleDe: 'Progredient', titleEn: 'Progressive', value: 'Progredient'},
  {titleDe: 'Plötzlich', titleEn: 'Sudden', value: 'Plötzlich'},
  {titleDe: 'Unbekannt / nicht erhoben', titleEn: 'Unknown / not taken', value: 'Unbekannt / nicht erhoben'},
])

const hearingLossStartOptions = makeLocalizedOptions([
  {titleDe: '<1y', value: '<1y'},
  {titleDe: '1-2 y', value: '1-2 y'},
  {titleDe: '2-5 y', value: '2-5 y'},
  {titleDe: '5-10 y', value: '5-10 y'},
  {titleDe: '10-20 y', value: '10-20 y'},
  {titleDe: '> 20 y', value: '> 20 y'},
  {titleDe: 'Unbekannt/kA', titleEn: 'Unknown/n.a.', value: 'Unbekannt/kA'},
])

const durationSevereOptions = makeLocalizedOptions([
  {titleDe: '<1y', value: '<1y'},
  {titleDe: '1-2 y', value: '1-2 y'},
  {titleDe: '2-5 y', value: '2-5 y'},
  {titleDe: '5-10 y', value: '5-10 y'},
  {titleDe: '10-20 y', value: '10-20 y'},
  {titleDe: '> 20 y', value: '> 20 y'},
  {titleDe: 'Unbekannt/kA', titleEn: 'Unknown/n.a.', value: 'Unbekannt/kA'},
])

const hearingDisorderTypeOptions = makeLocalizedOptions([
  {titleDe: 'Cochleär', titleEn: 'Cochlear', value: 'Cochleär'},
  {titleDe: 'Sonstige', titleEn: 'Other', value: 'Sonstige'},
  {titleDe: 'Schallleitung', titleEn: 'Conductive', value: 'Schallleitung'},
  {titleDe: 'Nicht erhoben', titleEn: 'Not taken', value: 'Nicht erhoben'},
  {titleDe: 'Andere', titleEn: 'Other (specify)', value: 'Other'},
])

const amplificationOtherValues = ['Sonstige', 'Other']
const hearingDisorderOtherValues = ['Sonstige', 'Other']

const hlContraOptions = makeLocalizedOptions([
  {titleDe: 'Normalhörend', titleEn: 'Normal hearing', value: 'Normalhörend'},
  {titleDe: 'Geringer HV', titleEn: 'Mild HL', value: 'Geringer HV'},
  {titleDe: 'Mässiger HV', titleEn: 'Moderate HL', value: 'Mässiger HV'},
  {titleDe: 'Hochgradiger HV', titleEn: 'Severe HL', value: 'Hochgradiger HV'},
  {titleDe: 'Taubheit (Profound HL)', titleEn: 'Profound HL', value: 'Taubheit (Profound HL)'},
])

const amplificationContraOptions = makeLocalizedOptions([
  {titleDe: 'Hörgerät', titleEn: 'Hearing aid', value: 'Hörgerät'},
  {titleDe: 'CI', titleEn: 'CI', value: 'CI'},
  {titleDe: 'Keine Versorgung', titleEn: 'No care', value: 'Keine Versorgung'},
])

const ciImplantTypeOptions = makeLocalizedOptions([
  {titleDe: 'Cochlear Nucleus Profile Plus CI622 (Slim Straight)', value: 'Cochlear Nucleus Profile Plus CI622 (Slim Straight)'},
  {titleDe: 'Cochlear Nucleus Profile Plus CI612 (Contour Advance)', value: 'Cochlear Nucleus Profile Plus CI612 (Contour Advance)'},
  {titleDe: 'MED-EL Implantattyp / Elektrodentyp', titleEn: 'MED-EL implant type / electrode', value: 'MED-EL Implantattyp / Elektrodentyp'},
  {titleDe: 'Advanced Bionics HiRes Ultra 3D (HiFocus Mid-Scala)', value: 'Advanced Bionics HiRes Ultra 3D (HiFocus Mid-Scala)'},
  {titleDe: 'Cochlear Nucleus Profile CI522 (Slim Straight)', value: 'Cochlear Nucleus Profile CI522 (Slim Straight)'},
  {titleDe: 'Cochlear Nucleus Profile CI532 (Slim Modiolar)', value: 'Cochlear Nucleus Profile CI532 (Slim Modiolar)'},
  {titleDe: 'Cochlear Nucleus Profile CI512 (Contour Advance)', value: 'Cochlear Nucleus Profile CI512 (Contour Advance)'},
  {titleDe: 'Advanced Bionics HiRes Ultra 3D (HiFocus SlimJ)', value: 'Advanced Bionics HiRes Ultra 3D (HiFocus SlimJ)'},
  {titleDe: 'Oticon Medical Neuro Zti EVO', value: 'Oticon Medical Neuro Zti EVO'},
  {titleDe: 'Cochlear Nucleus Profile Plus CI632 (Slim Modiolar)', value: 'Cochlear Nucleus Profile Plus CI632 (Slim Modiolar)'},
  {titleDe: 'Advanced Bionics HiRes Ultra (HiFocus SlimJ)', value: 'Advanced Bionics HiRes Ultra (HiFocus SlimJ)'},
  {titleDe: 'Andere', titleEn: 'Other', value: 'Other'},
])

const tasteOptions = makeLocalizedOptions([
  {titleDe: 'Subjektiv normal', titleEn: 'Subjectively normal', value: 'Subjektiv normal'},
  {titleDe: 'Nicht normal', titleEn: 'Not normal', value: 'Nicht normal'},
  {titleDe: 'Unbekannt/keine Angabe', titleEn: 'Unknown/no answer', value: 'Unbekannt'},
])

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
      if (ctx?.form?.hl_operated_ear === 'Other') {
        return requiredString(value, 'form.error.hl_operated_other')
      }
      return true
    },
    amplification_operated_ear(value: unknown) {
      return requiredString(value, 'form.error.amplification_operated_ear')
    },
    amplification_operated_other(value: unknown, ctx: any) {
      if (amplificationOtherValues.includes(ctx?.form?.amplification_operated_ear)) {
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
      if (hearingDisorderOtherValues.includes(ctx?.form?.hearing_disorder_type)) {
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
    ci_implant_type(value: unknown) {
      return requiredString(value, 'form.error.ci_implant_type')
    },
    ci_implant_other(value: unknown, ctx: any) {
      if (ctx?.form?.ci_implant_type === 'Other') {
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

const {handleSubmit, handleReset, setFieldTouched} = useForm({
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

const buildInputFeatures = (values: Record<string, any>) => {
  const imagingTypes = Array.isArray(values.imaging_type_preop) ? values.imaging_type_preop : []
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
    "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": withDefault(resolveOther(values.hl_operated_ear, values.hl_operated_other, ['Other'])),
    "Diagnose.Höranamnese.Versorgung operiertes Ohr...": withDefault(resolveOther(values.amplification_operated_ear, values.amplification_operated_other, amplificationOtherValues)),
    "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...": withDefault(values.hearing_loss_onset),
    "Diagnose.Höranamnese.Erwerbsart...": withDefault(values.acquisition_type),
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": withDefault(values.hearing_loss_start),
    "Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...": withDefault(values.duration_severe_hl),
    "Diagnose.Höranamnese.Ursache....Ursache...": withDefault(values.etiology),
    "Diagnose.Höranamnese.Art der Hörstörung...": withDefault(resolveOther(values.hearing_disorder_type, values.hearing_disorder_other, hearingDisorderOtherValues)),
    "Diagnose.Höranamnese.Hörminderung Gegenohr...": withDefault(values.hl_contra_ear),
    "Diagnose.Höranamnese.Versorgung Gegenohr...": withDefault(values.amplification_contra_ear),
    "Behandlung/OP.CI Implantation": resolveOther(values.ci_implant_type, values.ci_implant_other, ['Other']),
    "outcome_measurments.pre.measure.": Number(values.pre_measure),
    "outcome_measurments.post12.measure.": Number(values.post12_measure),
    "outcome_measurments.post24.measure.": Number(values.post24_measure),
    "abstand": Number(values.interval_days),
  }
  return input_features
}

const onSubmit = handleSubmit(
  async values => {
    try {
      const displayName = [values.last_name, values.first_name].filter(Boolean).join(", ")
      const payload = {
        input_features: buildInputFeatures(values),
        display_name: displayName || undefined,
      }

      const response = await fetch(`${API_BASE}/api/v1/patients/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(errorText || 'Failed to create patient')
      }

      const data = await response.json()
      alert(i18next.t('form.success.created_with_id', {id: data.id, defaultValue: `Patient created with id: ${data.id}`}))
      submitAttempted.value = false
      handleReset()
    } catch (err: any) {
      alert(err?.message ?? i18next.t('form.error.submit_failed'))
    }
  },
  (errors) => {
    allFieldNames.forEach(name => setFieldTouched(name, true, true))
    const messages = Object.values(errors || {}).flat().filter(Boolean)
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
