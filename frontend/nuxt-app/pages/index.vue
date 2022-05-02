<template>
  <div>
    <Nav />
  </div>
  <div class="container pt-5">
    <div class="row mb-3">
      <div class="col-md-4 themed-grid-col">
        <h3>Available Models</h3>
        <li v-for="model in data">
          {{ model }}
        </li>
      </div>
        <div class="col-md-4 themed-grid-col">
            <h3>
                Simulations history
            </h3>
          <Table />
        </div>
      </div>
    </div>
</template>

<script setup>
const { data } = await useFetch("http://127.0.0.1:8000/get_available_models");
</script>
