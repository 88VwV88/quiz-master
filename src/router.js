import HomeView from '@views/HomeView.vue'
import LoginView from '@views/LoginView.vue'
import QuizView from '@views/QuizView.vue'
import RegisterView from '@views/RegisterView.vue'
import SubjectView from '@views/SubjectView.vue'

import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomeView,
    },
    {
      path: '/login',
      component: LoginView,
    },
    {
      path: '/register',
      component: RegisterView,
    },
    {
      path: '/quiz',
      component: QuizView,
    },
    {
      path: '/subject',
      component: SubjectView,
    },
    {
      path: '/subject/:id',
      component: SubjectView,
    },
    {
      path: '/logout',
      redirect: (_) => {
        fetch('http://localhost:5000/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        }).then((response) => response.json())

        return { path: '/login' }
      },
    },
  ],
})

export default router
