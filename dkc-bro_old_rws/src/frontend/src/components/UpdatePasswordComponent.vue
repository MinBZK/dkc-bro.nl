<template>
  <v-container>
    <v-row style="justify-content: center">
      <v-col cols="12" sm="12" md="10" lg="10">
        <h2>Wijzig wachtwoord</h2>
        <p>
          Op deze pagina kunt u uw wachtwoord aanpassen. Uw nieuwe wachtwoord
          moet minstens 8 karakters bevatten.
        </p>
        <v-divider class="mb-4"></v-divider>
        <v-form ref="form" v-model="isFormValid" @submit.prevent>
          <v-row>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="E-mail adres"
                outlined
                disabled
                :value="this.$store.state.user.email"
                id="mailAddress"
                required
                type="text"
                autocomplete="username"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="12">
              <v-text-field
                label="Nieuw wachtwoord"
                outlined
                v-model="newPassword.newPassword"
                id="newPassword"
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
                label="Herhaal nieuw wachtwoord"
                outlined
                v-model="newPassword.repeatNewPassword"
                id="repeatNewPassword"
                required
                type="password"
                autocomplete="new-password"
                :rules="[
                  (v) => !!v || 'Wachtwoordherhaling moet zijn ingevuld.',
                  this.newPassword.newPassword ===
                    this.newPassword.repeatNewPassword ||
                    'Wachtwoord en wachtwoordherhaling moeten overeenkomen.',
                ]"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="6" lg="12">
              <v-btn
                color="accent"
                elevation="1"
                block
                large
                @click="UpdatePassword"
                id="newPasswordSubmit"
                :disabled="!isFormValid"
              >
                <v-icon dark medium> mdi-lock-reset </v-icon>
                Wijzig wachtwoord</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
        <template v-if="this.state === 'loaded'">
          <div class="alert succes">
            <p>
              <strong>Wachtwoord gewijzigd.</strong>
            </p>
            <p>U kunt vanaf nu inloggen met uw nieuwe wachtwoord.</p>
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
  name: "UpdatePassword",
  data: () => ({
    newPassword: {
      newPassword: "",
      repeatNewPassword: "",
    },
    isFormValid: false,
    state: "idle",
    error: undefined,
    detail: [],
    states,
    token: "",
    headers: "Content-Type=application/x-www-form-urlencoded",
  }),
  mounted() {
    this.token = sessionStorage.getItem("jwt") || "{}";
  },
  methods: {
    ResetForm() {
      this.newPassword = { newPassword: "", repeatNewPassword: "" };
      (
        this.$refs.form as Vue & { resetValidation: () => void }
      ).resetValidation();
    },
    UpdatePassword() {
      this.state = "loading";
      this.error = undefined;
      axios
        .put(
          `${this.$store.state.APIurl}/user/update`,
          {
            password: `${this.newPassword.newPassword}`,
          },
          { headers: { Authorization: `Bearer ${this.token}` } }
        )
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

<style lang="scss" scoped></style>
