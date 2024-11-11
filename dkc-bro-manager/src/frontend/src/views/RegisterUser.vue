<template>
  <register-user-component />
</template>

<script lang="ts">
import Vue from "vue";
import RegisterUserComponent from "@/components/RegisterUserComponent.vue";

export default Vue.extend({
  name: "Login",

  components: {
    RegisterUserComponent,
  },
});
</script>
