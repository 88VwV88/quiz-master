import Home from '@views/HomeView.vue'
import Login from '@views/LoginView.vue'
import Quiz from '@views/QuizView.vue'
import Register from '@views/RegisterView.vue'

import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Home,
    },
    {
      path: '/login',
      component: Login,
    },
    {
      path: '/register',
      component: Register,
    },
    {
      path: '/quiz',
      component: Quiz,
    },
    {
      path: '/logout',
      redirect: (to) => {
        fetch('http://localhost:5000/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        }).then((res) => res.json())

        return { path: '/login' }
      },
    },
  ],
})

export default router
