<template>
  <v-container>
    <v-row>
      <v-col cols="5" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Dashboard</h1>

        <p class="subheading font-weight-regular">
          Op deze pagina ziet u visualisaties en analyses die inzicht geven in
          de werking en het performen van de applicatie. De pagina toont
          algemene statistieken zoals het aantal bekende regels en het aantal
          uitgevoerde regelchecks. Daarnaast kunt u ook zien wat de verhouding
          positieve en negatieve bevindingen over de tijd is.
        </p></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="3">
        <v-card v-if="expertStatistics">
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
        </v-card>
      </v-col>
      <v-col cols="9">
        <source-statistics-component />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2 class="mb-3">Trends per bron per kwaliteitsregel</h2>
      </v-col>
    </v-row>
    <v-container v-for="(value, source) in findingsBatchAreaData" :key="source">
      <v-row
        ><v-col
          ><h3 class="mb-3">{{ source }}</h3></v-col
        >
      </v-row>
      <v-row>
        <v-col
          v-for="(rule, index) in findingsBatchAreaData[source][0][1]"
          :key="rule[0]"
          cols="4"
          v-show="
            findingsBatchAreaData[source].some(
              (x) => x[1][index].pass != 0 || x[1][index].fail != 0
            )
          "
        >
          <v-card>
            <v-card-title> {{ rule.name }} </v-card-title>
            <findings-area-chart
              :data="
                findingsBatchAreaData[source].map((x) => {
                  return {
                    date: x[0].slice(0, 16),
                    true: x[1][index].pass,
                    false: x[1][index].fail,
                  };
                })
              "
              style="height: 250px"
            ></findings-area-chart>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import FindingsAreaChart from "@/components/charts/FindingsAreaChart.vue";
import { Rule } from "@/types/rule";
import { CountObject } from "@/types/chartTypes";
import { Importance } from "@/types/importance";
import SourceStatisticsComponent from "./SourceStatisticsComponent.vue";

export default Vue.extend({
  name: "LspDashboardComponent",
  components: {
    FindingsAreaChart,
    SourceStatisticsComponent,
  },
  data: () => ({
    rules: [],
    findingsAreaData: [],
    findingsBatchAreaData: {},
    expertStatistics: undefined,
  }),
  computed: {
    rulePieChartData: function (): CountObject[] {
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
    ruleImportancePieChartData: function (): CountObject[] {
      const presentImportances: number[] = [
        ...new Set(this.$data.rules.map((rule: Rule) => rule.importance)),
      ] as number[];
      const countObjects = presentImportances.map((importance: number) => ({
        key: Importance[importance],
        count: this.$data.rules.filter(
          (rule: Rule) => rule.importance == importance
        ).length,
      }));
      return countObjects;
    },
  },
  methods: {
    getRules() {
      axios
        .get(`${this.$store.state.APIurl}/rule`)
        .then((response) => {
          this.$data.rules = response.data;
        })
        .catch((error) => {
          this.$data.rules = [];
        });
    },
    getFindingsAreaData() {
      axios
        .get(`${this.$store.state.APIurl}/finding/area-chart`)
        .then((response) => {
          this.$data.findingsAreaData = response.data;
        })
        .catch((error) => {
          this.$data.findingsAreaData = [];
        });
    },
    getFindingsBatchAreaData() {
      axios
        .get(`${this.$store.state.APIurl}/finding/area-batch-chart`)
        .then((response) => {
          this.$data.findingsBatchAreaData = response.data;
        })
        .catch((error) => {
          this.$data.findingsBatchAreaData = [];
        });
    },
    getExpertStatistics() {
      axios
        .get(`${this.$store.state.APIurl}/statistics`)
        .then((response) => {
          this.$data.expertStatistics = response.data;
        })
        .catch((error) => {
          this.$data.expertStatistics = undefined;
        });
    },
  },
  mounted() {
    this.getRules();
    this.getFindingsAreaData();
    this.getFindingsBatchAreaData();
    this.getExpertStatistics();
  },
});
</script>
