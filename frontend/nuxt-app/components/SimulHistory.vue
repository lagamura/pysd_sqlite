<template>
  <h3>Simulation History</h3>
  <li v-for="simul in data">
    {{ simul }}
  </li>
</template>

<script setup>
const { data } = await useFetch("http://127.0.0.1:8000/get_simuls");
</script>
