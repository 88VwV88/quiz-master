<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();

const currentUser = computed(() => store.state.currentUser);
const quiz = computed(() =>
  store.state.quizzes.find((quiz) => quiz.quiz_id === store.state.activeQuiz),
);

const qCount = ref(0); // question count
const cQues = ref(quiz.value.questions.at(0).id); // current question
const sOpt = ref(-1); // selected option
const ques = computed(() => quiz.value.questions);
console.log("timer set for:", quiz.value.hh * 3600 + quiz.value.mm * 60, "s");

const timer = ref(
  setTimeout(
    () => {
      alert("Time is up!");
      onSubmit();
    },
    (quiz.value.hh * 3600 + quiz.value.mm * 60) * 1000,
  ),
);

const hours = ref(quiz.value.hh);
const minutes = ref(quiz.value.mm);
setInterval(() => {
  if (hours.value > 0 && minutes.value === 0) {
    --hours.value;
    minutes.value = 59;
  } else {
    --minutes.value;
  }
}, 1000);

const selected = reactive({});

function onNext() {
  if (sOpt.value !== -1) {
    ++qCount.value;
    selected[cQues.value] = sOpt.value;
    if (qCount.value < ques.value.length)
      cQues.value = ques.value[qCount.value].id;
    else cQues.value = -1;
    sOpt.value = -1;
  }
}

async function onSubmit() {
  try {
    if (timer.value != null) clearTimeout(timer.value);

    await fetch("http://localhost:5000/submit", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        quiz_id: quiz.value.quiz_id,
        selected,
      }),
    });

    store.commit("clearQuiz");
    router.push("/user");
  } catch (error) {
    console.error("[ERROR] submitting answers:", error);
  } finally {
    sOpt.value = -1;
  }
}
</script>

<template>
  <div v-if="quiz" class="container-md">
    <p class="lead">{{ hours }}:{{ minutes }}</p>
    <p class="lead bg-dark rounded d-inline p-2" v-if="qCount < ques.length">
      {{ qCount + 1 }}/{{ ques.length }}
    </p>
    <h1 class="display-2 text-center">{{ quiz.name }}</h1>
    <div class="quiz">
      <div
        class="question"
        v-for="question in ques"
        :key="question.id"
        v-show="cQues === question.id"
      >
        <p class="question__statement lead fs-4">{{ question.statement }}</p>
        <div class="question__options">
          <div
            class="question__option"
            v-for="option in question.options"
            :key="option.id"
          >
            <input
              class="question__optioninput btn-check"
              :checked="option.id === sOpt"
              :id="`question${question.id}-option${option.id}`"
              autocomplete="off"
            />
            <label
              class="question__optionlabel btn btn-outline-primary"
              @click.prevent="sOpt = option.id"
              :for="`question${question.id}-option${option.id}`"
            >
              {{ option.statement }}
            </label>
          </div>
          <button
            class="question__submit btn btn-success"
            @click.prevent="onNext"
          >
            next
          </button>
        </div>
      </div>
      <button
        v-show="qCount === ques.length"
        class="quiz__submit btn btn-success"
        style="grid-area: 2 / 2"
        @click="onSubmit"
      >
        Submit
      </button>
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
      .question__optioninput[checked] ~ .question__optionlabel {
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
