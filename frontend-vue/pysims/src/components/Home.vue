<template>
  <div>
    <Nav />
  </div>
  <div class="container pt-5">
    <div class="row mb-3">
      <div class="col-md-4 themed-grid-col">
        <h3>Available Models</h3>
        <li v-for="model in models" :key="model.id">
          {{ model }}
        </li>
      </div>
      <div class="col-md-4 themed-grid-col">
        <h3>Simulations history</h3>
        <TableVue />
      </div>
    </div>
  <div class="row mb-3"><h3>Results Graph to be placed</h3></div>

  </div>
</template>

<script>
import Nav from "./components/Nav.vue";
import TableVue from "./components/TableVue.vue";
import axios from "axios";

export default {
  data() {
    return {
      models: [],
    }
  },
  mounted() {
    axios.get("http://127.0.0.1:8000/get_available_models")
    .then(response => {
      this.models = response.data;
      console.log(this.models)
    })
    .catch(error => {
      alert(error)
    })
  },
  components: {
    Nav,
    TableVue,
  },
}

</script>
