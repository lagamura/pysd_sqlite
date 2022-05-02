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
      <tr v-for="item in data" :key="item">
        <td v-for="field in fields" :key="field">{{ item[field] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
const { data } = await useFetch("http://127.0.0.1:8000/get_simuls");
const fields = ["id", "name", "csv_path", "date"];
</script>
