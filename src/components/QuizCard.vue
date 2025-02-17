<script setup>
const { title, remarks, questions } = defineProps(['title', 'remarks', 'questions']);
</script>

<template>
  <div class="jumbotron d-flex flex-column mb-3 py-2" :key="title">
    <h1 class="display-4">{{ title }}</h1>
    <p class="lead">{{ remarks }}</p>
    <hr class="my-4" />
    <p>{{ questions.length }} questions</p>
    <button class="btn btn-primary">start quiz</button>
  </div>
</template>
