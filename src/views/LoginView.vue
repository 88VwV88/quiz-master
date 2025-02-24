<script setup>
import { inject, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginData = reactive({
  email: '',
  password: '',
})

const current_user = inject('current_user')

function getType(attr) {
  return attr === 'password' ? 'password' : 'text'
}

async function handleSubmit(_) {
  const response = await fetch('http://127.0.0.1:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(loginData),
  })

  if (!response.ok) {
    throw new Error(`[ERROR: ${response.status}] failed to login user!`)
  }
  current_user.value = await response.json()

  router.push('/quiz')
}

function toLabel(attr) {
  return `${attr[0].toUpperCase()}${attr.slice(1)}`
}
</script>

<template>
  <form>
    <h1 class="display-5 text-center">Login</h1>
    <div v-for="attr in Object.keys(loginData)" :key="attr">
      <div class="form-floating mt-2">
        <input class="form-control" v-model="loginData[attr]" :type="getType(attr)" :id="attr" />
        <label :for="attr">{{ toLabel(attr) }}</label>
      </div>
    </div>
    <button @click.prevent.stop="handleSubmit" class="btn btn-primary mt-3" type="submit">
      login
    </button>
  </form>
</template>
