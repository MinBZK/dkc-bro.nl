<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Bevindingen</h1>

        <p class="subheading font-weight-regular">
          Bekijk hier de 100 meest recente bevindingen uit de database van de
          applicatie. De tabel kan gefilterd worden op documenttype en het
          mininum gewicht van de kwaliteitsregels.
        </p></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          v-model="selectedDocumentType"
          :items="documentTypes"
          label="Documenttype"
        ></v-select>
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="selectedImportanceLevel"
          :items="importanceLevels"
          label="Minimum gewicht van regel"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-table
          dense
          :headers="tableHeaders"
          :items="filteredResults"
          :items-per-page="10"
          class="elevation-1"
        >
          <template v-slot:item.Rule.importance="{ item }">
            <v-icon v-if="item.Finding.result" color="green">
              mdi-check-circle
            </v-icon>
            <v-icon v-else-if="item.Rule.importance == 1" color="blue">
              mdi-information
            </v-icon>
            <v-icon v-else-if="item.Rule.importance == 2" color="orange">
              mdi-alert
            </v-icon>
            <v-icon v-else-if="item.Rule.importance == 3" color="red">
              mdi-close-circle
            </v-icon>
          </template>
          <template v-slot:item.Finding.rule_id="{ item }">
            {{ item.Finding.rule_object_type }}-{{ item.Finding.rule_id }}
          </template>
          <template v-slot:item.Finding.timestamp="{ item }">
            {{ new Date(item.Finding.timestamp).toLocaleString() }}
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { RuleFinding } from "@/types/rule_finding";

export default Vue.extend({
  name: "resultsComponent",
  data: () => ({
    results: [],
    documentTypes: ["Alle"],
    importanceLevels: ["Alle", "Info", "Waarschuwing", "Fout"],
    selectedDocumentType: "Alle",
    selectedImportanceLevel: "Alle",
    tableHeaders: [
      {
        text: "Gewicht",
        value: "Rule.importance",
        sortable: false,
      },
      {
        text: "Bestandsnaam",
        value: "Finding.filename",
      },
      {
        text: "Regel-id",
        value: "Finding.rule_id",
      },
      {
        text: "Datum",
        value: "Finding.timestamp",
      },
      {
        text: "Feedback",
        value: "Finding.feedbackMessage",
      },
    ],
  }),
  computed: {
    filteredResults: function (): string[] {
      return this.results.filter(
        (result: RuleFinding) =>
          (result.Rule.object_type == this.selectedDocumentType ||
            this.selectedDocumentType === "Alle") &&
          (result.Rule.importance >=
            this.importanceLevels.indexOf(this.selectedImportanceLevel) ||
            this.selectedImportanceLevel === "Alle")
      );
    },
  },
  methods: {
    getresults() {
      axios
        .get(`${this.$store.state.APIurl}/finding`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.results = response.data;
          const presentTypes: string[] = [
            ...new Set(
              this.$data.results.map(
                (result: RuleFinding) => result.Rule.object_type
              )
            ),
          ] as string[];
          this.$data.documentTypes = ["Alle"].concat(presentTypes);
        })
        .catch((error) => {
          this.$data.results = [];
        });
    },
  },
  mounted() {
    this.getresults();
  },
});
</script>
<style scoped>
.critical {
  background-color: #ff000036 !important;
}
</style>
