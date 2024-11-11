<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Projectnummers</h1>

        <p>
          Hier ziet u alle projectnummers opgesomd en welke actief zijn.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-table :headers="headers" :items="projects" class="elevation-2" dense>
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Projectnummers</v-toolbar-title>
            </v-toolbar>
          </template>
          <template v-slot:item.project_nr="{ item }">
            {{ item.project_nr }}
          </template>
          <template v-slot:item.project_name="{ item }">
            {{ item.project_name }}
          </template>
          <template v-slot:item.timestamp="{ item }">
            {{ new Date(item.timestamp).toLocaleString() }}
          </template>
          <template v-slot:item.active="{ item }">
            {{ item.active ? 'Actief' : 'Inactief' }}
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { Project } from "@/types/project";

export default Vue.extend({
  name: "RulesComponent",
  data: () => ({
    projects: [] as Project[],
    headers: [
      {
        text: "Projectnummer",
        value: "project_nr",
        width: '10px',
      },
      {
        text: "Projectnaam",
        value: "project_name",
        width: '100px',
      },
      {
        text: "Bronhouder",
        value: "source_holder",
        width: '100px',
      },
      {
        text: "Actief",
        value: "active",
        width: '10px',
      },
      {
        text: "Laatst toegevoegd",
        value: "timestamp",
        width: '50px',
      },
    ],
  }),
  methods: {
    getProjects() {
      axios
        .get(`${this.$store.state.APIurl}/project`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.projects = response.data;
        })
        .catch(() => {
          this.$data.projects = [];
        });
    },
  },
  mounted() {
    this.getProjects();
  },
});
</script>
