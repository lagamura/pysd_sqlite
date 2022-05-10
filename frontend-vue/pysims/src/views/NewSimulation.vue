<template>
  <div class="container pt-5">
      <h3 class="pb-5">Create a new simulation</h3>
    <div class="row mb-3">
      <div class="col-md-4 themed-grid-col">
        <ListAvailableModels/>
      </div>
      <div class="col-md-4 themed-grid-col">
        <ResultsGraphVue/>
      </div>
    </div>
  </div>
</template>

<script setup>
import ListAvailableModels from '../components/ListAvailableModels.vue';
import ResultsGraph from '../components/ResultsGraph.vue';
import ResultsGraphVue from '../components/ResultsGraphVue.vue';
</script>