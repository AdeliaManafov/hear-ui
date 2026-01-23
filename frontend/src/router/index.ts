// src/router/index.ts
import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router";
import HomePage from "@/routes/HomePage.vue";
import CreatePatients from "@/routes/CreatePatients.vue";
import SearchPatients from "@/routes/SearchPatients.vue";
import Prediction from "@/routes/Prediction.vue";
import PatientDetails from "@/routes/PatientDetails.vue";
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
        name: "CreatePatient",
        component: CreatePatients,
    },
    {
        path: "/search-patients",
        name: "SearchPatients",
        component: SearchPatients,
    },
    {
        path: "/prediction/:patient_id",
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
        component: PatientDetails,
    },
    {
        path: "/patient-detail/:id/edit",
        name: "UpdatePatient",
        component: CreatePatients,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
