<template>
  <v-app>
    <v-app-bar absolute dense color="secondary" app>
      <v-container class="py-0 fill-height">
        <v-toolbar-items v-if="this.$store.state.user.isAuthenticated">
          <v-btn
            v-for="item in toolbar_items"
            :key="item.route"
            depressed
            exact
            plain
            text
            :ripple="false"
            :to="{ name: item.route }"
            class="headerItem"
            active-class="active-header-item"
            >{{ item.label }}</v-btn
          >
        </v-toolbar-items>
        <v-toolbar-items v-else>
          <v-btn
            depressed
            exact
            plain
            text
            :ripple="false"
            :to="{ name: 'Home' }"
            class="headerItem"
            active-class="active-header-item"
            >Home</v-btn
          >
          <v-btn
            depressed
            exact
            plain
            text
            :ripple="false"
            :to="{ name: 'Login' }"
            class="headerItem"
            active-class="active-header-item"
            >Inloggen</v-btn
          >
          <v-btn
            depressed
            exact
            plain
            text
            :ripple="false"
            :to="{ name: 'Rules' }"
            class="headerItem"
            active-class="active-header-item"
            >Kwaliteitsregels</v-btn
          >
        </v-toolbar-items>
        <v-spacer></v-spacer>
      </v-container>
    </v-app-bar>
    <v-main class="mt-5">
      <v-container>
        <v-row>
          <v-col> <router-view /> </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer color="secondary">
      <v-container class="py-0 fill-height">
        <v-row v-if="this.$store.state.user.isAuthenticated">
          <v-col cols="4"
            ><v-list color="secondary">
              <v-list-item>
                <router-link
                  :to="{ name: 'update-password' }"
                  class="footer-link"
                  >Wachtwoord wijzigen</router-link
                >
              </v-list-item>
              <v-list-item>
                <router-link :to="{ name: 'Logout' }" class="footer-link"
                  >Uitloggen</router-link
                >
              </v-list-item>
            </v-list></v-col
          ></v-row
        >
      </v-container>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "App",

  data: () => ({
    app_name: process.env.VUE_APP_TITLE,
    toolbar_items: [
      { label: "Home", route: "Home" },
      { label: "Analyse", route: "Demonstration" },
      { label: "Dashboard", route: "Dashboard" },
      { label: "Kwaliteitsregels", route: "Rules" },
      { label: "Bevindingen", route: "Findings" },
      { label: "Brondocumenten", route: "Documents" },
      { label: "Leveringen", route: "Batches" },
      { label: "Projectnummmers", route: "Projects" },
    ],
  }),
});
</script>

<style>
.headerItem > span.v-btn__content {
  color: var(--v-headerTextColour-base);
  text-transform: none !important;
  border-bottom: 3px solid transparent !important;
}
.headerItem:hover {
  color: var(--v-headerTextColour-base);
  text-decoration: underline;
  text-decoration-color: var(--v-headerTextColour-base);
  background: var(--v-headerHoverColour-base);
}
.active-header-item {
  background: var(--v-headerHoverColour-base);
  border-bottom: 3px solid var(--v-primary-base) !important;
}
.v-btn--plain:not(.v-btn--active):not(.v-btn--loading):not(:focus):not(:hover)
  .v-btn__content {
  opacity: 1 !important;
}

a.footer-link {
  color: var(--v-headerTextColour-base) !important;
  display: block;
  text-decoration: none;
}

a.footer-link:hover {
  text-decoration: underline;
}
</style>
