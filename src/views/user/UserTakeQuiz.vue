<script setup>
import { computed, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'

const store = useStore()
const router = useRouter()

const currentUser = computed(() => store.state.currentUser)
const quiz = computed(() =>
  store.state.quizzes.find(quiz =>
    quiz.quiz_id === store.state.activeQuiz))

const currentQuestion = ref(0)
const selectedOption = ref(-1)

const selected = reactive({})

function nextQuestion() {
  if (selectedOption.value !== -1) {
    selected[currentQuestion.value] = selectedOption
    ++currentQuestion.value
  }
}
function submitAnswers() {
  fetch('http://localhost:5000/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${currentUser.value.token}`,
    },
    body: JSON.stringify({
      selected
    })
  }).then(() => router.push('/quiz'))
}
</script>

<template>
  <div>
    <h1 class="display-2 text-center">{{ quiz.name }}</h1>
    <div class="quiz">
      <div class="question" v-for="(question, i) in quiz.questions" :key="i" v-show="currentQuestion === i">
        <p class="question__statement lead fs-4">{{ question.statement }}</p>
        <div class="question__options">
          <div class="question__option" v-for="(option, j) in question.options" :key="j">
            <input class="question__optioninput btn-check" :checked="j === selectedOption"
              :id="`question${i}-option${j}`" autocomplete="off" />
            <label class="question__optionlabel btn btn-outline-primary" @click.stop.prevent="selectedOption = j"
              :for="`question${i}-option${j}`">{{
                option
              }}</label>
          </div>
          <button class="btn btn-success" @click.prevent.stop="nextQuestion">Next</button>
        </div>
      </div>
      <button v-show="currentQuestion === quiz.questions.length" class="quiz__submit btn btn-success"
        style="grid-area: 2 / 2" @click="submitAnswers">Submit</button>
    </div>
  </div>
</template>

<style scoped>
.quiz {
  display: grid;
  grid-template-columns: 10px 1fr 10px;
  grid-template-rows: 10px 1fr 10px;
}

.question {
  grid-area: 2 / 2;

  .question__options {
    display: grid;
    grid-template-rows: repeat(4, 1fr);
    gap: 10px;

    .question__option {
      .question__optioninput[checked]~.question__optionlabel {
        background-color: var(--bs-primary);
      }

      .question__optionlabel {
        width: 100%;
        color: var(--bs-primary-text);
      }
    }
  }
}
</style>