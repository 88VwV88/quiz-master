<script setup>
import { inject } from 'vue'
import { RouterLink } from 'vue-router'

const current_user = inject('current_user')
const links = [
  { url: '/', text: 'Home', forAll: true },
  { url: '/login', text: 'Login', forAll: true },
  { url: '/register', text: 'Register', forAll: true },
  { url: '/quiz', text: 'Quiz', forAll: false },
  { url: '/subject', text: 'Subject', forAll: false },
]

const toRender = ({ forAll }) => {
  if (current_user.value && current_user.value.username !== '') return !forAll
  return forAll
}
</script>

<template>
  <nav class="bg-dark">
    <a href="/" class="ps-4 fs-5 lead">QuizMaster v2</a>
    <div class="space"></div>
    <ul class="justify-content-evenly navbar-links">
      <li v-for="link, i in links.filter(link => toRender(link))" :key="i">
        <RouterLink :to="link.url">{{ link.text }} </RouterLink>
      </li>
      <li v-if="current_user">
        <RouterLink to="/logout" @click.stop.prevent="() => { current_user = null }">
          Logout
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
nav {
  height: 3rem;
  display: flex;
  align-items: center;
  grid-template-columns: 150px auto 15%;

  .space {
    flex-grow: 1;
  }

  ul {
    margin-bottom: 0;
    width: 15rem;
    display: flex;
    justify-content: space-around;
  }
}

a:not(.router-link-active) {
  color: white;
}
</style>
