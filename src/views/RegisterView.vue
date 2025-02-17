<script setup>
import { reactive } from 'vue'

const user = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  qualification: '',
  dob: '',
})
const getType = (attr) => {
  if (attr === 'password') return 'password'
  if (attr === 'dob') return 'date'
  return 'text'
}
const handleSubmit = async (_) => {
  const { message } = await fetch('http://localhost:5000/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      password: user.password,
      qualification: user.qualification,
      dob: user.dob.toString(),
    }),
  }).then((res) => res.json())
  console.log('message from server:', message)
}
const toLabel = (attr) => {
  return attr
    .split('_')
    .map((str) => `${str[0].toUpperCase()}${str.slice(1)}`)
    .join(' ')
}
</script>

<template>
  <form>
    <div v-for="attr in Object.keys(user)" :key="attr">
      <div class="form-floating mt-2">
        <input class="form-control" v-model="user[attr]" :type="getType(attr)" :id="attr" />
        <label :for="attr">{{ toLabel(attr) }}</label>
      </div>
    </div>
    <button @click.stop.prevent="() => handleSubmit()" class="btn btn-primary mt-3" type="submit">
      register
    </button>
  </form>
</template>
