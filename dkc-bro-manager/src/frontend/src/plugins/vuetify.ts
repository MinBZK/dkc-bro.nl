import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import nl from "vuetify/src/locale/nl";

Vue.use(Vuetify);

const default_theme = {
  primary: "#1976D2",
  secondary: "#1976D2",
  accent: "#82B1FF",
  error: "#FF5252",
  info: "#2196F3",
  success: "#4CAF50",
  warning: "#FFC107",
  headerTextColour: "#FFFFFF",
  headerHoverColour: "#328de6",
};
const rws_theme = {
  primary: "#007bc7",
  secondary: "#f9e11e",
  accent: "#82B1FF",
  error: "#FF5252",
  info: "#2196F3",
  success: "#4CAF50",
  warning: "#FFC107",
  headerTextColour: "#000000",
  headerHoverColour: "#FCF29A",
};

export default new Vuetify({
  theme: {
    themes: {
      light: process.env.VUE_APP_THEME == "RWS" ? rws_theme : default_theme,
    },
    options: { customProperties: true, cspNonce: "eQw4j9WgXcB" },
  },
  lang: {
    locales: { nl },
    current: "nl",
  },
});
