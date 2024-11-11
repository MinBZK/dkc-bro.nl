<template>
  <update-password-component />
</template>

<script lang="ts">
import Vue from "vue";
import UpdatePasswordComponent from "@/components/UpdatePasswordComponent.vue";

export default Vue.extend({
  name: "UpdatePassword",

  components: {
    UpdatePasswordComponent,
  },
});
</script>
