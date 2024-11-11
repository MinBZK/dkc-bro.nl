<template>
  <v-container> </v-container>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "LogoutComponent",
  mounted() {
    this.logoutUser();
  },
  methods: {
    logoutUser() {
      sessionStorage.removeItem("jwt");
      this.$store.commit("changeUserEmail", "");
      this.$store.commit("changeUserAdmin", false);
      this.$store.commit("changeUserAuthenticated", false);
      this.$store.commit("changeUserToken", "");
      this.$store.commit("changeUserOrgName", "");
      this.$store.commit("changeUserOrgCode", "");
      this.$router.push("/login");
    },
  },
});
</script>
