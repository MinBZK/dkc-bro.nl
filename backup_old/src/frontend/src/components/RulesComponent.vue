<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">Kwaliteitsregels</h1>

        <p v-if="$store.state.user.isAuthenticated">
          Hier ziet u de kwaliteitsregels die per brondocument gelden. Op deze pagina kunt
          u de kwaliteitsregels inzien en beheren.
        </p>
        <p v-if="$store.state.user.isAuthenticated">
          De tabel kan gefilterd worden op het type regel en gewichten door middel van
          deze lijst. Een regel kan aangepast worden door op het Aanpassen icoon te
          klikken in de rij van de desbetreffende regel. Vervolgens kunt u de naam,
          gewicht en omschrijving van de regel aanpassen. Ook kunt u op deze manier regels
          actief of inactief maken.
        </p>
        <p v-if="!$store.state.user.isAuthenticated">
          Hier ziet u de kwaliteitsregels die per brondocument gelden. Op deze pagina kunt
          u de kwaliteitsregels inzien.
        </p>
      </v-col>
    </v-row>
    <v-row v-if="$store.state.user.isAuthenticated">
      <v-col cols="6">
        <v-select
          v-model="selectedDocumentType"
          :items="documentTypes"
          label="Documenttype"
        ></v-select>
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="selectedGewichtType"
          :items="sortedGewicht"
          item-text="key"
          item-value="value"
          label="Gewicht"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="filteredRules"
          class="elevation-2"
          dense
          :item-key="'object_type' + 'id'"
          :sort-by="['object_type', 'id']"
        >
          <template v-slot:top v-if="$store.state.user.isAuthenticated">
            <v-toolbar flat>
              <v-toolbar-title>Regelbeheeer</v-toolbar-title>
              <v-dialog v-model="dialog" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">Pas regel aan</v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <p>
                            <strong>Id: </strong>
                            {{ editedRule.object_type }}-{{ editedRule.id }}
                          </p>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-checkbox v-model="editedRule.enabled" label="Actief">
                          </v-checkbox>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-text-field
                            v-model="editedRule.name"
                            label="Regelnaam"
                            required
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12">
                          <v-select
                            v-model="editedRule.importance"
                            :items="
                              Object.values(Importance)
                                .filter((value) => typeof value === 'string')
                                .map((key) => ({
                                  key: key,
                                  value: Importance[key],
                                }))
                            "
                            item-text="key"
                            item-value="value"
                            label="Gewicht"
                            required
                          ></v-select>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-textarea
                            v-model="editedRule.explanation"
                            label="Omschrijving"
                            required
                          ></v-textarea>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-textarea
                            v-model="editedRule.docstring"
                            label="Uitleg uitgebreid"
                            required
                          ></v-textarea>
                        </v-col> </v-row></v-container
                  ></v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                      Sluit venster
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="saveRule(editedRule)">
                      Sla op
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.id="{ item }">
            {{ item.object_type }}-{{ item.id }}
          </template>
          <template v-slot:item.importance="{ item }">
            <v-chip v-if="item.importance == 1" color="blue" text-color="white" x-small>
              {{ Importance[item.importance] }}</v-chip
            >
            <v-chip
              v-else-if="item.importance == 2"
              color="orange"
              text-color="white"
              x-small
            >
              {{ Importance[item.importance] }}</v-chip
            >
            <v-chip
              v-else-if="item.importance == 3"
              color="red"
              text-color="white"
              x-small
            >
              {{ Importance[item.importance] }}</v-chip
            >
          </template>
          <template v-slot:item.enabled="{ item }">
            <v-icon color="green" v-if="item.enabled" small> mdi-check-bold </v-icon>
            <v-icon color="red" v-else small> mdi-close-thick </v-icon>
          </template>
          <template
            v-if="$store.state.user.isAuthenticated"
            v-slot:item.actions="{ item }"
          >
            <v-icon small class="mr-2" @click="editRule(item)"> mdi-pencil </v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { Rule } from "@/types/rule";
import { Importance } from "@/types/importance";
import { ImportancewithAlle } from "@/types/importance";
import store from "@/store";

export default Vue.extend({
  name: "RulesComponent",
  data: () => ({
    rules: [] as Rule[],
    documentTypes: ["Alle"],
    selectedDocumentType: "Alle",
    selectedGewichtType: 0,
    Importance: Importance,
    ImportancewithAlle: ImportancewithAlle,
    dialog: false,
    editedIndex: -1,
    editedRule: {
      name: "",
      importance: 0,
      explanation: "",
      docstring: "",
    },
    defaultRule: {
      name: "",
      id: "",
      object_type: "",
      importance: 0,
      explanation: "",
      docstring: "",
    },
    headers: [
      { text: "Actief", value: "enabled", width: "90px" },
      { text: "id", value: "id" },
      {
        text: "Naam",
        align: "start",
        value: "name",
      },
      { text: "Gewicht", value: "importance" },
      { text: "Omschrijving", value: "explanation" },
      { text: "Uitleg uitgebreid", value: "docstring" },
      {
        text: store.state.user.isAuthenticated ? "Aanpassen" : "",
        value: "actions",
        sortable: false,
        align: "center",
      },
    ],
  }),
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  computed: {
    filteredRules: function (): Rule[] {
      if (store.state.user.isAuthenticated) {
        return this.rules.filter(
          (rule: Rule) =>
            (rule.object_type == this.selectedDocumentType ||
              this.selectedDocumentType === "Alle") &&
            (rule.importance == this.selectedGewichtType ||
              this.selectedGewichtType === 0)
        );
      } else {
        return this.rules.filter(
          (rule: Rule) => rule.importance == 2 || rule.importance == 3
        );
      }
    },
    sortedGewicht() {
      let gewichten = Object.values(ImportancewithAlle)
        .filter((value) => typeof value === "string")
        .map((key: any) => ({
          key: key,
          value: ImportancewithAlle[key],
        }));
      return gewichten;
    },
  },
  methods: {
    getRules() {
      axios
        .get(`${this.$store.state.APIurl}/rule`, {
          headers: { Authorization: `Bearer ${this.$store.state.user.token}` },
        })
        .then((response) => {
          this.$data.rules = response.data;
          const presentTypes: string[] = [
            ...new Set(this.$data.rules.map((rule: Rule) => rule.object_type)),
          ] as string[];
          this.$data.documentTypes = ["Alle"].concat(presentTypes.sort());
        })
        .catch(() => {
          this.$data.rules = [];
        });
    },
    editRule(rule: Rule) {
      this.editedIndex = this.rules.indexOf(rule);
      this.editedRule = Object.assign({}, rule);
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedRule = Object.assign({}, this.defaultRule);
        this.editedIndex = -1;
      });
    },
    saveRule(rule: Rule) {
      if (this.editedIndex > -1) {
        Object.assign(this.rules[this.editedIndex], this.editedRule);
        axios
          .put(`${this.$store.state.APIurl}/rule/${rule.object_type}/${rule.id}`, rule, {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.token}`,
            },
          })
          .then((response) => {
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      }
      this.close();
    },
  },
  mounted() {
    this.getRules();
  },
});
</script>
