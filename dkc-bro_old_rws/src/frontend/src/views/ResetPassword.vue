<template>
  <reset-password-component />
</template>

<script lang="ts">
import Vue from "vue";
import ResetPasswordComponent from "@/components/ResetPasswordComponent.vue";

export default Vue.extend({
  name: "ResetPassword",

  components: {
    ResetPasswordComponent,
  },
});
</script>
