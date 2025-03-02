<script setup>
import { computed } from 'vue'
import ScrollWatcher from '@components/ScrollWatcher.vue'
import { useStore } from 'vuex'
import router from '@/router'

const store = useStore()
const currentUser = computed(() => store.state.currentUser)

const links = [
  { url: '/', text: 'Home', forAll: true },
  { url: '/login', text: 'Login', forAll: true },
  { url: '/register', text: 'Register', forAll: true },
  { url: '/quiz', text: 'Quiz', forAll: false },
  { url: '/subject', text: 'Subject', forAll: false },
  { url: '/profile', text: 'Profile', forAll: false }
]

function toRender({ forAll }) {
  if (currentUser.value && currentUser.value.username !== 'admin') return !forAll
  return forAll
}
function transition(task) {
  document.startViewTransition(() => task())
}
function logout() {
  store.commit('logoutUser')
  router.push('/login')
}
</script>

<template>
  <header>
    <nav class="bg-dark fixed-top">
      <span @click.prevent="() => transition(() => router.push('/'))" class="route-link ps-4 fs-5 lead">QuizMaster
        v2</span>
      <div class="space"></div>
      <ul class="justify-content-evenly navbar-links">
        <li v-for="link, i in links.filter(link => toRender(link))" :key="i">
          <span class="route-link" @click.prevent="() => transition(() => router.push(link.url))">{{
            link.text
            }}
          </span>
        </li>
        <li v-show="currentUser">
          <span class="route-link" @click.prevent="() => transition(() => logout())">Logout</span>
        </li>
      </ul>
      <ScrollWatcher />
    </nav>
  </header>
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

span.router-link.active {
  color: var(--bs-primary);
}

span.route-link {
  cursor: pointer;
}
</style>
