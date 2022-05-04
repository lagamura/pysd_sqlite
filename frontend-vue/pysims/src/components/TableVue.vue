<template>
  <table class="table table-striped table-dark">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Model</th>
        <th scope="col">Simulation Name</th>
        <th scope="col">Date</th>
      </tr>
    </thead>
    <tbody>
      <!-- Loop through the list get the each student data -->
      <tr v-for="item in models_history" :key="item">
        <td v-for="field in fields" :key="field">{{ item[field] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>

import axios from "axios";
import { onMounted } from "vue";
import {ref} from 'vue'


let models_history = ref([])

onMounted(async() => {
    await  axios.get("http://127.0.0.1:8000/get_simuls")
    .then(response => {
      models_history.value = response.data;
      console.log(models_history)
    })
    .catch(error => {
      alert(error)
    })
    })
    
const fields = ["id", "name", "csv_path", "date"];
</script>
