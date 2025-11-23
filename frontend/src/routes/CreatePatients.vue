<template>
  <v-container class="new-patient-page">
    <v-sheet
        border
        class="new-patient-card"
        rounded="0"
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

      <h1>{{ $t('form.title') }}</h1>

      <form class="new-patient-form" @submit.prevent="submit">
        <!-- First / Last name in one row -->
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
                v-model="first_name.value.value"
                :counter="10"
                :error-messages="first_name.errorMessage.value"
                :label="$t('form.first_name')"
                hide-details="auto"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
                v-model="last_name.value.value"
                :counter="10"
                :error-messages="last_name.errorMessage.value"
                :label="$t('form.last_name')"
                hide-details="auto"
            />
          </v-col>
        </v-row>

        <!-- Email (full width) -->
        <v-row dense>
          <v-col cols="12">
            <v-text-field
                v-model="email.value.value"
                :error-messages="email.errorMessage.value"
                hide-details="auto"
                :label="$t('form.email')"
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
                hide-details="auto"
                :label="$t('form.select')"
            />
          </v-col>
        </v-row>

        <!-- Checkbox row -->
        <v-row dense>
          <v-col cols="12">
            <v-checkbox
                v-model="checkbox.value.value"
                :error-messages="checkbox.errorMessage.value"
                hide-details="auto"
                :label="$t('form.option')"
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


<script setup lang="ts">
import { ref, computed } from 'vue'
import { useField, useForm } from 'vee-validate'
import i18next from 'i18next'

const language = ref(i18next.language)
i18next.on('languageChanged', (lng) => {
  language.value = lng
})

const validationSchema = computed(() => {
  const lang = language.value
  return {
    last_name (value) {
      if (value?.length >= 2) return true
      return i18next.t('form.error.name')
    },
    first_name (value) {
      if (value?.length >= 2) return true
      return i18next.t('form.error.name')
    },
    email (value) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
      return i18next.t('form.error.email')
    },
    select (value) {
      if (value) return true
      return i18next.t('form.error.select')
    },
    checkbox (value) {
      if (value === '1') return true
      return i18next.t('form.error.checkbox')
    },
  }
})

const { handleSubmit, handleReset } = useForm({
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
  border-width: 1px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
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
