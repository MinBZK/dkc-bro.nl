<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mb-4">
        <h1 class="display-2 font-weight-bold mb-5">
          {{ app_name }}
        </h1>

        <h3>Over deze Datakwaliteitscontrole service</h3>
        <p>
          Gebruikers van de BRO rekenen erop dat ondergrondgegevens in de BRO
          juist zijn. Deze Datakwaliteitscontrole
          <strong>service</strong> controleert brondocumenten op geldende
          kwaliteitsregels.
        </p>
        <p>
          <strong>Als Expert</strong> kunt u in het Bronhouderportaal BRO per
          levering zien wat de bevindingen zijn van de automatische
          kwaliteitscontrole. Alle bevindingen worden bewaard en kunnen in het
          dashboard weergegeven worden zodat u een overzicht heeft van de
          geleverde kwaliteit. Ga naar
          <router-link :to="{ name: 'Login' }">inloggen</router-link> om inzicht
          te krijgen in de resultaten en de geldende kwaliteitsregels beheren.
        </p>
        <p>
          <strong>Als Leverancier</strong> en <strong>Expert</strong> kunt u een
          eerste indruk opdoen van de Datakwaliteitscontrole service door de
          <router-link :to="{ name: 'Demonstration' }">DEMO</router-link> uit te
          voeren. Een standaard Demoset met brondocumenten worden gecontroleerd.
          De bevindingen worden niet opgeslagen.
        </p>
        <p>
          <strong>Als Leverancier </strong>kunt u de kwaliteit van de
          BRO-ondergrondgegevens bekijken en verbeteren vóórdat de
          brondocumenten worden aangeleverd aan de BRO. Dit voorkomt dat
          aangeleverde bestanden na aanlevering worden afgekeurd. Via
          <router-link :to="{ name: 'Demonstration' }">Analyse</router-link>
          kunt u de Datakwaliteitscontrole op uw eigen bestanden uitvoeren. De
          bevindingen worden niet opgeslagen.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "LandingComponent",

  data: () => ({
    app_name: process.env.VUE_APP_TITLE,
  }),
});
</script>
