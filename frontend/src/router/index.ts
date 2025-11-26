// src/router/index.ts
import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router";
import HomePage from "@/routes/HomePage.vue";
import CreatePatients from "@/routes/CreatePatients.vue";
import SearchPatients from "@/routes/SearchPatients.vue";
import Prediction from "@/routes/Prediction.vue";
import TestSearchTable from "@/routes/TestSearchTable.vue";
import PatientDetail from "@/routes/PatientDetail.vue";
import PredictionsHome from "@/routes/PredictionsHome.vue";

const routes: RouteRecordRaw[] = [
    {
        path: "/",
        redirect: "/home", // when opening the app, go to /home
    },
    {
        path: "/home",
        name: "Home",
        component: HomePage,
    },
    {
        path: "/create-patient",
        name: "CreatePatient", // 👈 route name used in your Vuetify button
        component: CreatePatients, // 👈 matches the actual file CreatePatients.vue
    },
    {
        path: "/search-patients",
        name: "SearchPatients",
        component: SearchPatients,
    },
    {
        path: "/prediction/:patient_id/:patient_name",
        name: "Prediction",
        component: Prediction,
    },
    {
        path: "/prediction-home",
        name: "PredictionsHome",
        component: PredictionsHome,
    },
    {
        path: "/patient-detail/:id",
        name: "PatientDetail",
        component: PatientDetail,
    },
    {
        path: "/test-search-table",
        name: "TestSearchTable",
        component: TestSearchTable,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
