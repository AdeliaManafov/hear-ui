<template>
  <v-container class="new-patient-page">
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
        <!-- First / Last name in one row -->
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="first_name.value.value"
                :counter="20"
                :error-messages="first_name.errorMessage.value"
                :label="$t('form.first_name')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
                v-model="last_name.value.value"
                :counter="20"
                :error-messages="last_name.errorMessage.value"
                :label="$t('form.last_name')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <!-- Email (full width) -->
        <v-row dense>
          <v-col cols="12">
            <v-text-field
                v-model="email.value.value"
                :error-messages="email.errorMessage.value"
                :label="$t('form.email')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <!-- Select (full width for now – like “Auswahl 1/2/3” later) -->
        <v-row dense>
          <v-col cols="12">
            <v-select
                v-model="select.value.value"
                :error-messages="select.errorMessage.value"
                :items="items"
                :label="$t('form.select')"
                color="primary"
                hide-details="auto"
                variant="outlined"
            />
          </v-col>
        </v-row>

        <!-- Checkbox row -->
        <v-row dense>
          <v-col cols="12">
            <v-checkbox
                v-model="checkbox.value.value"
                :error-messages="checkbox.errorMessage.value"
                :label="$t('form.option')"
                color="primary"
                hide-details="auto"
                type="checkbox"
                value="1"
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

  return {
    last_name(value: string) {
      if (value?.length >= 2) return true
      return i18next.t('form.error.name')
    },
    first_name(value: string) {
      if (value?.length >= 2) return true
      return i18next.t('form.error.name')
    },
    email(value: string) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
      return i18next.t('form.error.email')
    },
    select(value: string) {
      if (value) return true
      return i18next.t('form.error.select')
    },
    checkbox(value: string) {
      if (value === '1') return true
      return i18next.t('form.error.checkbox')
    },
  }
})

const {handleSubmit, handleReset} = useForm({
  validationSchema,
})

const last_name = useField('last_name')
const first_name = useField('first_name')
const email = useField('email')
const select = useField('select')
const checkbox = useField('checkbox')

const items = ref([
  'Item 1',
  'Item 2',
  'Item 3',
  'Item 4',
])

const submit = handleSubmit(values => {
  alert(JSON.stringify(values, null, 2))
})
</script>


<style scoped>
.new-patient-page {
  max-width: 960px;
  margin: 0 auto;
}

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
