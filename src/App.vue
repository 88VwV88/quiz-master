<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@components/NavBar.vue'
import { KeepAlive } from 'vue';
</script>

<template>
  <NavBar class="bg-dark" />
  <div class="page">
    <KeepAlive>
      <Suspense>
        <RouterView style="view-transition-name: route-view; grid-area: 2 / 2" />
        <template #fallback>
          <div class="text-primary" role="status">
            <span class="display-5">Loading...</span>
          </div>
        </template>
      </Suspense>
    </KeepAlive>
  </div>
</template>

<style>
.page {
  width: 100%;
  height: calc(100%);

  display: grid;
  gap: 1rem;

  align-items: center;
  justify-content: center;

  grid-template-rows: 5dvh 1fr 5dvh;
  grid-template-columns: 12.5dvw 1fr 12.5dvw;

  @media(max-width: 640px) {
    grid-template-rows: 20px 1fr 20px;
    grid-template-columns: 15px 1fr 15px;
  }
}

.v-move,
.v-enter-active,
.v-leave-active {
  transition: 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
