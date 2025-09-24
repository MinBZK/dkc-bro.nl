<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Dashboard</h1>

        <p>
          <strong>Als Expert</strong> is het belangrijk inzicht te hebben in
          de kwaliteit van de aangeleverde BRO-ondergrondgegevens.
        </p>
        <p>
          De datakwaliteitscontroles die in de loop van de tijd worden gedaan
          kunnen geanalyseerd worden.
        </p>
        <p>
          Op deze pagina worden de resultaten van de in het Bronhouderportaal
          uitgevoerde Datakwaliteitscontroles in figuren getoond. Deze
          resultaten helpen om zelf een analyse uit te voeren op de
          kwaliteitsaspecten. De figuren zijn aan uw wensen aan te passen, zodat
          u b.v. alleen foutmeldingen voor de sonderingen ten opzichte van de
          boormonsterprofielen kunt zien.
        </p>
        <p>
          Bovendien kunt u alle bevindingen exporteren naar een CSV-bestand.
        </p>
        <ul>
          <li>
            Resultaten van controles uit het Bronhouderportaal analyseren
            <ul>
              <li>Kwaliteitsregels per object</li>
              <li>Bevindingen per object</li>
              <li>Bevindingen in een periode</li>
            </ul>
          </li>
        </ul>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card v-if="expertStatistics">
          <div style="display: flex;">
            <div style="flex: 1;">
              <v-card-title>Statistieken</v-card-title>
              <v-card-text>
                <p>
                  <b>{{ expertStatistics.rules }}</b> regels bekend.
                </p>
                <p>
                  <b>{{ expertStatistics.findings }}</b> regelchecks uitgevoerd.
                </p>
                <p>
                  <b>{{ expertStatistics.batches }}</b> leveringen bekend.
                </p>
              </v-card-text>
            </div>
            <div style="flex: 1;">
              <v-card-title>Exporteer alle bevindingen</v-card-title>
              <v-card-text>
                Mocht u een export willen maken van alle bevindingen, kunt u dat hier doen.
                <strong>Let op, de start- en einddatum mogen niet meer dan 1 jaar van elkaar verschillen.</strong>
                <v-row>
                  <v-col cols="12" sm="7">
                    <v-menu v-model="menu" :close-on-content-click="false" transition="scale-transition" offset-y
                      min-width="290px">
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field v-model="dateRangeText" label="Selecteer een start- en einddatum"
                          prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"> <template v-slot:append>
                            <v-btn small icon @click="dateRangeText = ''">
                              <v-icon>mdi-close</v-icon>
                            </v-btn>
                          </template></v-text-field>
                      </template>
                      <v-date-picker v-model="dates" range></v-date-picker>
                    </v-menu>
                  </v-col>
                </v-row>
                <v-btn class="mt-4" color="primary" v-on:click="downloadDump()" :disabled="dates.length < 2">Download
                  CSV-bestand</v-btn>

                <v-dialog v-model="isLoading" max-width="400">
                  <v-card>
                    <v-card-title>Download is bezig, even geduld aub...</v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-progress-linear v-if="isLoading" indeterminate></v-progress-linear>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="dialogNoFindings" max-width="400">
                  <v-card>
                    <v-card-title>Niets gevonden</v-card-title>
                    <v-card-text>{{ noFindingsFound }}</v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="dialogNoFindings = false">Sluit venster</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="errorMessage" max-width="400">
                  <v-card>
                    <v-card-title>Selecteer een andere einddatum</v-card-title>
                    <v-card-text>Einddatum ligt verder dan een jaar tov begindatum!</v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="errorMessage = false">Sluit venster</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-card-text>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-title> Kwaliteitsregels per type </v-card-title>
          <bar-chart v-if="rules.length > 0" :data="ruleBarChartData"></bar-chart>
        </v-card>
      </v-col>
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-title> Kwaliteitsregels per gewicht </v-card-title>
          <bar-chart v-if="rules.length > 0" :data="ruleImportanceBarChartData"></bar-chart>
        </v-card>
      </v-col>
      <v-col cols="12">
        <v-card>
          <v-card-title> Bevindingen over tijd </v-card-title>
          <findings-area-chart v-if="findingsAreaData.length > 0" :data="findingsAreaData"></findings-area-chart>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import FindingsAreaChart from "@/components/charts/FindingsAreaChart.vue";
