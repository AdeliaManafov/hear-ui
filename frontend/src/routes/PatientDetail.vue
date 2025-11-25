<template>
  <v-container class="home-page py-8 ">
    <h1>Details for the patient No.{{ id }}</h1>
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