<script setup>
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
await store.dispatch("fetchStats");
const stats = computed(() => store.state.stats);
console.log(stats.value);
const { bySubject } = stats.value;
</script>

<template>
  <div class="container">
    <h1>User Summary</h1>
    <p>Subject wise:</p>
    <ul>
      <li v-for="(stat, key) in bySubject" :key>
        {{ stat.name }}: {{ stat.score }} / {{ stat.total }} | average:
        {{ stat.average }}
      </li>
    </ul>
  </div>
</template>
