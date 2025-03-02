<script setup>
import { reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const data = reactive({
  email: '',
  password: '',
})

async function submit() {
  await store.dispatch('loginUser', data).then(() =>
    document.startViewTransition(() => router.push('/quiz')))
}
function toLabel(attr) {
  return `${attr[0].toUpperCase()}${attr.slice(1)}`
}
</script>

<template>
  <form @submit.prevent="submit">
    <h1 class="display-5 text-center">Login</h1>
    <div v-for="attr in Object.keys(data)" :key="attr">
      <div class="form-floating mt-2">
        <input class="form-control" v-model="data[attr]" :type="attr === 'password' ? 'password' : 'text'" :id="attr" />
        <label :for="attr">{{ toLabel(attr) }}</label>
      </div>
    </div>
    <button class="btn btn-primary mt-3" type="submit">
      login
    </button>
  </form>
</template>
