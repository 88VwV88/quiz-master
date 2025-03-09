<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore()

const currentUser = computed(() => store.state.currentUser)
const quizzes = computed(() => store.state.quizzes)

console.log(quizzes.value)

await store.dispatch('fetchScores')
const scores = computed(() => store.state.scores)
</script>

<template>
  <div class="row">
    <div class="col-2 rounded bg-primary p-4 text-center">
      {{ currentUser.username }}
    </div>
    <div class="col-auto">
      <span>previous quizzes:</span>
      <li v-for="(i, quiz) in quizzes.filter(quiz => quiz.done)" :key="i">
        {{ quiz.title }}
      </li>
      <span>scores:</span>
      <li v-for="(i, score) in scores" :key="i">
        {{ score.score }}
      </li>
    </div>
  </div>
</template>