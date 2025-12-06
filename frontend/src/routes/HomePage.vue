<template>
  <v-container class="home-page py-8">
    <!-- Project name + description -->
    <v-row
        align="start"
        class="mb-4"
        justify="space-between"
    >
      <!-- Left: Text -->
      <v-col
          class="text-left text-md-left mb-4 mb-md-0"
          cols="12"
          md="7"
      >
        <h1 class="text-h4 font-weight-bold mb-1">
          {{ $t('homepage.title') }}
        </h1>
        <h2 class="text-h6 text-primary mb-2">
          {{ $t('homepage.subtitle') }}
        </h2>
        <p class="text-body-1 text-medium-emphasis mb-0">
          {{ $t('homepage.description') }}
        </p>
      </v-col>

      <!-- Right: Image -->
      <v-col
          class="d-flex justify-center justify-md-end"
          cols="12"
          md="5"
      >
        <v-img
            alt="HEAR-UI illustration"
            class="img-hero"
            contain
            max-width="300"
            src="assets/images/hero.png"
        />
      </v-col>
    </v-row>
    <v-divider
        class="my-6 home-divider"
    />

    <!-- Cards -->
    <v-row
        align="stretch"
        justify="center"
    >
      <!-- Search Patients -->
      <v-col class="pa-3" cols="12" md="4" sm="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
              :to="{ name: 'SearchPatients' }"
              class="home-card"
              color="primary"
              link
              v-bind="props"
              variant="outlined"
          >
            <v-img
                :alt="$t('homepage.search_patients_image_alt')"
                class="home-card-image"
                cover
                height="160"
                placeholder="assets/images/logo_black.png"
                src="assets/images/search.png"
            ></v-img>

            <v-col class="home-card-titles">
              <v-card-title>
                {{ $t('homepage.search_patients_title') }}
              </v-card-title>
              <v-card-subtitle>
                {{ $t('homepage.search_patients_subtitle') }}
              </v-card-subtitle>
            </v-col>

            <v-card-text>
              {{ $t('homepage.search_patients_text') }}
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>

      <!-- Create Patient -->
      <v-col class="pa-3" cols="12" md="4" sm="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
              :to="{ name: 'CreatePatient' }"
              class="home-card"
              color="primary"
              link
              v-bind="props"
              variant="outlined"
          >
            <v-img
                :alt="$t('homepage.create_patient_image_alt')"
                class="home-card-image"
                cover
                height="160"
                placeholder="assets/images/logo_black.png"
                src="assets/images/add_patient.png"
            ></v-img>

            <v-col class="home-card-titles">
              <v-card-title>
                {{ $t('homepage.create_patient_title') }}
              </v-card-title>
              <v-card-subtitle>
                {{ $t('homepage.create_patient_subtitle') }}
              </v-card-subtitle>
            </v-col>

            <v-card-text>
              {{ $t('homepage.create_patient_text') }}
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>

      <!-- Predictions -->
      <v-col class="pa-3" cols="12" md="4" sm="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
              :to="{ name: 'PredictionsHome' }"
              class="home-card"
              color="primary"
              link
              v-bind="props"
              variant="outlined"
          >
            <v-img
                :alt="$t('homepage.prediction_image_alt')"
                class="home-card-image"
                cover
                height="160"
                placeholder="assets/images/logo_black.png"
                src="assets/images/prediction.png"

            ></v-img>

            <v-col class="home-card-titles">
              <v-card-title>
                {{ $t('homepage.prediction_title') }}
              </v-card-title>
              <v-card-subtitle>
                {{ $t('homepage.prediction_subtitle') }}
              </v-card-subtitle>
            </v-col>

            <v-card-text>
              {{ $t('homepage.prediction_text') }}
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-page {
  max-width: 960px;
  margin: 0 auto;
}

/* Card base */
.home-card {
  height: 100%;
  border-width: 2px;
  border-style: solid;
  box-shadow: 0 0 22px rgba(var(--v-theme-primary), 0.25) !important;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

/* Optional styling for the image */
.home-card-image {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

/* Hover effect (works with v-hover + Vuetify hover styles) */
.home-card:hover,
.home-card.v-card--hover {
  box-shadow: 0 6px 28px rgba(var(--v-theme-primary), 0.45) !important;
  transform: translateY(-3px);
}

.home-divider {
  margin: 12px 0 48px 0 !important;
}

.img-hero {
  border-radius: 1%;
}

.home-card .v-card-subtitle {
  white-space: normal !important;
}

.home-card .v-card-title {
  white-space: normal !important;
  padding-bottom: 4px !important;
}

.home-card-titles {
  margin: 0 !important;
  padding: 0 !important;
  gap: 0 !important;
}

</style>
