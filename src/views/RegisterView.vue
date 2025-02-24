<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  qualification: '',
  dob: new Date().toISOString().split('T')[0],
})

const getType = (attr) => {
  if (attr === 'password') return 'password'
  if (attr === 'dob') return 'date'
  return 'text'
}
const handleSubmit = async (_) => {
  const response = await fetch('http://localhost:5000/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      password: user.password,
      qualification: user.qualification,
      dob: user.dob,
    }),
  })

  if (!response.ok) {
    throw new Error(`[ERROR: ${response.status}] failed to register user!`)
  }

  const { message } = await response.json()
  console.log('message from server:', message)

  if (response.ok)
    router.push('/login')
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
    <h1 class="display-5 text-center">Register</h1>
    <div v-for="attr in Object.keys(user)" :key="attr">
      <div class="form-floating mt-2">
        <input class="form-control" v-model="user[attr]" :type="getType(attr)" :id="attr" required />
        <label :for="attr">{{ toLabel(attr) }}</label>
      </div>
    </div>
    <button @click.stop.prevent="() => handleSubmit()" class="btn btn-primary mt-3" type="submit">
      register
    </button>
  </form>
</template>
