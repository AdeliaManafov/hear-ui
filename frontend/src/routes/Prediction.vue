<template>
  <v-container class="py-8">
    <v-sheet
        :elevation="12"
        border
        class="prediction-sheet"
        rounded="lg"
    >
      <!-- Title -->
      <v-row justify="start" no-gutters>
        <h1>
          {{ $t('prediction.title') }}
          <span class="text-primary">{{ patient_name }}</span>
        </h1>

      </v-row>
      <v-divider
          class="my-6"
      />

      <!-- Results -->
      <v-row
          justify="start"
          align="center"
          no-gutters
      >
        <!-- Result -->
        <v-col cols="7">
          <h3>{{ $t('prediction.result.title') }}</h3>
          <h1 class="prediction-value">{{ (prediction.result * 100).toFixed(0) }}%</h1>
          <p>{{ $t('prediction.result.probability') }}</p>

          <v-divider
              class="my-2"
          />

          <div
              class="prediction-status"
              :class="recommended ? 'status-success' : 'status-error'"
          >
            {{
              recommended
                  ? $t('prediction.result.status.recommended')
                  : $t('prediction.result.status.not_recommended')
            }}
          </div>


          <p>
            {{
              recommended
                  ? $t('prediction.result.description.recommended')
                  : $t('prediction.result.description.not_recommended')
            }}
          </p>

        </v-col>

        <!-- Graph -->
        <v-col class="graph-col" cols="5">
          <v-sheet class="graph-sheet" rounded="lg">
            <!-- Title -->
            <h4 class="graph-title">
              {{ $t('prediction.result.graph.title') }}
            </h4>

            <v-sheet class="graph-canvas" rounded="lg" elevation="0">
              <!-- GRAPH AREA -->
              <div class="graph-placeholder graph-placeholder-relative" :style="{'--patient-x-position': patientX + '%'}">
                <svg
                    class="graph-svg"
                    viewBox="0 33.33 100 66.67"
                >
                  <!-- curved “probability” line -->
                  <path
                      class="graph-curve"
                      :d="graphPath"
                  />

                  <!-- vertical dotted line at patient % -->
                  <line
                      class="graph-patient-line"
                      :x1="patientX"
                      y1="0"
                      :x2="patientX"
                      y2="100"
                  />

                  <!-- blue patient dot -->
                  <circle
                      class="graph-patient-dot"
                      :cx="patientX"
                      :cy="patientY"
                      r="1.5"
                  />
                </svg>

                <!-- top-right label: 'Patient: 87%' -->
                <div class="graph-patient-label" :class="recommended ? 'label-left' : 'label-right'">
                  {{ $t('prediction.result.graph.patient') }} {{ patientPercent }}%
                </div>
              </div>


              <!-- X-axis -->
              <div class="graph-x-axis"></div>
              <div class="graph-scale">
                <span>0</span>
                <span>100</span>
              </div>
            </v-sheet>


            <!-- Caption -->
            <p class="graph-caption">
              {{ $t('prediction.result.graph.description') }}
            </p>
          </v-sheet>
        </v-col>


      </v-row>
      <v-divider
          class="my-6"
      />

    </v-sheet>
  </v-container>
</template>

<script lang="ts" setup>
import {useRoute} from 'vue-router'
import {computed} from 'vue'

const route = useRoute()

const patient_id = route.params.patient_id
const patient_name = route.params.patient_name

// TODO: add an API call for the prediction
const prediction = {
  patient_id: patient_id,
  result: 0.7,
  params: {
    param1: -0.53,
    param2: 0.82,
    param3: -0.85,
    param4: -0.35,
    param5: 0.34,
    param6: 0.22,
  }
}
const recommended = prediction.result > 0.5

const GRAPH_SCALE_FACTOR = 200 // Larger number = flatter curve
const MAX_Y_COORD = 96 // Max Y coordinate in SVG viewBox

