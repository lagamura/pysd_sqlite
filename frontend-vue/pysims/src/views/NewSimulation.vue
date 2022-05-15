<template>
  <div class="container pt-5">
    <div class="d-flex justify-content: center">
      <!--not working centered-->
      <h3 class="pb-5">Results of your Simulation</h3>
    </div>
    <div class="row mb-3">
      <div class="col-md-4 themed-grid-col">
        Here Posts component deactivated for debugging purposes
      </div>
      <div class="col-md-4 themed-grid-col">
        <p>Line Chart to be implemented</p>
        <LineChart />
      </div>
    </div>
  </div>
</template>

<script setup>
import ResultsGraph from "../components/ResultsGraph.vue";
import ResultsGraphVue from "../components/ResultsGraphVue.vue";
import BarChart from "../components/BarChart.vue";
import LineChart from "../components/LineChart.vue";
import Posts from "../components/Posts.vue";
</script>