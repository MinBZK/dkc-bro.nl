<template>
  <v-container>
    <v-row style="justify-content: center">
      <v-col cols="12" sm="12" md="10" lg="10">
        <h1>Registreer een account</h1>
        <p>
          Op deze pagina kunnen accounts worden aangemaakt voor het gebruik van
          de applicatie.
        </p>
        <v-divider class="mb-4"></v-divider>
        <h2>Registreer</h2>

        <v-form @submit.prevent ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="E-mail adres"
                outlined
                v-model="newUserCredentials.email"
                id="newUserEmail"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="Wachtwoord"
                outlined
                v-model="newUserCredentials.password"
                id="password"
                required
                type="password"
                autocomplete="new-password"
                :rules="[
                  (v) => !!v || 'Wachtwoord moet zijn ingevuld.',
                  (v) =>
                    (v && v.length >= 8) ||
                    'Wachtwoord moet minstens 8 karakters lang zijn.',
                ]"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="Herhaal wachtwoord"
                outlined
                v-model="newUserCredentials.repeatPassword"
                id="repeatPassword"
                required
                type="password"
                autocomplete="new-password"
                :rules="[
                  (v) => !!v || 'Wachtwoordherhaling moet zijn ingevuld.',
                  this.newUserCredentials.password ===
                    this.newUserCredentials.repeatPassword ||
                    'Wachtwoord en wachtwoordherhaling moeten overeenkomen.',
                ]"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-select
                label="Organisatie"
                outlined
                v-model="newUserCredentials.org_code"
                id="orgCode"
                required
                :items="availableOrgs"
                :rules="[
                  (v) => !!v || 'Organisatie moet zijn ingevuld.',
                ]"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="12" md="6" lg="12">
              <v-btn
                :disabled="!valid"
                color="primary"
                elevation="1"
                block
                large
                @click="CreateUser"
                id="newUserSubmit"
              >
                <v-icon dark medium> mdi-plus </v-icon>
                Registreer</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
        <template v-if="this.state === 'loaded'">
          <v-alert class="mt-8" type="success">
            <p>
              <strong
                >Account succesvol aangemaakt. Uw QR-Code voor
                twee-factor-authenticatie is opgestuurd naar het opgegeven
                emailadres. Vervolgens kunt u inloggen met het opgegeven
                wachtwoord en teruggegeven 2FA code.</strong
              >
              <br />
              Klik <router-link :to="{ name: 'Login' }"> hier</router-link> om
              naar de login-pagina te navigeren.
            </p>
          </v-alert>
        </template>
        <br />
        <template v-if="this.error">
          <v-alert type="error">
            Er is iets mis gegaan:
            <pre> {{ this.detail.data.detail[0]['msg'] }} </pre>
          </v-alert>
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { UserCreated } from "@/types/user";

const states = {
  idle: "idle",
  loading: "loading",
  loaded: "loaded",
  failed: "failed",
};

export default Vue.extend({
  name: "RegisterUserComponent",
  data: () => ({
    availableOrgs: [
      { text: "Rijkswaterstaat", value: "rws" },
      // Add future organizations here ...
    ],
    newUserCredentials: {
      email: "",
      password: "",
      repeatPassword: "",
      org_code: "",
    },
    valid: false,
    state: "idle",
    error: undefined,
    detail: [],
    states,
    token: "",
    headers: "Content-Type=application/x-www-form-urlencoded",
  }),
  methods: {
    CreateUser() {
      this.state = "loading";
      this.error = undefined;
      axios
        .post(`${this.$store.state.APIurl}/user/`, {
          email: `${this.newUserCredentials.email}`,
          password: `${this.newUserCredentials.password}`,
          repeated_password: `${this.newUserCredentials.repeatPassword}`,
          org_code: `${this.newUserCredentials.org_code}`,
        })
        .then((response) => {
          const response_data: UserCreated =
            response.data as unknown as UserCreated;
          this.state = "loaded";
        })
        .catch((error) => {
          if (error.response.status >= 400) {
            this.detail = error.response;
          }
          this.state = "failed";
          this.error = error;
        });
    },
  },
});
</script>
