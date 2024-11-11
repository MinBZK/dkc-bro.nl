<template>
  <login-component />
</template>

<script lang="ts">
import Vue from "vue";
import LoginComponent from "@/components/LoginComponent.vue";

export default Vue.extend({
  name: "Login",

  components: {
    LoginComponent,
  },
});
</script>
