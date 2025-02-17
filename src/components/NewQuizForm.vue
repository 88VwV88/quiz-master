<script setup>
import { ref, reactive, inject } from 'vue'

const questions = reactive([])
const doq = ref(new Date(Date.now()))
const current_user = inject('current_user')

const emit = defineEmits(['refreshQuizzes'])

const newQuiz = reactive({
  name: '',
  remarks: '',
  subject: '',
  chapter: '',
  duration: 0,
})

const getCookies = (name) => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

const handleSubmit = async () => {
  if (current_user == null) throw new Error('Failed to submit quiz!')
  doq.value = new Date(doq.value)

  const response = await fetch('http://127.0.0.1:5000/quizzes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-TOKEN': getCookies('csrf_access_token'),
      Authorization: `Bearer ${current_user.value.token}`,
    },
    body: JSON.stringify({
      ...newQuiz,
      date_of_quiz: doq.value != null ?
        `${doq.value.getFullYear()}-${doq.value.getMonth()}-${doq.value.getDate()}`
        : 'null',
      questions,
    }),
  })

  if (!response.ok) {
    const { message } = await response.json();
    console.warn(`[ERROR: ${response.status}] ${message}!`)
  }
  emit('refreshQuizzes')
};

const addQuestion = () => {
  const options = []
  for (let i = 0; i < 4; ++i) options.push({ statement: '' })
  questions.push({
    statement: '',
    options: options,
    answer: 0,
  })
}

const removeQuestion = (index) => {
  while (index-- > 0) questions.push(questions.shift())
  questions.shift()
}

const getType = (attr) => attr === 'duration' ? 'number' : 'text';
</script>

<template>
  <form @submit.prevent.stop="handleSubmit">
    <div v-for="attr in Object.keys(newQuiz)" class="form-floating text-start my-2" :key="attr">
      <!-- if attr is remarks -->
      <textarea v-model="newQuiz[attr]" v-if="attr === 'remarks'" :id="attr" class="form-control" />
      <!-- else -->
      <input v-else v-model="newQuiz[attr]" :type="getType(attr)" :id="attr" class="form-control" />
      <label :for="attr">{{ attr }}</label>
    </div>
    <div class="form-floating my-2">
      <input v-model="doq" type="date" id="doq" class="form-control" />
      <label for="doq">Date of Quiz</label>
    </div>
    <p class="text-start">Questions:</p>
    <button @click.prevent.stop="addQuestion" class="btn btn-secondary">+</button>
    <ul>
      <li v-for="(ques, i) in questions" :key="i">
        <div>
          <div class="form-floating my-2">
            <textarea v-model="ques.statement" :id="`question-${i}-statement`" class="form-control" />
            <label :for="`question-${i}-statement`">Question {{ i + 1 }} Statement</label>
          </div>
          <ul>
            <li v-for="(opt, j) in ques.options" :key="j" class="form-floating mt-2">
              <textarea v-model="opt.statement" :id="`opt-${i}-${j}`" class="form-control" />
              <label :for="`opt-${i}-${j}`">{{ j + 1 }}.</label>
            </li>
          </ul>
          <div class="form-floating mt-4">
            <input type="number" v-model="ques.answer" id="answer" class="form-control" />
            <label for="answer">answer [1-4]</label>
          </div>
        </div>
        <button @click.prevent.stop="() => removeQuestion(i)" class="btn btn-secondary my-2">-</button>
      </li>
    </ul>
    <button class="btn btn-primary" type="submit" popovertargetaction="hide">add quiz</button>
  </form>
</template>
