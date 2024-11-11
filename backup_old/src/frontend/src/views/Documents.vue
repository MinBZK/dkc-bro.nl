<template>
  <documents-component />
</template>

<script lang="ts">
import Vue from "vue";
import DocumentsComponent from "../components/DocumentsComponent.vue";

export default Vue.extend({
  name: "Documents",

  components: {
    DocumentsComponent,
  },
});
</script>
