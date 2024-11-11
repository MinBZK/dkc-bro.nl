<template>
  <batches-component />
</template>

<script lang="ts">
import Vue from "vue";
import BatchesComponent from "../components/BatchesComponent.vue";

export default Vue.extend({
  name: "Batches",

  components: {
    BatchesComponent,
  },
});
</script>
