<script setup>
import NewQuizForm from '@/components/NewQuizForm.vue'
import QuizCard from '@/components/QuizCard.vue'
import { ref, inject, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const quizzes = ref([])
const current_user = inject('current_user')

if (current_user.value != null) {
  const response = await fetch('http://127.0.0.1:5000/quizzes', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  });
  if (!response.ok) {
    const { message } = await response.json();
    console.warn(`[ERROR: ${response.status}] ${message}!`)
  }
  quizzes.value = await response.json().then((data) => data.quizzes);
}

async function refresh() {
  quizzes.value = (await fetch('http://127.0.0.1:5000/quizzes', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  }).then((response) => current_user.value ? response.json() : { quizzes: [] })).quizzes
}

async function deleteQuiz(quiz) {
  const response = await fetch(`http://localhost:5000/quizzes/${quiz.quiz_id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  }).then((response) => response.json())

  if (!response.ok)
    throw new Error('Failed to delete quiz!')

  console.warn(response.message)
  refresh()
}

async function updateQuiz(quiz) {
  const response = await fetch(`http://localhost:5000/quizzes/${quiz.quiz_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify(quiz),
  })
    .then(response => response.json())
    .error(error => console.error(error))

  console.log(response.message)
  refresh()
}
</script>

<template>
  <div v-if="!current_user">
    <p class="display-6">Failed to fetch quizzes!</p>
    <RouterLink to="/login">Go back to login...</RouterLink>
  </div>

  <div v-else-if="!current_user.isAdmin">
    <h1 class="display-6">Available Quizzes</h1>

    <div v-if="quizzes" style="min-height: max(fit-content, 50dvh);">
      <QuizCard v-for="quiz, i in quizzes" :quiz="quiz" :key="i" :admin="current_user.isAdmin" />
    </div>
  </div>

  <div v-else>
    <h1 class="display-6">Active Quizzes</h1>

    <button type="button" class="btn btn-primary ps-3 pe-3 my-3" data-bs-toggle="modal" data-bs-target="#newQuizModal">
      Add Quiz <img src="@/assets/add.svg" alt="add" />
    </button>

    <div class="scrollable">
      <QuizCard v-for="(quiz, i) in quizzes.filter(q => !(q.date_of_quiz > Date.now()))" :key="i" :quiz="quiz"
        :admin="current_user.isAdmin" @delete="deleteQuiz" />
    </div>

    <NewQuizForm @refresh.stop="refresh" :quizzes="quizzes" />

    <hr />

    <h1 class="display-6">Past Quizzes</h1>

    <div class="scrollable">
      <QuizCard v-for="(quiz, i) in quizzes.filter(q => q.date_of_quiz <= Date.now())" :key="i" :quiz="quiz"
        :admin="current_user.isAdmin" @delete.stop="deleteQuiz" @update.stop="updateQuiz" />
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
