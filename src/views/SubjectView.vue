<script setup>
import { inject, onMounted, ref } from 'vue'
import SubjectCard from '@/components/SubjectCard.vue'
import NewSubjectForm from '@/components/NewSubjectForm.vue';

const current_user = inject('current_user')
const subjects = ref([])

onMounted(async () => {
  if (current_user.value == null) return

  subjects.value = await fetch('http://localhost:5000/subjects', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`
    }
  }).then(response => response.json()).then(data => data.subjects)
})

const refreshSubjects = async () => {
  subjects.value = await fetch('http://localhost:5000/subjects', {
    headers: {
      Authorization: `Bearer ${current_user.value.token}`
    }
  }).then(response => response.json()).then(data => data.subjects)
}
</script>

<template>
  <div v-if="current_user">
    <NewSubjectForm />

    <h1 class="display-5">Available Subjects:</h1>

    <div class="scrollable" style="height: 60dvh;">
      <SubjectCard @refresh-subjects="refreshSubjects" v-for="(subject, i) in subjects" :subjectKey="i" :key="i"
        :subject="subject" />
    </div>

    <button type="button" class="btn btn-primary text-center mt-3" data-bs-toggle="modal"
      data-bs-target="#newSubjectModal">
      <img src="@assets/add.svg" alt="add subject" />
    </button>
  </div>

  <div v-else>
    <p class="display-6">Please log in to view subjects.</p>
    <RouterLink to="/login">Back to log in...</RouterLink>
  </div>
</template>