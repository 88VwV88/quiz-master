import Home from "@views/Home.vue";
import Login from "@views/Login.vue";
import Quiz from "@views/Quiz.vue";
import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: Home,
    },
    {
      path: "/login",
      component: Login,
    },
    {
      path: "/quiz",
      component: Quiz,
    }
  ],
});

export default router;
