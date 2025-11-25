<template>
  <v-container class="home-page py-8 ">
    <h1>Details for the patient No.{{ id }}</h1>
    <v-btn
        class="me-4"
        color="primary"
        variant="flat"
        :to="{ name: 'Prediction', params: { patient_id: id } }"
    >
      generate prediction
    </v-btn>
  </v-container>
</template>

<script lang="ts" setup>
import {useRoute} from 'vue-router'

const route = useRoute()

// Get the id from the URL
const id = route.params.id
</script>

<style scoped>

</style>