<script setup>
import { ref, inject } from 'vue'

const current_user = inject('current_user')

const emit = defineEmits(['refresh'])

const quiz = ref({
  name: '',
  remarks: '',
  subject: '',
  chapter: '',
  duration: 0,
  date_of_quiz: new Date().toISOString().split('T')[0],
})
const questions = ref([])

async function submit() {
  if (current_user == null) throw new Error('Failed to submit quiz!')

  const response = await fetch('http://127.0.0.1:5000/quizzes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify({
      ...quiz.value,
      questions: questions.value,
    }),
  })
    .then(response => response.json())
    .error(error => console.error(error))

  console.log(response.message)

  quiz.value = {
    name: '',
    remarks: '',
    subject: '',
    chapter: '',
    duration: 0,
  }
  questions.value = []
  emit('refresh')
};

const addQuestion = () => {
  const options = []
  for (let i = 0; i < 4; ++i) options.push({ statement: '' })
  questions.value.push({
    statement: '',
    options: options,
    answer: 0,
  })
}

const removeQuestion = (index) => questions.value.splice(index, 1)

const getType = (attr) => attr === 'date_of_quiz' ? 'date' : attr === 'duration' ? 'number' : 'text';
</script>

<template>
  <div class="modal fade" id="newQuizModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title lead">Add new quiz</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form>
            <div v-for="attr in Object.keys(quiz)" class="form-floating text-start my-2" :key="attr">
              <textarea rows="5" cols="30" v-model="quiz[attr]" v-if="attr === 'remarks'" :id="attr"
                class="form-control" autocomplete="off" />

              <input v-else v-model="quiz[attr]" :type="getType(attr)" :id="attr" class="form-control"
                autocomplete="off" />

              <label :for="attr">{{ attr.split('_').join(' ') }}</label>
            </div>

            <p class="text-start">Questions:</p>

            <button @click.prevent.stop="addQuestion" class="btn btn-secondary fs-5">+</button>

            <ul>
              <li v-for="(ques, i) in questions" :key="i" class="d-flex flex-column">
                <div>
                  <div class="form-floating my-2">
                    <textarea v-model="ques.statement" :id="`question-${i}-statement`" class="form-control"
                      autocomplete="off" />
                    <label :for="`question-${i}-statement`">Question {{ i + 1 }} Statement</label>
                  </div>

                  <ul>
                    <li v-for="(opt, j) in ques.options" :key="j" class="form-floating mt-2">
                      <textarea rows="5" cols="30" v-model="opt.statement" :id="`opt-${i}-${j}`" class="form-control"
                        autocomplete="off" />
                      <label :for="`opt-${i}-${j}`">{{ j + 1 }}.</label>
                    </li>
                  </ul>

                  <div class="form-floating mt-4">
                    <input type="number" v-model="ques.answer" id="answer" class="form-control" autocomplete="off" />
                    <label for="answer">answer [1-4]</label>
                  </div>
                </div>

                <button @click.prevent.stop="() => removeQuestion(i)" class="btn btn-secondary fs-5 my-2">-</button>
              </li>
            </ul>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">close</button>
          <button type="button" class="btn btn-primary" @click.prevent.stop="submit">add quiz</button>
        </div>
      </div>
    </div>
  </div>
</template>
