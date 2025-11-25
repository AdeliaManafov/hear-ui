<template>
  <v-container class="home-page py-8 ">
    <h1>Prediction for the patient No.{{ patient_id }}</h1>
  </v-container>
</template>

<script lang="ts" setup>
import {useRoute} from 'vue-router'

const route = useRoute()

// Get the id from the URL
const patient_id = route.params.patient_id
</script>

<style scoped>

</style>