<template>
  <v-container>
    <v-row style="justify-content: center">
      <v-col cols="12" sm="12" md="10" lg="10">
        <h2>Wachtwoord vergeten</h2>
        <p>
          Op deze pagina kunt u een nieuw wachtwoord aanvragen indien u uw
          wachtwoord bent vergeten. Het nieuwe wachtwoord zal naar uw mailadres
          verstuurd worden.
        </p>
        <p>
          Om er zeker van te zijn dat u zelf het nieuwe wachtwoord aanvraagt,
          vragen wij u om de code uit uw Authenticator in te vullen ter
          verificatie.
        </p>
        <v-divider class="mb-4"></v-divider>
        <v-form ref="form" v-model="isFormValid" @submit.prevent>
          <v-row>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="E-mail adres"
                outlined
                v-model="email"
                id="mailAddress"
                required
                type="text"
                autocomplete="username"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="8" lg="12">
              <v-text-field
                label="Eenmalige code uit de Authenticator-app"
                outlined
                v-model="filledinTOTP"
                :rules="totpRules"
                :counter="6"
                id="loginTOTP"
                required
                autocomplete="off"
                v-on:keyup.enter="Login"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="6" lg="12">
              <v-btn
                color="accent"
                elevation="1"
                block
                large
                @click="ResetPassword"
                id="resetPasswordSubmit"
                :disabled="!isFormValid"
              >
                <v-icon dark medium> mdi-lock-reset </v-icon>
                Nieuw wachtwoord</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
        <template v-if="this.state === 'loaded'">
          <div class="alert succes">
            <p>
              <strong>Wachtwoord gewijzigd.</strong>
            </p>
            <p>
              Uw nieuwe wachtwoord vind u in uw mailbox. Dit kan even duren.
            </p>
          </div>
        </template>
        <br />
        <template v-if="this.error">
          <div class="alert error">
            Er is iets mis gegaan:
            <pre> {{ this.detail.data.detail }} </pre>
          </div>
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

const states = {
  idle: "idle",
  loading: "loading",
  loaded: "loaded",
  failed: "failed",
};

export default Vue.extend({
  name: "ResetPassword",
  data: () => ({
    email: "",
    filledinTOTP: "",
    isFormValid: false,
    state: "idle",
    error: undefined,
    detail: [],
    states,
    token: "",
    headers: "Content-Type=application/x-www-form-urlencoded",
    totpRules: [
      (v: string) =>
        !!v ||
        "De eenmalige code uit de Authenticator-app is verplicht, zorg dat deze op tijd wordt ingevoerd",
      (v: string) =>
        (v && v.length === 6) ||
        "De eenmalige code uit de Authenticator-app bestaat uit 6 cijfers ",
    ],
  }),
  methods: {
    ResetForm() {
      this.$data.email = "";
      this.$data.filledinTOTP = "";
    },
    ResetPassword() {
      this.state = "loading";
      this.error = undefined;
      axios
        .get(`${this.$store.state.APIurl}/user/reset-password`, {
          params: { email: this.$data.email, totp: this.$data.filledinTOTP },
        })
        .then((_) => {
          this.state = "loaded";
        })
        .catch((error) => {
          this.detail = error.response;
          this.state = "failed";
          this.error = error;
        });
      this.ResetForm();
    },
  },
});
</script>
