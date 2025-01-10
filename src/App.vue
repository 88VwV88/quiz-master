<script setup>
import { RouterView } from 'vue-router';
import NavBar from '@components/NavBar.vue';
const links = [
  { url: '/', text: 'Home' },
  { url: '/login', text: 'Login' },
  { url: '/quiz', text: 'Quiz' },
];
</script>

<template>
  <div>
    <NavBar :links="links" />
    <Suspense>
      <RouterView />
      <template #fallback>
        <p>Loading...</p>
      </template>
    </Suspense>
  </div>
</template>