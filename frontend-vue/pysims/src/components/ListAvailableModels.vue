<template>
      <div class="list-group">
        <h3>List of Available Models</h3>
        <a v-for="model in models" :key="model.id">
          {{ model }}
        </a>
      </div>
</template>

<script>
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
}

</script>