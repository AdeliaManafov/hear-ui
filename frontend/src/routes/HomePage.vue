<template>
  <v-container>
    <v-row>
      <template v-for="n in 4" :key="n">
        <v-col
            class="mt-2"
            cols="12"
        >
          <strong>Category {{ n }}</strong>
        </v-col>
        <v-col
            v-for="j in 6"
            :key="`${n}${j}`"
            cols="6"
            md="2"
        >
          <v-sheet
              color="secondary"
              height="150"
          ></v-sheet>
        </v-col>
      </template>
    </v-row>
  </v-container>
</template>

<script>
</script>