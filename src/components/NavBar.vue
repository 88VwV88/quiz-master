<script setup>
import { RouterLink } from 'vue-router';

const { links } = defineProps(['links']);
</script>

<template>
    <nav>
        <ul>
            <li v-for="link in links">
                <RouterLink :to="link.url">{{ link.text }}</RouterLink>
            </li>
        </ul>
    </nav>
</template>

<style scoped>
ul {
    display: flex;
    list-style: none;
    justify-content: space-evenly;
}
</style>