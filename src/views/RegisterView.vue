<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = ref({
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

async function submit() {
  const { first_name, last_name } = user.value

  await fetch('http://localhost:5000/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: `${first_name} ${last_name}`,
      ...user.value
    }),
  }).then(async (response) => {
    user.value = {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      qualification: '',
      dob: new Date().toISOString().split('T')[0]
    };

    if (!response.ok)
      throw new Error(`[ERROR] FAILED TO REGISTER USER`)
    else {
      const { message } = await response.json()
      console.log('[LOG]', message)

      router.push('/login')
    }
  })
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
    <button @click.stop.prevent="submit" class="btn btn-primary mt-3" type="submit">
      register
    </button>
  </form>
</template>
