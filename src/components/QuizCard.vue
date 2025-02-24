<script setup>
const { quiz, admin } = defineProps(['quiz', 'admin']);
const { deleteQuiz } = defineEmits(['deleteQuiz']);
</script>

<template>
  <div class="card mt-2">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ quiz.name }}</h5>
      <h6 class="card-subtitle mb-2 text-muted">{{ quiz.chapter }}</h6>
      <hr>
      <p class="card-text">{{ quiz.remarks }}</p>

      <div v-if="admin" class="row gap-2 p-2">
        <button class="col btn btn-warning" @click.prevent.stop="() => deleteQuiz(quiz)">
          <img src="@/assets/edit.svg" alt="edit quiz" />
        </button>
        <button v-if="admin" class="col btn btn-danger" @click.prevent.stop="() => deleteQuiz(quiz)">
          <img src="@/assets/remove.svg" alt="remove quiz" />
        </button>
      </div>
      <button v-else class="btn btn-primary">
        start quiz
      </button>
    </div>
  </div>
</template>