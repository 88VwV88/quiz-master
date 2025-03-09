<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const currentUser = computed(() => store.state.currentUser)

const quiz = ref({
  name: '',
  remarks: '',
  subject: '',
  chapter: '',
  date_of_quiz: new Date().toISOString().split('T')[0],
})
const questions = ref([])

async function submit() {
  if (currentUser.value == null) throw new Error('failed to submit quiz!')

  const response = await fetch('http://127.0.0.1:5000/quizzes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${currentUser.value.token}`,
    },
    body: JSON.stringify({
      ...quiz.value,
      questions: questions.value,
    }),
  })
    .then(response => response.json())
    .catch(error => console.error(error))

  console.log(response.message)

  quiz.value = {
    name: null,
    remarks: null,
    subject: '',
    chapter: '',
    duration: 0,
  }

  questions.value = []
  store.dispatch('fetchQuizzes')
};

function addQuestion() {
  const options = []

  for (let i = 0; i < 4; ++i)
    options.push({ statement: '' })

  questions.value.push({
    statement: '',
    options: options,
    answer: 0,
  })
}

function removeQuestion(index) {
  questions.value.splice(index, 1);
}

function getType(attr) {
  return attr === 'date_of_quiz' ? 'date' : 'text';
}
</script>

<template>
  <div class="vw-25">
    <h4 class="display-4 text-center">Add New Quiz</h4>
    <form @submit.prevent.stop="submit" class="container-md">
      <div v-for="attr in Object.keys(quiz)" class="form-floating text-start my-2" :key="attr">
        <textarea v-model="quiz[attr]" v-if="attr === 'remarks'" :id="attr" class="form-control" autocomplete="off" />

        <input v-else v-model="quiz[attr]" :type="getType(attr)" :id="attr" class="form-control" autocomplete="off" />

        <label :for="attr">{{ attr.split('_').join(' ') }}</label>
      </div>
      <div class="bg-dark p-4 rounded mt-3">
        <p class="text-start">Questions:</p>
        <ul class="d-flex flex-column align-items-center">
          <li v-for="(ques, i) in questions" :key="i" class="d-flex flex-column w-100">
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

            <button @click.prevent="() => removeQuestion(i)"
              class="btn btn-danger align-self-center fs-5 my-2">-</button>
          </li>
          <button @click.prevent="addQuestion" class="btn btn-primary align-self-center mt-2 fs-5">+</button>
        </ul>

        <input type="submit" class="btn btn-success w-100 mt-2" value="add quiz" />
      </div>
    </form>
  </div>
</template>

<style scoped>
.btn-danger,
.btn-primary {
  width: 10rem;
}
</style>