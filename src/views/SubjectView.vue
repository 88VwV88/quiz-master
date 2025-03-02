<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import SubjectCard from '@components/SubjectCard.vue'

const store = useStore()
await store.dispatch('fetchSubjects')
const router = useRouter();

const currentUser = computed(() => store.state.currentUser)
const subjects = computed(() => store.state.subjects)
function transition(task) {
  document.startViewTransition(task)
}
</script>

<template>
  <div v-if="currentUser">
    <h1 class="display-5">Available Subjects</h1>

    <div v-show="currentUser.isAdmin">
      <button type="button" class="btn btn-primary ps-3 pe-3 text-center mt-3"
        @click.prevent="transition(() => router.push('/subject/add'))">
        Add Subject <img src="@assets/add.svg" alt="add subject" />
      </button>
    </div>

    <div class="d-flex p-0 flex-wrap flex-md-nowrap justify-content-start" style="height: 60dvh;">
      <SubjectCard @refresh="() => store.dispatch('fetchSubjects')" v-for="(subject, i) in subjects" :subjectKey="i"
        :key="i" :subject="subject" />
    </div>
  </div>

  <div v-else>
    <p class="display-6">Please log in to view subjects</p>
    <RouterLink to="/login">Back to log in...</RouterLink>
  </div>
</template>