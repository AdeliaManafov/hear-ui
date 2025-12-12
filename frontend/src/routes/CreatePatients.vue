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
                hint="Patient given name"
                persistent-hint
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
                hint="Patient family name"
                persistent-hint
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
                hint="Patient's age"
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
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Gender (w/m)"
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
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Ear operated on"
                persistent-hint
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
                hint="Patients primary language"
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
                hint="Patients secondary language"
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
                hint="Whether patient can speak good German."
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
                hint="Whether patient speaks or uses sign-language."
                persistent-hint
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
                hint="Patients parents have a hearing impairment"
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
                hint="Patients siblings have a hearing impairment"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.preop_symptoms') }}</h3>
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
                hint="Whether patient has tinnitus as a preoperative symptom"
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
                hint="Whether patient has dizziness as a preoperative symptom"
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
                hint="Whether patient suffers from ear discharge as a preoperative symptom"
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
                hint="Whether patient has headache as a preoperative symptom"
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
                hint="Taste (subjective assessment)"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">Imaging</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-checkbox-group
                v-model="imaging_type_preop.value.value"
                :error-messages="imaging_type_preop.errorMessage.value"
                label="Imaging type (pre-op)"
                color="primary"
                hint="Select all imaging modalities done preoperatively"
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
                label="Imaging findings (pre-op)"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="CT/MRT findings"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">Objective measurements</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
                v-model="oae_status.value.value"
                :error-messages="oae_status.errorMessage.value"
                :items="oaeStatusOptions"
                item-title="title"
                item-value="value"
                label="OAE status"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Otoacoustic emissions measurement"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="ll_status.value.value"
                :error-messages="ll_status.errorMessage.value"
                :items="llStatusOptions"
                item-title="title"
                item-value="value"
                label="LL status"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Loudness level measurement"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="hz4k_status.value.value"
                :error-messages="hz4k_status.errorMessage.value"
                :items="hz4kStatusOptions"
                item-title="title"
                item-value="value"
                label="4 kHz status"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="4 kHz objective measurement"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.hearing_status') }}</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
                v-model="hl_operated_ear.value.value"
                :error-messages="hl_operated_ear.errorMessage.value"
                :items="hlOperatedOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.hl_operated_ear')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Type of hearing loss in the ear to be operated on"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="amplification_operated_ear.value.value"
                :error-messages="amplification_operated_ear.errorMessage.value"
                :items="amplificationOperatedOptions"
                item-title="title"
                item-value="value"
                label="Amplification operated ear"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Type of care performed on the ear to be operated on"
                persistent-hint
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                v-model="hearing_loss_onset.value.value"
                :error-messages="hearing_loss_onset.errorMessage.value"
                :items="hearingLossOnsetOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.hearing_loss_onset')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="When did the hearing loss occur"
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
                label="Acquisition type"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="How did the patient acquire the hearing loss"
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
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="When did the hearing impairment begin"
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
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="How long has the patient had severe HL or deafness"
                persistent-hint
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
                hint="Cause of hearing loss"
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
                label="Hearing disorder type"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Type of hearing disorder"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.hearing_status') }} – {{ $t('patient_details.fields.hl_contra_ear') }}</h3>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
                v-model="hl_contra_ear.value.value"
                :error-messages="hl_contra_ear.errorMessage.value"
                :items="hlContraOptions"
                item-title="title"
                item-value="value"
                :label="$t('patient_details.fields.hl_contra_ear')"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Hearing loss in the other ear"
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
                label="Amplification contralateral ear"
                color="primary"
                hide-details="auto"
                variant="outlined"
                hint="Type of care performed on the opposite ear"
                persistent-hint
            />
          </v-col>
        </v-row>

        <v-divider class="my-4"/>
        <h3 class="section-title">{{ $t('patient_details.sections.treatment_outcome') }}</h3>
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
                hint="Cochlear implant surgery (treatment info)"
                persistent-hint
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
                hint="Freiburger test measurement pre-operation"
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
                hint="Freiburger measurement 12 months post-operation"
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
                hint="Freiburger measurement 24 months post-operation"
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
                hint="Number of days between pre-op measure and operation date"
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

const llStatusOptions = makeLocalizedOptions([
  {titleDe: 'Keine Reizantwort', titleEn: 'No response', value: 'Keine Reizantwort'},
  {titleDe: 'Schwelle', titleEn: 'Threshold', value: 'Schwelle'},
  {titleDe: 'Nicht erhoben', titleEn: 'Not taken', value: 'Nicht erhoben'},
])

const oaeStatusOptions = llStatusOptions

const hz4kStatusOptions = llStatusOptions

const hlOperatedOptions = makeLocalizedOptions([
  {titleDe: 'Hochgradiger HV', titleEn: 'Severe HL', value: 'Hochgradiger HV'},
  {titleDe: 'Taubheit (Profound HL)', titleEn: 'Profound HL', value: 'Taubheit (Profound HL)'},
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
])

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
      return !!(value);
    },
    operated_side(value: unknown) {
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
      if (Array.isArray(value) && value.length > 0) return true
      return requiredString(value as string, 'form.error.imaging_type_preop')
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
      return !!(value);
    },
    etiology(value: unknown) {
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
