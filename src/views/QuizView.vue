<script setup>
import NewQuizForm from '@/components/NewQuizForm.vue'
import QuizCard from '@/components/QuizCard.vue'
import { ref, inject, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const quizzes = ref([])
const current_user = inject('current_user')

onMounted(async () => {
  if (current_user.value == null) return
  const response = await fetch('http://127.0.0.1:5000/quizzes', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  });
  console.log(response.ok);
  if (!response.ok) {
    const { message } = await response.json();
    console.warn(`[ERROR: ${response.status}] ${message}!`)
  }
  quizzes.value = await response.json().then((data) => data.quizzes);
  console.log(quizzes.value);
});

const refreshQuizzes = async () => {
  quizzes.value = (await fetch('http://127.0.0.1:5000/quizzes', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  }).then((response) => current_user.value ? response.json() : { quizzes: [] })).quizzes
}

const deleteQuiz = async (quiz) => {
  const response = await fetch(`http://localhost:5000/quizzes`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify({ quiz_id: quiz.id }),
  }).then((response) => response.json())
  console.log(response.message)
  await refreshQuizzes()
}
</script>

<template>
  <div v-if="!current_user">
    <h1>Failed to fetch quizzes!</h1>
    <RouterLink to="/login">Go back to login...</RouterLink>
  </div>
  <div v-else-if="!current_user.isAdmin">
    <h1>Available Quizzes</h1>
    <!-- Quizzes  -->
    <div v-if="quizzes">
      <QuizCard v-for="q in quizzes" :title="q.title" :remarks="q.remarks" :questions="q.questions" :key="q.title" />
    </div>
  </div>
  <div v-else>
    <h1>Active Quizzes</h1>
    <button popovertarget="new-quiz-popover" class="btn btn-secondary my-3">+New Quiz</button>
    <div v-for="(q, i) in quizzes.filter(quiz => quiz.date_of_quiz < Date.now())" :key="i">
      {{ q }}
    </div>
    <div id="new-quiz-popover" popover>
      <button class="close-btn btn btn-danger" popovertarget="new-quiz-popover" popovertargetaction="hide">X</button>
      <NewQuizForm @refresh-quizzes="refreshQuizzes" :quizzes="quizzes" />
    </div>
    <hr />
    <h1>Past Quizzes</h1>
    <div v-for="(q, i) in quizzes.filter(quiz => !(quiz.date_of_quiz < Date.now()))" :key="i">
      <div class="card mt-2">
        <div class="card-body">
          <h5 class="card-title">{{ q.name }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ q.chapter }}</h6>
          <p class="card-text">{{ q.remarks }}</p>
          <button class="btn btn-danger" @click="() => deleteQuiz(q)">delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
#new-quiz-popover {
  height: 80dvh;
  width: 80dvw;
  border-radius: 16px;
  justify-self: center;
  align-self: center;
  text-align: center;
  padding: 2rem;
  border: none;
  border-radius: 1.5rem;
  scrollbar-width: thin;
  scroll-behavior: smooth;
  justify-items: center;

  .btn-secondary {
    width: 3rem;
    height: 3rem;
    padding: none;
    margin: none;
    align-self: center;
    font-size: 1.5rem;
  }
}

ul {
  padding: 0;
  list-style: none;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
}
</style>
