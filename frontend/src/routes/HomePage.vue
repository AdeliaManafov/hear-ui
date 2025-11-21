<template>
  <v-container class="py-10">
    <h1>HEAR-UI</h1>
    <p>Homepage</p>

    <v-row class="mt-6" dense>
      <!-- Create patient -->
      <v-col cols="12" sm="6" md="3">
        <v-btn
            block
            color="primary"
            :to="{ name: 'CreatePatient' }"
        >
          Patient:in anlegen
        </v-btn>
      </v-col>

      <!-- Search patients -->
      <v-col cols="12" sm="6" md="3">
        <v-btn
            block
            color="primary"
            variant="outlined"
            :to="{ name: 'SearchPatients' }"
        >
          Patient:innen suchen
        </v-btn>
      </v-col>

      <!-- Make prediction -->
      <v-col cols="12" sm="6" md="3">
        <v-btn
            block
            color="secondary"
            :to="{ name: 'Prediction' }"
        >
          Vorhersage durchführen
        </v-btn>
      </v-col>

      <!-- Back to Home (optional, more useful on other pages) -->
      <v-col cols="12" sm="6" md="3">
        <v-btn
            block
            color="secondary"
            variant="text"
            :to="{ name: 'Home' }"
        >
          Zur Startseite
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
/*
  Vuetify integrates with Vue Router automatically via the `to` prop.
  No extra imports needed here as long as Vuetify & the router plugin
  are registered in main.ts.
*/
</script>

<style scoped>
h1 {
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

p {
  margin-bottom: 1rem;
}
</style>
