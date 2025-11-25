<template>
  <v-container class="home-page py-8 ">

    <!-- SEARCH BAR -->
    <v-row
        :elevation="12"
        align="center"
        border
        class="search-box"
        rounded="lg"
    >
      <v-text-field
          v-model="search"
          :placeholder="$t('search.text')"
          density="comfortable"
          flat
          hide-details
          prepend-inner-icon="mdi-magnify"
          rounded="lg"
          variant="solo"
      />
      <v-btn
          :to="{ name: 'CreatePatient' }"
          color="primary"
          density="comfortable"
          flat
          rounded=6
      >
        {{ $t('search.add_new_patient') }}
      </v-btn>
    </v-row>

    <!-- Results -->

    <v-row
        v-if="filteredList.length > 0"
        :elevation="12"
        align="stretch"
        border
        class="search-box result_list"
        rounded="lg"
    >

      <v-col class="result_list" cols="12">
        <v-list class="result_list">
          <v-list-item
              v-for="item in filteredList"
              :key="item.id"
              :to="{ name: 'PatientDetail', params: { id: item.id } }"
              class="search-result-item"
              prepend-icon="mdi-account-box"
          >
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-col>

    </v-row>

  </v-container>
</template>

<script lang="ts" setup>
import {computed, ref} from "vue";

const search = ref("");
const item_limit = 10

const data = [
  {name: 'Item 1', id: 1},
  {name: 'Item 2', id: 2},
  {name: 'Item 3', id: 3},
  {name: 'Item 4', id: 4},
];

/* Implement bouncing

let isTurn = false;
  if (!isTurn) {

  }
*/

const filteredList = computed(() => {

  if (search.value.length < 1) {
    return []
  } else {
    return data.filter((item) =>
        item.name.toLowerCase().includes(search.value.toLowerCase())
    ).slice(0, item_limit)
  }
});
</script>

<style scoped>
.search-box {
  padding-right: 8px;
  margin: 32px 0 32px 0;
  border-radius: 10px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}

/* LIST container with no padding */
.result_list {
  padding-left: 0 !important;
  margin-left: 0 !important;
  padding-right: 0 !important;
  margin-right: 0 !important;
}

/* each item: spacing + better layout */
.search-result-item {
  padding-left: 20px;
  padding-right: 20px;
  min-height: 72px;
  display: flex;
  align-items: center;
  font-size: 1.25rem;
}

/* lighter primary for hover */
.search-result-item:hover {
  /* very light blue tint */
  background-color: rgba(var(--v-theme-primary), 0.06) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

/* Router-link active state (selected row) */
.search-result-item.v-list-item--active {
  background-color: rgba(var(--v-theme-primary), 0.06) !important;
  color: rgb(var(--v-theme-primary)) !important;
  font-weight: 500;
}

/* icon left spacing fix — compensates for removed padding */
.search-result-item .v-list-item__prepend {
  margin-left: 12px;
  margin-right: 16px;
}

/* optional: make the active icon look like your mockup */
.search-result-item.v-list-item--active .v-icon {
  background-color: rgb(var(--v-theme-primary));
  color: white;
  border-radius: 4px;
  padding: 4px;
}
</style>
