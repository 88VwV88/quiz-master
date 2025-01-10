<script setup>
import { reactive } from 'vue';

const user = reactive({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    qualification: '',
    dob: '',
});
const getType = (attr) => {
    if (attr === 'password')
        return 'password';
    if (attr === 'dob')
        return 'date';
    return 'text';
}
const handleSubmit = async (event) => {
    console.log(user);
    const { msg } = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    }).then((res) => res.json());
    console.log(msg);
}
</script>

<template>
    <form @submit.prevent.once="handleSubmit">
        <div v-for="attr in Object.keys(user)">
            <label :for="attr">{{ attr }}</label>
            <input v-model="user[attr]" :type="getType(attr)" :id="attr" />
        </div>
        <input type="submit" value="Login" />
    </form>
</template>