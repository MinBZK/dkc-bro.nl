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
              met de demo knoppen.
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
            v-for="findingOverview in findings"
            :key="findingOverview.filename"
          >
            <v-expansion-panel-header>
              <span>
                <v-icon> mdi-file-document</v-icon>
                {{ findingOverview.filename }}
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
                      v-for="finding in findingOverview.findings"
                      :key="(finding.ruleId, finding.objectType)"
                    >
                      <td>
                        <v-icon v-if="finding.result" color="green">
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
                      <td>{{ finding.objectType }}-{{ finding.ruleId }}</td>
                      <td>{{ finding.feedbackMessage }}</td>
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
import { FindingOverview } from "@/types/finding";

export default Vue.extend({
  name: "DemonstrationComponent",

  data: () => ({
    app_name: process.env.VUE_APP_TITLE,
    files: [],
    findings: [] as FindingOverview[],
    loading: false,
    isFormValid: false,
    fileInputRules: [
      (files: any) =>
        files.reduce((sum: number, current: any) => sum + current.size, 0) <
          20000000 || "Upload maximaal 20 MB aan bestanden per keer.",
    ],
  }),
  methods: {
    postFilesForValidation() {
      this.$data.loading = true;
      const formData = new FormData();
      for (let i = 0; i < this.$data.files.length; i++) {
        formData.append("documents", this.$data.files[i]);
      }
      console.log(formData);
      const headers = {
        "Content-Type": "multipart/form-data",
      };
      axios
        .post(`${this.$store.state.APIurl}/document/demo-dry`, formData, {
          headers: headers,
        })
        .then((response) => {
          this.$data.findings = response.data;
          this.$data.loading = false;
        })
        .catch((_) => {
          this.$data.findings = [];
          this.$data.loading = false;
        });
    },
    performDemonstration(demo: string) {
      this.$data.loading = true;
      axios
        .post(`${this.$store.state.APIurl}/document/demo-examples-files`, demo)
        .then((response) => {
          this.$data.findings = response.data;
          this.$data.loading = false;
        })
        .catch((_) => {
          this.$data.findings = [];
          this.$data.loading = false;
        });
    },
  },
});
</script>
