<script setup>
import { reactive } from 'vue';

const { quizzes } = await fetch('http://127.0.0.1:5000/quizzes').then((res) => res.json());
const newQuiz = reactive({
    name: '',
    subject: '',
    chapter: '',
});
const questions = reactive([]);
const handleSubmit = () => {
    fetch('http://127.0.0.1:5000/quizzes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: newQuiz.name,
            subject: newQuiz.subject,
            chapter: newQuiz.chapter,
            questions: questions
        })
    }).then(x => x.json()).then(console.log);
}
const addQuestion = () => {
    const options = [];
    for (let i = 0; i < 4; ++i)
        options.push({ statement: '' });
    questions.push({
        statement: '',
        options: options,
        answer: 0,
    });
}
const removeQuestion = (index) => {
    while (index-- > 0)
        questions.push(questions.shift());
    questions.shift();
}
</script>

<template>
    <div>
        <h1>Available Quizzes</h1>
        <div v-for="q in quizzes">
            <h2>{{ q.title }}</h2>
            <p>{{ q.remarks }}</p>
            <p>{{ q.questions.length }} questions</p>
            <button>Start</button>
        </div>
        <button popovertarget="new-quiz-popover">+New Quiz</button>
        <div id="new-quiz-popover" popover>
            <form @submit.prevent.once="handleSubmit">
                <div v-for="attr in Object.keys(newQuiz)">
                    <label :for="attr">{{ attr }}</label>
                    <input v-model="newQuiz[attr]" type="text" :id="attr" />
                </div>
                <p>Questions:</p><button @click.prevent.stop="addQuestion">+</button>
                <ul>
                    <li v-for="(ques, i) in questions" :key="i">
                        <div>
                            <p>question {{ i + 1 }}</p>
                            <input v-model="ques.statement">
                            <ul>
                                <li v-for="(opt, j) in ques.options" :key="j">
                                    <label for="">option {{ j + 1 }}: </label>
                                    <input v-model="opt.statement">
                                </li>
                            </ul>
                            <input type="number" v-model="ques.answer" </div>
                            <button @click.prevent.stop="() => removeQuestion(i)">-</button>
                    </li>
                </ul>
                <button type="submit" popovertargetaction="hide">Add Quiz</button>
            </form>
        </div>
    </div>

</template>

<style>
#new-quiz-popover {
    height: 80dvh;
    width: 80dvw;
    border-radius: 16px;
    justify-content: center;
    align-content: center;
    text-align: center;
}

ul {
    list-style: none;
}
</style>