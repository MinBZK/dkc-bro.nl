<template>
  <demonstration-component />
</template>

<script lang="ts">
import Vue from "vue";
import DemonstrationComponent from "../components/DemonstrationComponent.vue";

export default Vue.extend({
  name: "Home",

  components: {
    DemonstrationComponent,
  },
});
</script>
