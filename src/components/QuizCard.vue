<script setup>
const emit = defineEmits(['delete', 'update', 'start']);
const { quiz, admin } = defineProps(['quiz', 'admin']);
</script>

<template>
  <div class="card bg-secondary mt-2 me-2">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title text-white">{{ quiz.name }}</h5>
      <h6 class="card-subtitle mb-2 text-dark">{{ quiz.chapter }}</h6>
      <hr>
      <p class="card-text text-dark">{{ quiz.remarks }}</p>

      <div v-if="admin" class="row gap-2 p-2">
        <button class="col btn btn-warning" @click.prevent="() => emit('update', quiz)">
          <img src="@/assets/edit.svg" alt="edit quiz" />
        </button>
        <button v-if="admin" class="col btn btn-danger" @click.prevent="() => emit('delete', quiz)">
          <img src="@/assets/remove.svg" alt="remove quiz" />
        </button>
      </div>
      <button @click.prevent="emit('start', quiz.quiz_id)" v-else class="btn btn-primary">
        Start Quiz
      </button>
    </div>
  </div>
</template>