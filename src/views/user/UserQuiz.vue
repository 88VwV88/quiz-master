<script setup>
import QuizCard from '@components/QuizCard.vue'

import { computed } from 'vue'
import { useStore } from 'vuex'
import { RouterLink, useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
await store.dispatch('fetchQuizzes')

const quizzes = computed(() => store.state.quizzes)
const currentUser = computed(() => store.state.currentUser)

async function deleteQuiz(quiz) {
  console.table(quiz)
  await fetch(`http://localhost:5000/quizzes/${quiz.quiz_id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${currentUser.value.token}`,
    },
  })
    .then((response) => response.json())
    .then(() => store.dispatch('fetchQuizzes'))
    .catch(error => console.error(error))
}

async function updateQuiz(quiz) {
  await fetch(`http://localhost:5000/quizzes/${quiz.quiz_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${currentUser.value.token}`,
    },
    body: JSON.stringify(quiz),
  })
    .then(response => response.json())
    .then(() => store.dispatch('fetchQuizzes'))
    .catch(error => console.error(error))
}
function startQuiz(quiz_id) {
  store.commit('startQuiz', quiz_id)
  router.replace(`/quiz/${quiz_id}`)
}
</script>

<template>
  <div>
    <div v-if="currentUser">
      <h1 class="display-6">Available Quizzes</h1>
      <div v-show="quizzes" style="min-height: max(fit-content, 50dvh);">
        <QuizCard v-for="quiz, i in quizzes" v-show="!quiz.done" :quiz="quiz" :key="i" @start="startQuiz" />
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
