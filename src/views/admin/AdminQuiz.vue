<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import QuizCard from '@components/QuizCard.vue';

const store = useStore();
const currentUser = computed(() => store.state.currentUser);
const router = useRouter();

await store.dispatch('fetchQuizzes');
const quizzes = computed(() => store.state.quizzes);

async function deleteQuiz(quiz) {
  await fetch(`http://localhost:5000/quizzes/${quiz.quiz_id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${currentUser.value.token}`,
    },
  })
    .then((response) => response.json())
    .then(() => store.dispatch('fetchQuizzes'))
    .catch((error) => console.error(error));
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
    .then((response) => response.json())
    .then(() => store.dispatch('fetchQuizzes'))
    .catch((error) => console.error(error));
}
</script>

<template>
  <div v-show="currentUser" class="text-center">
    <h1 class="display-6">Active Quizzes</h1>
    <button type="button" class="btn btn-primary ps-3 pe-3 my-3" @click.prevent="router.push('/admin/quiz/add')">
      Add Quiz <img src="@/assets/add.svg" alt="add" />
    </button>
    <div v-show="quizzes" class="p-0 d-flex flex-wrap flex-md-nowrap">
      <QuizCard v-for="(quiz, i) in quizzes.filter(quiz => !(quiz.date_of_quiz > Date.now()))" :key="i" :quiz
        :admin="currentUser.isAdmin" @update="updateQuiz" @delete="deleteQuiz" />
    </div>
    <hr />
    <h1 class="display-6">Past Quizzes</h1>
    <div class="container">
      <QuizCard v-for="(quiz, i) in quizzes.filter(quiz => quiz.date_of_quiz <= Date.now())" :key="i" :quiz
        :admin="currentUser.isAdmin" @delete="deleteQuiz" @update="updateQuiz" />
    </div>
  </div>
</template>