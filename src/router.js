import HomeView from '@views/HomeView.vue'
import QuizView from '@views/QuizView.vue'
import LoginView from '@views/LoginView.vue'
import ProfileView from '@views/ProfileView.vue'
import SubjectView from '@views/SubjectView.vue'
import RegisterView from '@views/RegisterView.vue'
import ActiveQuizView from '@views/ActiveQuizView.vue'
import NewSubjectView from '@views/NewSubjectView.vue'

import { store } from '@/store'
import { createRouter, createWebHistory } from 'vue-router'
import NewQuizView from './views/NewQuizView.vue'

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
      path: '/quiz/:id(\\d+)',
      component: ActiveQuizView,
      beforeEnter(_to, _from, next) {
        if (!store.state.authenticated) {
          next({ path: '/login' })
        } else next()
      },
    },
    {
      path: '/quiz',
      component: QuizView,
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.path !== '/login') {
          next({ path: '/login' })
        } else next()
      },
    },
    {
      path: '/quiz/add',
      component: NewQuizView,
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.path !== '/login') {
          next({ path: '/login' })
        } else next()
      },
    },
    {
      path: '/subject',
      component: SubjectView,
      beforeEnter(_to, _from, next) {
        if (!store.state.authenticated) {
          next({ path: '/login' })
        } else next()
      },
    },
    {
      path: '/subject/add',
      component: NewSubjectView,
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.path !== '/login') {
          next({ path: '/login' })
        } else next()
      },
    },
    {
      path: '/profile',
      component: ProfileView,
      beforeEnter(_to, _from, next) {
        if (!store.state.authenticated) {
          next({ path: '/login' })
        } else next()
      },
    },
  ],
})

export default router
