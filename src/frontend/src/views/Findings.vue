<template>
  <findings-component />
</template>

<script lang="ts">
import Vue from "vue";
import FindingsComponent from "../components/FindingsComponent.vue";

export default Vue.extend({
  name: "Findings",

  components: {
    FindingsComponent,
  },
});
</script>
