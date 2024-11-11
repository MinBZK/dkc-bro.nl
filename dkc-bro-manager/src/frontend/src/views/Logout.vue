<template>
  <logout-component />
</template>

<script lang="ts">
import Vue from "vue";
import LogoutComponent from "@/components/LogoutComponent.vue";

export default Vue.extend({
  name: "Logout",

  components: {
    LogoutComponent,
  },
});
</script>
