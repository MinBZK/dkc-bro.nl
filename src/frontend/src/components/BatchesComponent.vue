<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Leveringen</h1>

        <p>
          Hier kunt u als expert een leveringsnummer ingeven en direct de
          rapportage in pdf bekijken en downloaden. Deze rapportages worden
          bewaard.
        </p>
        <p>
          Als het nummer niet bekend is kunt u via zoeken de juiste levering
          selecteren.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-iterator
          :items="results"
          :items-per-page="5"
          item-key="result.id"
          :search="search"
        >
          <template v-slot:header>
            <v-toolbar dark color="blue darken-3" class="mb-5">
              <v-text-field
                v-model="search"
                clearable
                solo-inverted
                hide-details
                prepend-inner-icon="mdi-magnify"
                label="Zoek een levering"
              ></v-text-field>
            </v-toolbar>
          </template>
          <template v-slot:default="{ items }">
            <v-row v-for="result in items" :key="result.id">
              <v-col cols="12">
                <v-card style="width: 100%">
                  <v-row>
                    <v-col cols="10">
                      <v-card-title>
                        {{ result.id }}
                      </v-card-title>
                    </v-col>
                    <v-col cols="2" align="center" justify="center">
                      <v-btn
                        icon
                        x-large
                        center
                        @click="() => downloadReport(result)"
                      >
                        <v-icon> mdi-download </v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
          </template>
        </v-data-iterator>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-if="!production">
        <v-btn x-large center @click="() => startAnalysis()"
          >Start nieuwe analyse</v-btn
        ></v-col
      >
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  name: "BatchesComponent",
  data: () => ({
    results: [],
    search: "",
    production:
      process.env.NODE_ENV === "production" ||
      process.env.VUE_APP_TITLE === "Datakwaliteitscontrole BRO",
  }),
  methods: {
    getresults() {
      axios
        .get(`${this.$store.state.APIurl}/batch`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.results = response.data;
        })
        .catch((error) => {
          this.$data.results = [];
        });
    },
    downloadReport(item: { id: string }) {
      axios({
        url: `${this.$store.state.APIurl}/batch/report/` + item.id,
        method: "GET",
        responseType: "blob",
        headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
      })
        .then((response) => {
          let fileURL = window.URL.createObjectURL(new Blob([response.data]));
          let fURL = document.createElement("a");

          fURL.href = fileURL;
          fURL.setAttribute("download", `${item.id}.pdf`);
          document.body.appendChild(fURL);

          fURL.click();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    startAnalysis() {
      axios({
        url: `${this.$store.state.APIurl}/batch/scan`,
        method: "GET",
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  mounted() {
    this.getresults();
  },
});
</script>
