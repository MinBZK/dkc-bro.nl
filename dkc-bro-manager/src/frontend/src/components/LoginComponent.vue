<template>
  <v-container>
    <v-row style="justify-content: center">
      <v-col cols="12">
        <p>
          Nog geen account? Klik
          <router-link :to="{ name: 'Register-User' }">hier</router-link> om een
          account te registreren of navigeer naar de
          <router-link :to="{ name: 'Demonstration' }"
            >demonstratiepagina</router-link
          >
          om vrijblijvend uw bestanden te controleren.
        </p>
        <h1 class="mb-4">Login</h1>
        <v-form @submit.prevent ref="form" v-model="valid">
          <v-row>
            <v-col cols="12">
              <v-text-field
                label="E-mailadres"
                :rules="emailRules"
                outlined
                v-model="loginCredentials.filledinUser"
                id="loginEmail"
                required
                autocomplete="off"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Wachtwoord"
                outlined
                v-model="loginCredentials.filledinPassword"
                :rules="passwordRules"
                id="loginPassword"
                type="password"
                required
                autocomplete="off"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Code uit de Authenticator-app"
                outlined
                v-model="loginCredentials.filledinTOTP"
                :rules="totpRules"
                :counter="6"
                id="loginTOTP"
                required
                autocomplete="off"
                v-on:keyup.enter="Login"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="4" lg="12">
              <v-btn
                color="primary"
                elevation="1"
                block
                large
                @click="Login"
                id="loginSubmit"
                :disabled="!valid"
              >
                <v-icon dark medium> mdi-lock </v-icon>
                Inloggen</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
        <p class="pt-5">
          Bent u uw wachtwoord vergeten? Klik
          <router-link :to="{ name: 'reset-password' }">hier</router-link> om
          een nieuw wachtwoord aan te vragen.
        </p>
        <template v-if="this.error">
          <div class="alert error">
            Er is iets mis gegaan:
            <pre> {{ this.error }} </pre>
          </div>
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { User } from "@/types/user";
import { Token } from "@/types/token";

const totpLength = 6;

export default Vue.extend({
  name: "LoginComponent",

  data: () => ({
    loginCredentials: {
      filledinUser: "",
      filledinPassword: "",
      filledinTOTP: "",
    },
    valid: true,
    error: undefined,
    headers: "Content-Type=application/x-www-form-urlencoded",
    emailRules: [
      (v: string) => !!v || "E-mailadres is verplicht",
      (v: string) => /.+@.+\..+/.test(v) || "Voer een geldig E-mailadres in",
    ],
    passwordRules: [(v: string) => !!v || "Wachtwoord is verplicht"],
    totpRules: [
      (v: string) =>
        !!v ||
        "De eenmalige code uit de Authenticator-app is verplicht, zorg dat deze op tijd wordt ingevoerd",
      (v: string) =>
        (v && v.length === totpLength) ||
        "De eenmalige code uit de Authenticator-app bestaat uit 6 cijfers ",
    ],
  }),
  methods: {
    Login() {
      this.error = undefined;
      axios
        .post(
          `${this.$store.state.APIurl}/user/login`,
          `username=${this.loginCredentials.filledinUser}&password=${this.loginCredentials.filledinPassword}${this.loginCredentials.filledinTOTP}`
        )
        .then((response) => {
          const response_data: Token = response.data as unknown as Token;
          const access_token: string = response_data.access_token;
          sessionStorage.setItem("jwt", access_token);
          this.$store.commit("changeUserToken", access_token);
          this.verifyAndRedirect();
        })
        .catch((error) => {
          this.error = error;
        });
    },
    verifyAndRedirect() {
      axios
        .get(`${this.$store.state.APIurl}/user/login/verifieer`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.user.token}`,
          },
        })
        .then((response) => {
          const response_data: User = response.data;
          this.$store.commit("changeUserToken", this.$store.state.user.token);
          this.$store.commit("changeUserEmail", response_data.email);
          this.$store.commit("changeUserAdmin", response_data.admin);
          this.$store.commit("changeUserAuthenticated", true);
          this.$store.commit("changeUserOrgName", response_data.org_name);
          this.$store.commit("changeUserOrgCode", response_data.org_code);
          this.$store.commit("changeOrgId", response_data.org_id);
        })
        .catch((error) => {
          sessionStorage.removeItem("jwt");
          this.$store.commit("changeUserToken", "");
          this.$store.commit("changeUserEmail", "");
          this.$store.commit("changeUserAdmin", false);
          this.$store.commit("changeUserAuthenticated", false);
          this.$store.commit("changeUserOrgName", "");
          this.$store.commit("changeUserOrgCode", "");
          this.$store.commit("changeOrgId", null);
        });
      this.$router.push("/");
    },
  },
});
</script>

<style lang="scss" scoped></style>
