<script setup>
import { provide, ref } from 'vue'
import { RouterView } from 'vue-router'
import NavBar from '@components/NavBar.vue'

const current_user = ref(null);
provide('current_user', current_user);
</script>

<template>
  <NavBar class="bg-dark" />

  <div class="page">
    <Suspense>
      <RouterView style="grid-column: 2; grid-row: 2;" />

      <template #fallback>
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </template>
    </Suspense>
  </div>
</template>

<style scoped>
.page {
  width: 100%;
  height: calc(100% - 3rem);

  display: grid;
  gap: 1rem;

  align-items: center;
  justify-content: center;

  grid-template-rows: 40px 1fr 40px;
  grid-template-columns: 30px 1fr 30px;
}
</style>
