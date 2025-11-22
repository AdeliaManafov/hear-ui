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
          class="drawer-list"
      >
        <v-list-item
            :to="{ name: 'Home' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-home-outline"
            :title="$t('navbar_homepage')"
        />

        <v-list-item
            :to="{ name: 'SearchPatients' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-magnify"
            :title="$t('navbar_search_patients')"
        />

        <v-list-item
            :to="{ name: 'CreatePatient' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-account-plus"
            :title="$t('navbar_create_patient')"
        />

        <v-list-item
            :to="{ name: 'Prediction' }"
            class="text-white text-body-1 nav-item"
            prepend-icon="mdi-trending-up"
            :title="$t('navbar_predictions')"
        />
      </v-list>
    </v-navigation-drawer>


    <!-- Top App Bar -->
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer"/>
      <v-app-bar-title class="text-white">
        HEAR-UI
      </v-app-bar-title>
      <v-btn variant="outlined"
             density="comfortable"
             size="large"
             rounded="xs"
             class="language-button"
             @click="switch_language"
      >
      {{languages[curr_language]}}
      </v-btn>
    </v-app-bar>

    <!-- Main Content (your router pages render here) -->
    <v-main class="pa-4">
      <router-view/>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import {onMounted, ref} from "vue"
import i18next from "i18next";
const drawer = ref(false)
const curr_language = ref(0)
const languages = ref(["de", "en"])


function switch_language() {
  curr_language.value++
  curr_language.value = curr_language.value % languages.value.length
  i18next.changeLanguage(languages.value[curr_language.value])
}

onMounted(() => {
  languages.value = Object.keys(i18next.options.resources!)
})

</script>

<style scoped>
.nav-item {
  border-radius: 0 999px 999px 0;
  margin-bottom: 8px;
}

/* remove ALL CAPS look from list text */
.nav-item :deep(.v-list-item-title) {
  text-transform: none;
  letter-spacing: 0.02em;
  font-weight: 500;
}

.nav-item :deep(.v-list-item__prepend) {
  padding-left: 20px !important;   /* padding BEFORE the icon */
}

.drawer-list {
  padding-left: 0 !important;
  padding-right: 16px !important;
}

.language-button{
  margin-right:16px !important;
}
</style>
