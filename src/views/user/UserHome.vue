<script setup>
import QuizCard from '@components/QuizCard.vue'

import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
await store.dispatch('fetchQuizzes')

const quizzes = computed(() => store.state.quizzes);
const currentUser = computed(() => store.state.currentUser);

function onStart(quiz_id) {
  store.commit('startQuiz', quiz_id);
  router.replace(`/user/quiz/take/${quiz_id}`);
}
function onView(quiz_id) {
  router.replace(`/user/quiz/${quiz_id}`);
}
</script>

<template>
  <div>
    <div v-if="currentUser">
      <h1 class="display-6 text-center">Upcomming Quizzes</h1>
      <hr />
      <div v-show="quizzes" class="container-md">
        <QuizCard v-for="(quiz, key) in quizzes" v-show="!quiz.done" :quiz="quiz" :key @view="() => onView(key)"
          @start="onStart" />
      </div>
    </div>
  </div>
</template>

<style>
ul {
  padding: 0;
  list-style: none;
}

button.btn {
  img {
    width: 1.25rem;
  }
}
</style>
