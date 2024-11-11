<template>
  <rules-component />
</template>

<script lang="ts">
import Vue from "vue";
import RulesComponent from "../components/RulesComponent.vue";

export default Vue.extend({
  name: "Rules",

  components: {
    RulesComponent,
  },
});
</script>
