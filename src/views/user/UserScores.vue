<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
await store.dispatch('fetchScores');

const scores = computed(() => store.state.scores);
</script>

<template>
  <div class="container">
    <h1 class="display-4 text-center">User Scores:</h1>
    <hr />
    <div v-if="scores.length !== 0" class="p-2 bg-dark rounded">
      <div v-for="(score, key) in scores" :key>
        {{ score }}
      </div>
    </div>
    <div v-else class="lead bg-dark rounded p-2 text-center">No scores available</div>
  </div>
</template>