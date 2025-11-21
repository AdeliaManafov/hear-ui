<template>
  <v-app id="hear-ui">
    <!-- Navigation Drawer -->
    <v-navigation-drawer
        v-model="drawer"
        class="pt-4"
        color="primary"
        width="260"
    >
      <v-list
          density="comfortable"
          nav
      >
        <v-list-item
            :to="{ name: 'Home' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-home-outline"
            title="Startseite"
        />

        <v-list-item
            :to="{ name: 'SearchPatients' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-magnify"
            title="Patienten suchen"
        />

        <v-list-item
            :to="{ name: 'CreatePatient' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-account-plus"
            title="Neuen Patienten anlegen"
        />

        <v-list-item
            :to="{ name: 'Prediction' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-brain"
            title="Vorhersage durchführen"
        />
      </v-list>
    </v-navigation-drawer>


    <!-- Top App Bar -->
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer"/>
      <v-app-bar-title class="text-white">
        HEAR-UI
      </v-app-bar-title>
    </v-app-bar>

    <!-- Main Content (your router pages render here) -->
    <v-main class="pa-4">
      <router-view/>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import {ref} from "vue"

const drawer = ref(false)
</script>

<style scoped>
.nav-item {
  border-radius: 999px;
  margin-bottom: 8px;
}

/* remove ALL CAPS look from list text */
.nav-item :deep(.v-list-item-title) {
  text-transform: none;
  letter-spacing: 0.02em;
  font-weight: 500;
}
</style>
