import HomeView from '@views/HomeView.vue'
import LoginView from '@views/LoginView.vue'
import RegisterView from '@views/RegisterView.vue'

import DashboardView from '@views/DashboardView.vue'
import UserTakeQuiz from '@views/UserTakeQuiz.vue'

import UserQuizzes from '@views/UserQuizzes.vue'
import AdminSubjects from '@views/AdminSubjects.vue'
import AdminNewQuiz from '@views/AdminNewQuiz.vue'
import AdminNewSubject from '@views/AdminNewSubject.vue'

import { store } from '@/store'
import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'home',
      path: '/',
      component: HomeView,
    },
    {
      name: 'login',
      path: '/login',
      component: LoginView,
    },
    {
      name: 'register',
      path: '/register',
      component: RegisterView,
    },
    {
      path: '/user',
      component: DashboardView,
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.name !== 'login') {
          next({ name: 'login' })
        } else next()
      },
      children: [
        {
          name: 'userQuizzes',
          path: 'quiz',
          component: UserQuizzes,
        },
        {
          name: 'takeQuiz',
          path: 'quiz/:id(\\d+)',
          component: UserTakeQuiz,
        },
      ],
    },
    {
      path: '/admin',
      component: DashboardView,
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.name !== 'login') {
          next({ name: 'login' })
        } else next()
      },
      children: [
        {
          name: 'quiz',
          path: 'quiz',
          component: UserQuizzes,
        },
        {
          name: 'addQuiz',
          path: 'quiz/add',
          component: AdminNewQuiz,
        },
        {
          name: 'subject',
          path: 'subject',
          component: AdminSubjects,
        },
        {
          name: 'addSubject',
          path: 'subject/add',
          component: AdminNewSubject,
        },
      ],
    },
  ],
})
router.beforeEach((_to, _from, next) => {
  document.startViewTransition(next)
})

export default router
