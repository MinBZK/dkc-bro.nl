<template>
  <project-component />
</template>

<script lang="ts">
import Vue from "vue";
import ProjectComponent from "../components/ProjectsComponent.vue";

export default Vue.extend({
  name: "Rules",

  components: {
    ProjectComponent,
  },
});
</script>
