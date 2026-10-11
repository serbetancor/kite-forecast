import { createRouter, createWebHistory } from "vue-router"

import ForecastPage from "../pages/ForecastPage.vue"
import ScorePage from "../pages/ScorePage.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "forecast",
      component: ForecastPage,
    },
    {
      path: "/ranking",
      name: "ranking",
      component: ScorePage,
    },
  ],
})

export default router
