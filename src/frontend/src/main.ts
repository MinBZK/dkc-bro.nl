import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

if (process.env.NODE_ENV === "production" && process.env.DOCKER_DEV === "false") {
  store.commit("changeAPIurl", `${window.location.origin}/api`);
}

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
