<script setup>
import { inject } from 'vue'

const current_user = inject('current_user')
const emit = defineEmits(['refresh'])
const { subject, subjectKey } = defineProps(['subject', 'subjectKey'])

const deleteSubject = async () => {
  const response = await fetch(`http://localhost:5000/subjects/${subject.subject_id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${current_user.value.token}`,
    },
  }).then((response) => response.json());

  console.log(response.message);
  emit('refresh');
};

const editSubject = async () => {
  const response = await fetch(`http://localhost:5000/subjects/${subject.subject_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify(subject),
  }).then((response) => response.json());

  console.log(response.message);
  emit('refresh');
};
</script>

<template>
  <div class="bg-gradient-dark rounded p-3 card mt-3">
    <h4 class="lead">{{ subject.name }}</h4>

    <p class="text-muted">{{ subject.description }}</p>

    <div class="row px-2 gap-2">
      <button v-if="current_user.isAdmin" class="col btn btn-warning" @click=editSubject>
        <img src="@assets/edit.svg" alt="delete subject">
      </button>
      <button v-if="current_user.isAdmin" class="col btn btn-danger" @click=deleteSubject>
        <img src="@assets/remove.svg" alt="delete subject">
      </button>
    </div>

    <hr>

    <div class="accordion accordion-flush" :id="`subject${subjectKey}-chapters`">
      <div class="accordion-item" v-for="(chapter, i) in subject.chapters" :key="i">
        <h2 class="accordion-header">
          <button class="accordion-button text-muted fs-6 lead" data-bs-toggle="collapse" type="button"
            :data-bs-target="`#subject${subjectKey}-chapter${i}`" :id="`header-${i}`">
            {{ chapter.name }}
          </button>
        </h2>

        <div class="accordion-body" :data-bs-parent="`#subject${subjectKey}-chapter`">
          <div :id="`subject${subjectKey}-chapter${i}`" class="accordion-collapse collapse">
            {{ chapter.description }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.accordion-button {
  background-color: transparent;
}

.accordion-body {
  padding: 0;

  .accordion-collapse {
    padding-block: 1rem;
  }
}
</style>