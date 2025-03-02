<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore()

const currentUser = computed(() => store.state.currentUser)
await store.dispatch('fetchScores')

const scores = computed(() => store.state.scores)
</script>

<template>
  <div>
    {{ currentUser.name }}
    {{ scores }}
  </div>
</template>