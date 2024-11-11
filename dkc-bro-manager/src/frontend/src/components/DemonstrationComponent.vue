<template>
  <v-container>
    <v-overlay :value="loading">
      <v-progress-circular
        color="secondary"
        indeterminate
        absolute
        size="128"
        width="8"
      >
      </v-progress-circular>
    </v-overlay>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Analyse</h1>
        <p>
          U kunt als BRO-gegevens leverancier zelf één of meerdere
          gegevensbestand(en) laten controleren en het resultaat bekijken. De
          kwaliteit van de gegevens kan hiermee verbeterd worden vóórdat u ze
          aanlevert aan de BRO.
        </p>
        <p>
          Bent u leverancier dan helpt de Datakwaliteitscontrole service bij
        </p>
        <ul>
          <li>Controleren van één bestand</li>
          <li>Controleren meerdere bestand</li>
          <li>Controleren levering met meerdere bestanden</li>
        </ul>
        <p>
          De bevindingen uit de kwaliteitscontrole worden weergegeven in de vorm
          van waarschuwingen, fouten, en informatieve meldingen.
        </p>
        <p>
          U kunt als BRO-software leverancier de Datakwaliteitscontrole service
          gebruiken om uw software te beproeven.
        </p>
      </v-col>
    </v-row>

    <v-row class="center">
      <v-col cols="5">
        <v-row>
          <v-col cols="12">
            <h2 class="mb-4">Demo</h2>
            <p>
              Zelf de analyse uitproberen met een aantal voorbeeldbestandjes kan
              met de demo knoppen op basis van Rijkswaterstaat kwaliteitsregels.
            </p>
            <v-btn
              class="mr-4"
              v-on:click="performDemonstration('bodemdomein')"
              color="primary"
              >Demo bodem</v-btn
            >
            <v-btn
              v-on:click="performDemonstration('waterdomein')"
              color="primary"
              >Demo water</v-btn
            >
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-form v-model="isFormValid">
              <h2>Voer eigen bestanden in</h2>
              <v-file-input
                counter
                multiple
                show-size
                small-chips
                v-model="files"
                accept=".xml,.zip"
                :rules="fileInputRules"
              />
              <v-btn
                class="mt-4"
                v-on:click="postFilesForValidation()"
                color="primary"
                :disabled="!files.length > 0 || !isFormValid"
                >Controleer</v-btn
              >
            </v-form>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="7">
        <h2>Bevindingen</h2>
        <v-expansion-panels>
          <v-expansion-panel
            v-for="(documentFindings, document) in groupedFindings"
            :key="document"
          >
            <v-expansion-panel-header>
              <span>
                <v-icon> mdi-file-document</v-icon>
                {{ document }}
              </span>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-simple-table dense>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">Resultaat</th>
                      <th class="text-left">Regel-id</th>
                      <th class="text-left">Feedback</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="finding in documentFindings"
                      :key="finding.rule"
                    >
                      <td>
                        <v-icon v-if="finding.result.passed" color="green">
                          mdi-check-circle
                        </v-icon>
                        <v-icon
                          v-else-if="finding.importance == 1"
                          color="blue"
                        >
                          mdi-information
                        </v-icon>
                        <v-icon
                          v-else-if="finding.importance == 2"
                          color="orange"
                        >
                          mdi-alert
                        </v-icon>
                        <v-icon v-else-if="finding.importance == 3" color="red">
                          mdi-close-circle
                        </v-icon>
                      </td>
                      <td>{{ finding.rule }}</td>
                      <td>{{ finding.result.feedback_message || 'Geen feedback' }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { FindingOverview, GroupedFindings } from "@/types/finding";

export default Vue.extend({
  name: "DemonstrationComponent",

  data: () => ({
    app_name: process.env.VUE_APP_TITLE,
    files: [] as File[],
    findings: { results: [] as FindingOverview[] },
    loading: false,
    isFormValid: false,
    fileInputRules: [
      (files: File[]) =>
        files.reduce((sum: number, current: File) => sum + current.size, 0) <
          20000000 || "Upload maximaal 20 MB aan bestanden per keer.",
    ],
  }),

  computed: {
    groupedFindings(): { [key: string]: FindingOverview[] } {
      return this.findings.results.reduce((acc: GroupedFindings, finding: FindingOverview) => {
        if (!acc[finding.document]) {
          acc[finding.document] = [];
        }
        acc[finding.document].push(finding);
        return acc;
      }, {} as { [key: string]: FindingOverview[] });
    }
  },

  methods: {
    postFilesForValidation() {
      this.loading = true;
      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        formData.append("documents", this.files[i]);
      }
      const headers: Record<string, string> = {
        "Content-Type": "multipart/form-data",
      };
      let endpoint = "/document/rws-demo-dry";

      const loggedIn = this.$store.state.user.isAuthenticated;
      if (loggedIn) {
        headers["Authorization"] = `Bearer ${this.$store.state.user.token}`;
        endpoint = "/document/demo-dry";
      }

      axios
        .post(this.$store.state.APIurl + endpoint, formData, {
          headers: headers,
        })
        .then((response) => {
          this.$data.findings = response.data;
          this.loading = false;
        })
        .catch((_) => {
          this.findings = { results: [] };
          this.loading = false;
        });
    },

    performDemonstration(demo: string) {
      this.loading = true;
      let endpoint = "/document/rws-demo-examples-files";
      let headers;

      const loggedIn = this.$store.state.user.isAuthenticated;
      if (loggedIn) {
        headers = {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        };
        endpoint = "/document/demo-examples-files";
      }
      axios
        .post(this.$store.state.APIurl + endpoint, demo, headers)
        .then((response) => {
          this.$data.findings = response.data;
          this.loading = false;
        })
        .catch((_) => {
          this.findings = { results: [] };
          this.loading = false;
        });
    },
  },
});
</script>