<script setup>
import { RouterView } from "vue-router"
</script>

<template>
  <Suspense>
    <RouterView style="grid-area: 2 / 2" />
    <template #fallback>
      <div class="text-primary" role="status">
        <span class="display-5">Loading...</span>
      </div>
    </template>
  </Suspense>
</template>
