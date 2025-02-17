<script setup>
import { provide, ref } from 'vue'
import { RouterView } from 'vue-router'
import NavBar from '@components/NavBar.vue'

const current_user = ref(null)
provide('current_user', current_user)
</script>

<template>
  <div>
    <NavBar />
    <div class="page mt-5 bg-body-tertiary">
      <Suspense>
        <RouterView style="width: 75dvw" />
        <template #fallback>
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </template>
      </Suspense>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 2rem;
  min-height: calc(100dvh - 6rem);
  display: grid;
  place-items: center;
}
</style>
