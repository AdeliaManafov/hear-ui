<template>
  <v-container class="new-patient-page">
    <!--
    Project Name and description
    -->

    <!--
    Cards
    -->

    <v-row
        align="center"
        align-content="center"
        justify="center"
    >
      <v-hover>
        <template v-slot:default="{ isHovering, props }">
          <v-card
          :to="{name: 'SearchPatients'}"
          link
          class="home-card"
          variant="outlined"
          color="primary"
      >
        <v-card-title>Title</v-card-title>
        <v-card-subtitle>Subtitle</v-card-subtitle>
        <v-card-text>Text</v-card-text>
      </v-card>
        </template>
      </v-hover>

    </v-row>
  </v-container>
</template>

<script>
</script>

<style scoped>
.new-patient-page {
  max-width: 960px;
  margin: 0 auto;
}

.home-card {
  max-width: 300px;
  margin: 0 auto;
  border-width: 2px;
  border-style: solid;
  box-shadow: 0 0 22px rgba(var(--v-theme-primary), 0.35) !important;
}

</style>