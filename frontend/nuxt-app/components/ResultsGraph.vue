<template>
<h3>
    This is the plot Component
</h3>
</template>

<script setup>
import * as d3 from "d3";

d3.csv("../user/results/Teacup/2022_05_02-22_08_51.csv", function (data) {
  console.log(data)
});
</script>