// 0–100 %
const patientPercent = computed(() => Math.round(prediction.result * 100))

// x coordinate in SVG (viewBox width = 100)
const patientX = computed(() => patientPercent.value)

const patientY = computed(() => {
  const x = patientX.value
  return MAX_Y_COORD - (x * x / GRAPH_SCALE_FACTOR)
})

const graphPath = computed(() => {
  let path = `M 0 ${MAX_Y_COORD}`;
  for (let x = 1; x <= 100; x += 5) {
    const y = MAX_Y_COORD - (x * x / GRAPH_SCALE_FACTOR);
    path += ` L ${x},${y}`;
  }
  return path;
})
</script>

<style scoped>
.prediction-sheet {
  padding: 32px;
  border-width: 2px;
  border-style: solid;
  border-color: rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 4px 22px rgba(var(--v-theme-primary), 0.35) !important;
}

.prediction-value {
  font-size: 56px;
  font-weight: 700;
  line-height: 1;
  margin: 12px 12px 16px 12px;
}

.prediction-status {
  display: inline-block;
  font-size: 14px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 6px;
  margin: 8px 0 8px 0;
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Green badge */
.status-success {
  background-color: rgb(var(--v-theme-success));
  color: white;
}

/* Red badge */
.status-error {
  background-color: rgb(var(--v-theme-error));
  color: white;
}

.graph-col {
  display: flex;
  justify-content: flex-end; /* align to the right like in Figma */
}

/* Outer square card */
.graph-sheet {
  border: 1px solid #000; /* black border */
  border-radius: 12px; /* rounded corners */
  padding: 16px;
  width: 100%;
  max-width: 360px; /* tweak to match your layout */
  aspect-ratio: 1 / 1; /* keep it roughly square */
  display: flex;
  flex-direction: column;
}

/* h4-style title */
.graph-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

/* Inner sheet where the graph will be drawn */
.graph-canvas {
  flex: 1;
  margin-bottom: 12px;
}

/* Caption text under the graph */
.graph-caption {
  font-size: 14px;
  line-height: 1.4;
  margin: 0;
}

/* Graph drawing area (empty for now) */
.graph-placeholder {
  flex: 1;
  width: 100%;
  margin-bottom: 12px;
}

/* Thin horizontal gray axis line */
.graph-x-axis {
  width: 100%;
  height: 1px;
  background-color: #d0d0d0; /* light gray like in mockup */
  margin-bottom: 4px;
}

/* 0 --- 100 aligned left/right */
.graph-scale {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 12px;
  color: #666;
  padding: 0 2px;
  margin-bottom: 4px;
}


/* SVG fills area */
.graph-svg {
  width: 100%;
  height: 100%;
}

/* MAIN CURVE – this was missing, so it got filled black */
.graph-curve {
  fill: none;           /* 🔥 prevent black wedge */
  stroke: #000;
  stroke-width: 0.7;
}

/* vertical dotted line at patient value */
.graph-patient-line {
  stroke: #bdbdbd;
  stroke-width: 0.4;
  stroke-dasharray: 1.5 1.5;
}

/* blue dot */
.graph-patient-dot {
  fill: rgb(var(--v-theme-primary));
}

/* 'Patient: 87%' label */
.graph-patient-label {
  position: absolute;
  top: 2px;
  font-size: 12px;
  color: #000;
}

.label-left {
  left: var(--patient-x-position);
  transform: translateX(-110%); /* shift left by 110% of its own width */
}

.label-right {
  left: var(--patient-x-position);
  transform: translateX(10%); /* shift right by 10% of its own width */
}

.graph-placeholder-relative {
  position: relative;
}

/* axis + scale */
.graph-x-axis {
  width: 100%;
  height: 1px;
  background-color: #d0d0d0;
  margin-bottom: 4px;
}

.graph-scale {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 12px;
  color: #666;
  padding: 0 2px;
  margin-bottom: 4px;
}



</style>