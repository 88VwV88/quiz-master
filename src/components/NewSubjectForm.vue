<script setup>
import { inject, reactive } from 'vue'

const current_user = inject('current_user')
const chapters = reactive([])
const subject = reactive({
  name: '',
  description: '',
})

const addChapter = () => {
  chapters.push({
    name: '',
    description: '',
  })
}
const removeChapter = (index) => chapters.splice(index, 1)
const handleSubmit = async () => {
  const response = await fetch('http://localhost:5000/subjects', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify({
      ...subject,
      chapters,
    }),
  })

  if (!response.ok)
    console.warn(`[ERROR: ${response.status}] Failed to add subject!`)
}
</script>

<template>
  <div class="modal fade" id="newSubjectModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title lead">Add new subject</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form>
            <div v-for="attr in Object.keys(subject)" class="form-floating text-start my-2" :key="attr">
              <!-- if attr is remarks -->
              <textarea rows="10" cols="30" v-model="subject[attr]" v-if="attr === 'description'" :id="attr"
                class="form-control" />
              <!-- else -->
              <input v-else v-model="subject[attr]" type="text" :id="attr" class="form-control" />
              <label :for="attr">{{ attr }}</label>
            </div>
            <p class="text-start">Chapters:</p>
            <button @click.prevent.stop="addChapter" class="btn btn-secondary fs-5">+</button>
            <ul>
              <li v-for="(chapter, i) in chapters" :key="i" class="d-flex flex-column">
                <div>
                  <div class="form-floating my-2" v-for="attr in Object.keys(chapter)" :key="attr">
                    <textarea v-if="attr === 'description'" v-model="chapter[attr]" :id="`chapter-${i}-${attr}`"
                      class="form-control" />
                    <input v-else v-model="chapter[attr]" type="text" :id="`chapter-${i}-${attr}`"
                      class="form-control" />
                    <label :for="`chapter-${i}-name`">Chapter {{ i + 1 }} {{ attr }}</label>
                  </div>
                </div>
                <button @click.prevent.stop="() => removeChapter(i)" class="btn btn-secondary fs-5 my-2">-</button>
              </li>
            </ul>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">close</button>
          <button type="button" class="btn btn-primary" @click.prevent.stop="handleSubmit">add subject</button>
        </div>
      </div>
    </div>
  </div>
</template>