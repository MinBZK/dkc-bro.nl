<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-3">
          <v-card-text>
            Welkom op de Verwerkingen pagina. Hier vindt je een overzicht van
            onze data, georganiseerd in een gebruiksvriendelijk format. Gebruik
            de tools om de informatie te filteren en analyseren zoals nodig.
            Hier zie je een overzicht van de organizaties, de regels die zijn
            toegepast, de status van de request en het tijdstip waarop de
            request is gemaakt.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-row>
            <v-col>
                <v-text-field v-model="filter" label="Filter" class="mb-4"></v-text-field>
            </v-col>
        </v-row> -->
    <v-row>
      <v-col>
        <v-data-table :headers="headers" :items="items" class="elevation-1">
          <template v-slot:item.rule_code="{ item }">
            <span>{{ item.rule_code }}</span>
          </template>
          <template v-slot:item.status="{ item }">
            <v-chip :color="item.status === true ? 'green' : 'red'" dark>
              {{ item.status === true ? "voltooid" : "mislukt" }}
            </v-chip>
          </template>
          <template v-slot:item.timestamp="{ item }">
            <span>{{ item.timestamp }}</span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
//import { filter } from 'vue/types/umd';

export default {
  name: "DemoTabel",
  data() {
    return {
      headers: [
        { text: "Organisatie", value: "org_name" },
        { text: "Regelcode", value: "rule_code" },
        { text: "Status", value: "status" },
        { text: "Tijd", value: "timestamp" },
      ],
      items: [],
      //filter: '',
    };
  },
  // computed: {
  //     filteredItems() {
  //         // const searchTerm = this.filter.trim().toLowerCase();
  //         // if (!searchTerm) {
  //         //     return this.items;
  //         // }

  //         return this.items.filter(item => {
  //             const searchTerm = this.filter.toLowerCase();
  //             return (
  //                 item.org_name.toLowerCase() === searchTerm ||//.includes(searchTerm) ||// //
  //                 item.rule_code.toLowerCase() === searchTerm ||// === searchTerm ||
  //                 item.status.toLowerCase() === searchTerm ||// === searchTerm ||
  //                 item.timestamp.toLowerCase() === searchTerm// === searchTerm
  //             );
  //         });
  //     },
  // },
  mounted() {
    axios
      .get(`${this.$store.state.APIurl}/process-requests/processing-request`, {
        headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
      })
      .then((response) => {
        console.log(response.data);
        this.items = response.data;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
};
</script>

<style scoped></style>
