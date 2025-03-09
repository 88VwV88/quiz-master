<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import ScrollWatcher from '@components/ScrollWatcher.vue'

const store = useStore()
const router = useRouter()
const currentUser = computed(() => store.state.currentUser)

const { links } = defineProps(['links'])

function logout() {
  store.commit('logoutUser')
  router.push('/login')
}
</script>

<template>
  <header>
    <nav class="bg-dark fixed-top">
      <span @click.prevent="() => { router.push(''); }" class="route-link ps-4 fs-5 lead">
        QuizMaster v2
      </span>
      <div class="space"></div>
      <ul class="justify-content-evenly navbar-links">
        <li v-for="link, i in links" :key="i">
          <span class="route-link" @click.prevent="() => router.push(link.url)">{{
            link.name
          }}
          </span>
        </li>
        <li v-show="!!currentUser">
          <span class="route-link" @click.prevent="logout">Logout</span>
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

span.route-link {
  cursor: pointer;
}
</style>