import BarChart from "@/components/charts/BarChart.vue";
import { Rule } from "@/types/rule";
import { CountObject } from "@/types/chartTypes";
import { Importance } from "@/types/importance";

export default Vue.extend({
  name: "DashboardComponent",
  components: {
    FindingsAreaChart,
    BarChart,
  },
  data: () => ({
    rules: [],
    findingsAreaData: [],
    expertStatistics: undefined,
    dates: [],
    dialogNoFindings: false,
    noFindingsFound: '',
    isLoading: false,
    menu: false,
    maxDate: null,
    dateRangeText: '',
    errorMessage: '',
  }),
  computed: {
    ruleBarChartData: function (): CountObject[] {
      const presentTypes: string[] = [
        ...new Set(this.$data.rules.map((rule: Rule) => rule.object_type)),
      ] as string[];
      const countObjects = presentTypes.map((type: string) => ({
        key: type,
        count: this.$data.rules.filter((rule: Rule) => rule.object_type == type)
          .length,
      }));
      return countObjects;
    },
    ruleImportanceBarChartData: function (): CountObject[] {
      const presentImportances: number[] = [
        ...new Set(this.$data.rules.map((rule: Rule) => rule.importance)),
      ] as number[];
      const countObjects = presentImportances
        .sort((a, b) => (a > b ? 1 : -1))
        .map((importance: number) => ({
          key: Importance[importance],
          count: this.$data.rules.filter(
            (rule: Rule) => rule.importance == importance
          ).length,
        }));
      return countObjects;
    },
  },
  methods: {
    downloadDump() {
      this.isLoading = true;
      const [start_date, end_date] = this.$data.dateRangeText.split(' ~ ').sort();
      axios({
        url: `${this.$store.state.APIurl}/finding/download`,
        method: "GET",
        responseType: "blob",
        headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        params: {
          start_date: start_date,
          end_date: end_date,
        },
      })
        .then((response) => {
          let fileURL = window.URL.createObjectURL(new Blob([response.data]));
          let fURL = document.createElement("a");
          this.$data.isLoading = false;

          fURL.href = fileURL;
          const currentDate = new Date().toLocaleDateString('en-GB').split('/').reverse().join('-');
          fURL.setAttribute("download", `dump_bevindingen_${currentDate}.csv`);
          document.body.appendChild(fURL);
          fURL.click();
        })
        .catch((error) => {
          this.$data.dialogNoFindings = true;
          this.$data.noFindingsFound = 'Geen resultaten gevonden voor deze start- en einddatum, kies een andere datum.';
          this.$data.isLoading = false;
          console.log(error);
        });
    },
    getRules() {
      axios
        .get(`${this.$store.state.APIurl}/rule`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.rules = response.data;
        })
        .catch((error) => {
          this.$data.rules = [];
        });
    },
    getFindingsAreaData() {
      axios
        .get(`${this.$store.state.APIurl}/finding/area-chart`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.findingsAreaData = response.data;
        })
        .catch((error) => {
          this.$data.findingsAreaData = [];
        });
    },
    getExpertStatistics() {
      axios
        .get(`${this.$store.state.APIurl}/statistics`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.expertStatistics = response.data;
        })
        .catch((error) => {
          this.$data.expertStatistics = undefined;
        });
    },
  },
  watch: {
    dates(newDates) {
      if (newDates.length === 2) {
        const startDate = new Date(newDates[0]);
        const endDate = new Date(newDates[1]);
        const oneYearLater = new Date(startDate);
        oneYearLater.setFullYear(startDate.getFullYear() + 1);
        console.log(startDate)

        if (endDate > oneYearLater) {
          this.$data.dates = [];
          this.$data.dateRangeText = '';
          this.$data.errorMessage = 'The selected dates must lie within one year or less.';
        } else {
          this.dateRangeText = `${newDates[0]} ~ ${newDates[1]}`;
        }
      }
    },
  },
  mounted() {
    this.getRules();
    this.getFindingsAreaData();
    this.getExpertStatistics();
  },
});
</script>
