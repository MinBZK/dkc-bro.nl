<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Brondocumenten</h1>

        <p>
          Als expert kunt u hier de rapportage van de meest recent
          gecontroleerde brondocumenten inzien.
        </p>
        <p>
          U kunt recent in het Bronhouderportaal gecontroleerde documenten
          inzien. De lijst van documenten kan gefilterd worden op document-type
          en op het soort bevinding. Door op een document te klikken wordt
          zichtbaar welke regels er zijn gecontroleerd en wat de bevindingen
          zijn.
        </p>
      </v-col>
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
          v-model="selectedResultType"
          :items="resultTypes"
          label="Resultaten"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-iterator :items="filteredResults" item-key="timestamp">
          <template v-slot:default="{ items }">
            <v-expansion-panels>
              <v-expansion-panel
                v-for="(findingOverview, index) in items"
                :key="index"
              >
                <v-expansion-panel-header>
                  <v-col cols="11">
                    <div>
                      <p class="font-weight-bold">
                        {{ findingOverview.filename }}
                      </p>
                      <p>
                        {{
                          new Date(findingOverview.timestamp).toLocaleString()
                        }}
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="1">
                    <v-chip
                      v-if="
                        findingOverview.findings.some(
                          (x) => x.Finding.result == false
                        )
                      "
                      color="red"
                      outlined
                    >
                      {{
                        findingOverview.findings.filter(
                          (finding) => finding.Finding.result
                        ).length
                      }}/{{ findingOverview.findings.length }}</v-chip
                    >
                    <v-chip v-else color="green" outlined>
                      {{ findingOverview.findings.length }}/{{
                        findingOverview.findings.length
                      }}</v-chip
                    >
                  </v-col>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-simple-table dense>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-left">Resultaat</th>
                          <th class="text-left">Regel</th>
                          <th class="text-left">Feedback</th>
                          <th class="text-left">Regel-id</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="finding in findingOverview.findings"
                          :key="finding.Finding.id"
                        >
                          <td>
                            <v-icon v-if="finding.Finding.result" color="green">
                              mdi-check-circle
                            </v-icon>
                            <v-icon v-else color="red">
                              mdi-close-circle</v-icon
                            >
                          </td>
                          <td>{{ finding.Rule.name }}</td>
                          <td>{{ finding.Finding.feedbackMessage }}</td>
                          <td>{{ finding.Finding.rule_id }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </template>
        </v-data-iterator>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { Document } from "@/types/document";

export default Vue.extend({
  name: "DocumentsComponent",
  data: () => ({
    results: [],
    documentTypes: ["Alle"],
    resultTypes: ["Alle", "Alleen met fouten"],
    selectedDocumentType: "Alle",
    selectedResultType: "Alle",
  }),
  computed: {
    filteredResults: function (): Document[] {
      return this.results.filter(
        (result: Document) =>
          (result.object_type == this.selectedDocumentType ||
            this.selectedDocumentType === "Alle") &&
          (result.findings.some((x) => x.Finding.result == false) ||
            this.selectedResultType == "Alle")
      );
    },
  },
  methods: {
    getresults() {
      axios
        .get(
          `${this.$store.state.APIurl}/finding/documents?skip=0&limit=1000`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.token}`,
            },
          }
        )
        .then((response) => {
          this.$data.results = response.data;
          const presentTypes: string[] = [
            ...new Set(
              this.$data.results.map((result: Document) => result.object_type)
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
