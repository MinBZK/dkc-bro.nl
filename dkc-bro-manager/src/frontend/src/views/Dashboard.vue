<template>
  <div>
    <lsp-dashboard-component v-if="app_name === 'Expertservice acc.nplo.nl'" />
    <dashboard-component v-else />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import DashboardComponent from "@/components/DashboardComponent.vue";
import LspDashboardComponent from "@/components/LspDashboardComponent.vue";

export default Vue.extend({
  name: "Dashboard",

  components: {
    DashboardComponent,
    LspDashboardComponent,
  },

  data: () => ({
    app_name: process.env.VUE_APP_TITLE,
  }),
});
</script>
