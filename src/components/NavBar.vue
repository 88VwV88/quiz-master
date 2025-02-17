<script setup>
import { inject } from 'vue'
import { RouterLink } from 'vue-router'

const current_user = inject('current_user')
const links = [
  { url: '/', text: 'Home', forAll: true },
  { url: '/login', text: 'Login', forAll: true },
  { url: '/register', text: 'Register', forAll: true },
  { url: '/quiz', text: 'Quiz', forAll: false },
  { url: '/logout', text: 'Logout', forAll: false },
]

const toRender = ({ forAll }) => {
  if (current_user.value && current_user.value.username !== '') return !forAll
  return forAll
}
</script>

<template>
  <nav class="bg-body-tertiary d-flex h-5">
    <a href="/" class="ps-4 fs-4">QuizMaster v2</a>
    <ul class="navbar-links">
      <li v-for="link in links" class="me-4 pt-2" :key="link.text">
        <RouterLink :to="link.url" v-if="toRender(link)">{{ link.text }} </RouterLink>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
nav {
  display: grid;
  justify-content: space-between;
  align-items: center;
  grid-template-columns: 1fr 1fr;
}

a:not(.router-link-active) {
  color: white;
}

.navbar-links {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}
</style>
