<script setup>
import { inject, onMounted, ref } from 'vue'

const current_user = inject('current_user')
const subjects = ref([])

onMounted(async () => {
  const current_user = inject('current_user')
  if (current_user.value == null) return

  subjects.value = await fetch('http://localhost:5000/subjects', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`
    }
  }).then(response => response.json()).then(data => data.subjects)
})
</script>

<template>
  <div>
    <h1>Available Subjects:</h1>
    <div v-if="current_user">
      {{ subjects }}
    </div>
  </div>
</template>