<template>
  <v-container>
  <v-btn
      variant="tonal"
      prepend-icon="mdi-arrow-left"
      :to="{name : 'SearchPatients'}"
      size="small"
      color="primary"
  >
  {{$t('form.back')}}
  </v-btn>
  <h1>{{$t('form.title')}}</h1>
  <form @submit.prevent="submit">
    <v-text-field
      v-model="last_name.value.value"
      :counter="10"
      :error-messages="last_name.errorMessage.value"
      :label="$t('form.last_name')"
      class="field"
    ></v-text-field>

    <v-text-field
      v-model="first_name.value.value"
      :counter="10"
      :error-messages="first_name.errorMessage.value"
      :label="$t('form.first_name')"
    ></v-text-field>

    <v-text-field
      v-model="email.value.value"
      :error-messages="email.errorMessage.value"
      label="E-mail"
    ></v-text-field>

    <v-select
      v-model="select.value.value"
      :error-messages="select.errorMessage.value"
      :items="items"
      label="Select"
    ></v-select>

    <v-checkbox
      v-model="checkbox.value.value"
      :error-messages="checkbox.errorMessage.value"
      label="Option"
      type="checkbox"
      value="1"
    ></v-checkbox>

    <v-btn
  class="me-4"
  type="submit"
  color="primary"
>
  {{ $t('form.submit') }}
</v-btn>


    <v-btn
  @click="handleReset"
  variant="outlined"
  color="primary"
>
  {{ $t('form.reset') }}
</v-btn>

  </form>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import { useField, useForm } from 'vee-validate'

  const { handleSubmit, handleReset } = useForm({
    validationSchema: {
      last_name (value) {
        if (value?.length >= 2) return true
        return $t('form.error.name')
      },
      first_name (value) {
        if (value?.length >= 2) return true
        return $t('form.error.name')
      },
      email (value) {
        if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true

        return $t('form.error.email')
      },
      select (value) {
        if (value) return true

        return $t('form.error.select')
      },
      checkbox (value) {
        if (value === '1') return true

        return $t('form.error.checkbox')
      },
    },
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
.form_field{
  color: primary;

}
</style>