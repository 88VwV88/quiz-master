<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { RouterView } from 'vue-router'
import NavBar from '@components/NavBar.vue'

const store = useStore()
const currentUser = computed(() => store.state.currentUser)

const links = computed(() => !currentUser.value ?
  [
    { name: 'Home', path: '/' },
    { name: 'Login', path: '/login' },
    { name: 'Register', path: '/register' },
  ] : currentUser.value.isAdmin ?
    [
      { name: "Home", path: "" },
      { name: "Quiz", path: "quiz" },
      { name: "Summary", path: "summary" },
    ] : [
      { name: "Home", path: "" },
      { name: "Quiz", path: "quiz" },
    ])
</script>

<template>
  <NavBar :links class="bg-dark" />
  <KeepAlive>
    <div class="page">
      <RouterView style="view-transition-name: route-view; grid-area: 2 / 2" />
    </div>
  </KeepAlive>
</template>